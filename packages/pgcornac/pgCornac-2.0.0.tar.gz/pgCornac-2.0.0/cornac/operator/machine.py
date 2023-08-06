import logging
from urllib.parse import urlparse

from flask import current_app

from ..core import list_availability_zones
from ..ssh import RemoteShell, wait_machine
from ..utils import make_tenant_hash, zoned_config


logger = logging.getLogger(__name__)


class Machine:
    # IaaS independent data and operation on a single machine
    #
    # Help operator manage per-machine operator data and execute SSH command on
    # a single machine.

    _supg = ["sudo", "-iu", "postgres"]

    _hostname_fmt = '{prefix}{identifier}-{tenant}{z}'

    auto_zone = object()

    def __init__(self, instance, zone=None):
        self.instance = instance
        # By default, use zone of instance. For MultiAZ instance, fallback to
        # first zone must be explicitly requested using zone=auto_zone.
        if self.auto_zone == zone:
            if instance.data.get('MultiAZ'):
                zone, *_ = list_availability_zones()
            else:
                zone = zone = None
        self.zone = zone or instance.data['AvailabilityZone']

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self)

    def __str__(self):
        return self.hostname

    @property
    def data(self):
        opdata = self.instance.operator_data
        if opdata is None:
            raise KeyError('machines')
        return opdata['machines'].setdefault(
            self.hostname, dict(zone=self.zone))

    @property
    def fqdn(self):
        return self.hostname + current_app.config['DNS_DOMAIN']

    @property
    def ident(self):
        return dict(
            identifier=self.instance.identifier,
            prefix=current_app.config['MACHINE_PREFIX'],
            tenant=self.instance.data['TenantHash'],
            region=self.instance.data['Region'],
            zone=self.zone,
            z=self.zone[-1],
        )

    @property
    def hostname(self):
        return self._hostname_fmt.format(**self.ident)

    @property
    def shell(self) -> RemoteShell:
        return RemoteShell('root', self.data['admin_ip'])

    def is_running(self):
        try:
            address = self.data['admin_ip']
        except KeyError:
            # For error log.
            address = self.fqdn
        try:
            self.shell(['true'])
            return True
        except Exception as e:
            logger.debug("Failed to contact host %s: %s.", address, e)
            return False

    def ssh_authorize_key(self, key, user='postgres'):
        self.shell([
            "bash", "-c", f"echo {key} >> ~{user}/.ssh/authorized_keys",
        ])

    def ssh_keygen(self, comment):
        logger.info('Generating SSH key on Postgres host.')
        path = "/var/lib/pgsql/.ssh/id_rsa"
        self.shell(self._supg + [
            # Sudo -i breaks passing emtpy arguments. See
            # https://stackoverflow.com/questions/27892812/passing-empty-arguments-to-sudo-i/27892867#27892867
            "/bin/bash", "-ec",
            f"ssh-keygen -b 2048 -t rsa -C {comment} -f {path} -N ''",
        ])
        self.shell(self._supg + ["touch", ".ssh/authorized_keys"])
        self.shell(self._supg + ["chmod", "0600", ".ssh/authorized_keys"])

        return self.shell(self._supg + ['cat', '.ssh/id_rsa.pub']).strip()

    def ssh_copy_id(self, target_url):
        target_url = urlparse(target_url)
        destination = f"{target_url.username}@{target_url.hostname}"
        logger.info('Authorize postgres on %s.', destination)
        args = ["-p", str(target_url.port or 22), destination]
        self.shell([
            "ssh-copy-id",
            "-i", "/var/lib/pgsql/.ssh/id_rsa",
            "-o", 'StrictHostKeyChecking=no',
            *args,
        ], ssh_options=["-A"])

        # Check SSH access.
        self.shell(self._supg + [
            "ssh", *args,
            # Save host key as user.
            "-o", 'StrictHostKeyChecking=no',
            "true",
        ])

    def wait(self):
        wait_machine(self.data['admin_ip'], port=22)

    def zoned_config(self, prefix):
        # Returns Flask config value depending on instance availability zone.
        return zoned_config(self.zone, prefix)


class MachineCork:
    # Machine object without DBInstance. Useful for testing and recovery when
    # cornac database is down.

    def __init__(self, identifier, account_id=1, zone=None):
        self.identifier = identifier
        self.tenant = make_tenant_hash(account_id)
        self.zone = zone or current_app.config['REGION'] + 'a'

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self)

    def __str__(self):
        return self.hostname

    @property
    def ident(self):
        return dict(
            identifier=self.identifier,
            prefix=current_app.config['MACHINE_PREFIX'],
            tenant=self.tenant,
            region=current_app.config['REGION'],
            zone=self.zone,
            z=self.zone[-1],
        )

    @property
    def hostname(self):
        return Machine._hostname_fmt.format(**self.ident)
