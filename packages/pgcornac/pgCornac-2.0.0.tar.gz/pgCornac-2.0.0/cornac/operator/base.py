import logging
import re
from pkg_resources import iter_entry_points

from ..core import list_availability_zones
from ..errors import KnownError
from ..ssh import RemoteShell
from .machine import Machine

logger = logging.getLogger(__name__)


class Operator(object):
    RESERVED_ROLES = ['postgres', 'rdsadmin']

    _supg = ["sudo", "-iu", "postgres"]

    @staticmethod
    def factory(iaas, config):
        name = config['OPERATOR']
        try:
            ep, *_ = iter_entry_points('cornac.operators', name=name)
        except ValueError:
            raise KnownError(f"Unknown operator type {name}")

        cls = ep.load()
        return cls(iaas, config)

    def __init__(self, iaas, config):
        self.iaas = iaas
        self.config = config

    def delete_db_instance(self, instance):
        self.iaas.delete_machine(self.machine(instance))

    def is_running(self, instance):
        return self.machine(instance).is_running()

    def maintainance(self, instance):
        pass

    def reboot_db_instance(self, instance, force_failover=False):
        self.stop_db_instance(instance)
        self.start_db_instance(instance)

    def recovery_end(self, instance):
        pass

    def start_db_instance(self, instance):
        for machine in self.machines(instance):
            self.iaas.start_machine(machine)
        for machine in self.machines(instance):
            machine.wait()
            logger.debug("Machine %s is up.", machine)

    def stop_db_instance(self, instance):
        for machine in self.machines(instance):
            self.iaas.stop_machine(machine)
            logger.debug("Machine %s is down.", machine)

    def create_machine(self, machine):
        if not machine.instance.operator_data:
            machine.instance.operator_data = dict()
        machine.instance.operator_data.setdefault('machines', dict())

        self.iaas.create_machine(
            machine,
            data_size_gb=machine.instance.data['AllocatedStorage'],
        )
        machine.data['admin_ip'] = self.iaas.endpoint(machine)
        self.iaas.start_machine(machine)

    def reboot_machine(self, machine):
        self.iaas.stop_machine(machine)
        self.iaas.start_machine(machine)
        machine.wait()

    def teardown_ssh_for_backup(self, comment, backup_url):
        pattern = re.sub(r'[ /+]', '.', comment)
        shell = RemoteShell.from_url(backup_url)
        shell(['sed', '-i', f"/ {pattern}$/d", ".ssh/authorized_keys"])

    def machine(self, instance, zone=None) -> Machine:
        # Helps subclasses to instanciate custom machine object.
        return Machine(instance, zone)

    def machines(self, instance):
        if instance.data['MultiAZ']:
            zones = list_availability_zones()
        else:
            zones = [instance.data['AvailabilityZone']]
        for zone in zones:
            yield self.machine(instance, zone=zone)
