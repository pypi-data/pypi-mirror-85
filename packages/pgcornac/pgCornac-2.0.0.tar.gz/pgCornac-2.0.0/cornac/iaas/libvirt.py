# Implementation of IaaS based on libvirt tools.
#
# Uses libvirt binding, virt-manager and guestfs tools to manage VM.
# Current purpose is PoC or development.


import logging
import os
from copy import deepcopy
from string import ascii_lowercase
from xml.etree import ElementTree as ET
from subprocess import CalledProcessError
from textwrap import dedent
from time import sleep
from urllib.parse import urlparse

import libvirt
import tenacity

from . import IaaS, check_url
from ..errors import Timeout
from ..ssh import logged_cmd
from ..utils import canonical_url_for


logger = logging.getLogger(__name__)


_1G = 1024 * 1024 * 1024


class LibVirtIaaS(IaaS):
    @classmethod
    def connect(cls, url, config):
        return cls(libvirt.open(url), config)

    def __init__(self, conn, config):
        self.conn = conn
        self.uri = conn.getURI()
        self.uri_p = urlparse(self.uri)
        self.config = config
        # Configuration Keys:
        #
        # DEPLOY_KEY: SSH public key to inject to access root user
        #             on new machines.
        # DNS_DOMAIN: DNS domain to build FQDN of machine on the IaaS.

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.uri)

    def attach_disk(self, domain, disk):
        xml = domain.XMLDesc()
        path = disk.path()
        disk.machine = self
        if path in xml:
            logger.debug("Disk %s already attached to %s.", path, disk.name())
            return

        xml = ET.fromstring(xml)
        xdevices = xml.find('./devices')
        xdisk0 = xdevices.find('./disk')
        xdisk = deepcopy(xdisk0)
        xsrc = xdisk.find('./source')
        xsrc.attrib['file'] = path

        # Try to place data disk after first one.
        xdisks = xml.findall(".//disk")
        xdevices.insert(1 + len(xdisks), xdisk)

        # Relabel each disks.
        xscsidisks = xml.findall(".//disk/target[@bus='scsi']/..")
        for i, xdisk in enumerate(xscsidisks):
            xtarget = xdisk.find('./target')
            xtarget.attrib['dev'] = 'sd' + ascii_lowercase[i]
            xdisk.remove(xdisk.find('./address'))
            xtarget.tail = xtarget.tail[:-2]  # Remove one indent level.

        xml = ET.tostring(xml, encoding="unicode")
        logger.debug("Attaching disk %s.", path)
        self.conn.defineXML(xml)

    def configure_cloudinit_datasource(self, domain, seedfrom):
        xml = domain.XMLDesc()
        xml = ET.fromstring(xml)
        xdomain = xml.find('.')
        # Ensure smbios is read from sysinfo
        xsmbios = xml.find('./os/smbios')
        if xsmbios is None:
            xsmbios = ET.SubElement(xml.find('./os'), 'smbios')
            xsmbios.set('mode', 'sysinfo')
        if 'sysinfo' != xsmbios.attrib['mode']:
            raise Exception("Can't configure SMBIOS from Sysinfo.")

        # Configure system serial for NoCloud cloud-init Datasource.
        xsysinfo = xml.find('./sysinfo')
        if xsysinfo is None:
            xsysinfo = ET.SubElement(xdomain, 'sysinfo')
            xsysinfo.set('type', 'smbios')
            xsysinfo.text = '\n    '
            xsysinfo.tail = '\n'
        xsystem = xml.find('./sysinfo/system')
        if xsystem is None:
            xsystem = ET.SubElement(xsysinfo, 'system')
            xsystem.text = '\n      '
            xsystem.tail = '\n    '
        xserial = xml.find("./sysinfo/system/entry[@name='serial']")
        if xserial is None:
            xserial = ET.SubElement(xsystem, 'entry')
            xserial.set('name', 'serial')
            xserial.tail = '\n    '
        xserial.text = f"ds=nocloud-net;s={seedfrom}"
        xml = ET.tostring(xml, encoding="unicode")
        self.conn.defineXML(xml)

    def close(self):
        self.conn.close()

    def create_disk(self, pool, name, size_gb):
        name = f"{name}.qcow2"
        pool = self.conn.storagePoolLookupByName(pool)
        try:
            disk = pool.storageVolLookupByName(name)
        except libvirt.libvirtError:
            pass
        else:
            logger.info("Reusing disk %s.", name)
            return disk

        size_b = size_gb * _1G
        # Preallocate 256K, for partition, PV metadata and mkfs.
        allocation = 256 * 1024
        xml = dedent(f"""\
        <volume type='file'>
          <name>{name}</name>
          <capacity unit='bytes'>{size_b}</capacity>
          <allocation unit='bytes'>{allocation}</allocation>
          <target>
            <format type='qcow2'/>
            <compat>1.1</compat>
            <features>
              <lazy_refcounts/>
            </features>
          </target>
        </volume>
        """)
        logger.info("Creating disk %s.", name)
        return pool.createXML(xml)

    class CloneRace(Exception):
        pass

    @tenacity.retry(
        after=tenacity.after_log(logger, logging.DEBUG),
        reraise=True,
        retry=tenacity.retry_if_exception_type(CloneRace),
        stop=tenacity.stop_after_attempt(15),
        wait=tenacity.wait_fixed(2) + tenacity.wait_random(0, 2),
    )
    def clone_machine(self, machine):
        # Create disk destination
        pool = machine.zoned_config('STORAGE_POOL_')
        clone_disk = self.create_disk(pool, f"{machine}-system", 1)
        xml = ET.fromstring(clone_disk.XMLDesc())
        # Delete it to let virt-clone clone it.
        clone_disk.delete()
        clone_disk = xml.find("./key").text

        clone_cmd = [
            "virt-clone",
            "--connect", self.uri,
            "--original", self.origin,
            "--name", machine.hostname,
            "--auto-clone",
            "--file", clone_disk,
        ]
        logger.info("Allocating machine %s.", machine)
        try:
            logged_cmd(clone_cmd)
        except CalledProcessError as e:
            last_line = e.stderr.splitlines()[-1]
            conflict = last_line.endswith('has asynchronous jobs running.')
            if conflict:
                raise self.CloneRace() from None
            raise

        return self.conn.lookupByName(machine.hostname)

    def create_machine(self, machine, data_size_gb):
        name = machine.hostname

        metadata_baseurl = canonical_url_for(
            "cornac.cloudinit_metadata", instance=name)
        check_url(metadata_baseurl)

        # The PoC reuses ressources until we have persistence of objects.
        try:
            domain = self.conn.lookupByName(name)
        except libvirt.libvirtError:
            domain = self.clone_machine(machine)
        else:
            logger.info("Reusing VM %s.", name)

        seedfrom = metadata_baseurl.replace('meta-data', '')
        logger.debug("Seeding VM from %s.", seedfrom)
        self.configure_cloudinit_datasource(domain, seedfrom=seedfrom)

        pool = machine.zoned_config('STORAGE_POOL_')
        disk = self.create_disk(pool, f'{name}-data', data_size_gb)
        self.attach_disk(domain, disk)

        return domain

    def delete_machine(self, machine):
        try:
            domain = self._ensure_domain(machine)
        except libvirt.libvirtError as e:
            if 'Domain not found' in str(e):
                return logger.debug("Already deleted.")
            raise
        state, _ = domain.state()
        if self.is_running(domain):
            domain.destroy()

        xml = ET.fromstring(domain.XMLDesc())
        for xsource in xml.findall('./devices/disk/source'):
            file_ = xsource.attrib['file']
            name = os.path.basename(file_)
            try:
                vol = self.conn.storageVolLookupByPath(file_)
            except libvirt.libvirtError as e:
                logger.debug("Failed to get handle on disk %s: %s", name, e)
                continue
            logger.info("Deleting disk image %s.", file_)
            vol.delete()

        logger.info("Undefining domain %s.", domain.name())
        domain.undefineFlags(
            libvirt.VIR_DOMAIN_UNDEFINE_MANAGED_SAVE |
            libvirt.VIR_DOMAIN_UNDEFINE_NVRAM |
            libvirt.VIR_DOMAIN_UNDEFINE_SNAPSHOTS_METADATA |
            0
        )

    def is_running(self, machine):
        try:
            domain = self._ensure_domain(machine)
        except libvirt.libvirtError as e:
            logger.debug("Failed to get domain %s: %s.", machine, e)
            return False
        state, _ = domain.state()
        return libvirt.VIR_DOMAIN_RUNNING == state

    def list_machines(self):
        for domain in self.conn.listAllDomains():
            name = domain.name()
            if name == self.origin:
                continue
            if name.startswith(self.prefix):
                yield domain

    def _ensure_domain(self, domain_or_machine):
        if isinstance(getattr(domain_or_machine, "hostname", None), str):
            return self.conn.lookupByName(domain_or_machine.hostname)
        return domain_or_machine

    def endpoint(self, machine):
        domain = self._ensure_domain(machine)
        # Let's DNS resolve machine IP for now.
        return domain.name() + self.config['DNS_DOMAIN']

    def guess_data_device_in_guest(self, machine):
        domain = self._ensure_domain(machine)
        # Guess /dev/disk/by-path/… device file from XML.
        xml = ET.fromstring(domain.XMLDesc())
        name = f'{domain.name()}-data'
        for xdisk in xml.findall(".//disk"):
            if name in xdisk.find('./source').attrib['file']:
                xdiskaddress = xdisk.find('./address')
                break
        else:
            raise Exception(f"Can't find disk {name} in VM.")

        xcontrolleraddress = xml.find(
            ".//controller[@type='scsi']/address[@type='pci']")
        pci_path = 'pci-{domain:04x}:{bus:02x}:{slot:02x}.{function}'.format(
            bus=int(xcontrolleraddress.attrib['bus'], base=0),
            domain=int(xcontrolleraddress.attrib['domain'], base=0),
            function=int(xcontrolleraddress.attrib['function'], base=0),
            slot=int(xcontrolleraddress.attrib['slot'], base=0),
        )
        # cf.
        # https://cgit.freedesktop.org/systemd/systemd/tree/src/udev/udev-builtin-path_id.c#n405
        scsi_path = 'scsi-{controller}:{bus}:{target}:{unit}'.format(
            **xdiskaddress.attrib)
        return f'/dev/disk/by-path/{pci_path}-{scsi_path}'

    def start_machine(self, machine, wait=300):
        domain = self._ensure_domain(machine)
        name = domain.name()
        state, _ = domain.state()
        if self.is_running(domain):
            logger.debug("VM %s running.", name)
        else:
            logger.info("Starting VM %s.", name)
            domain.create()
        self.wait_state(domain, libvirt.VIR_DOMAIN_RUNNING, wait)

    def stop_machine(self, machine, wait=60):
        domain = self._ensure_domain(machine)
        name = domain.name()
        state, _ = domain.state()
        if libvirt.VIR_DOMAIN_SHUTOFF == state:
            logger.debug("VM %s stopped.", name)
        else:
            logger.info("Stopping VM %s.", name)
            domain.shutdown()

        logger.debug("Waiting for VM %s to shutdown.", name)
        self.wait_state(domain, libvirt.VIR_DOMAIN_SHUTOFF, wait)
        logger.debug("VM %s is down.", name)

    def wait_state(self, domain, wanted, wait=60):
        if not wait:
            return

        for _ in range(int(wait)):
            state, _ = domain.state()
            if wanted == state:
                break
            else:
                sleep(1)
            wait -= 1
        else:
            raise Timeout()
