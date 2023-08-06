# Apply actions on infrastructure.
#
# The concept of Operator is borrowed from K8S.
#

import logging
from pathlib import Path

from .. import worker
from ..ssh import Password
from ..utils import pwgen
from .base import Operator


logger = logging.getLogger(__name__)


class BasicOperator(Operator):
    # Implementation using pghelper.sh

    helper = '/usr/local/bin/pghelper.sh'

    def create_db_instance(self, instance):
        machine = self.machine(instance)
        self.create_machine(machine)
        machine.shell.wait()
        logger.debug("Sending helper script.")
        local_helper = str(Path(__file__).parent / 'pghelper.sh')
        machine.shell.copy(local_helper, self.helper)

        # Formatting disk
        try:
            # Check whether Postgres VG is configured.
            machine.shell(["test", "-d", "/dev/Postgres"])
        except Exception:
            dev = self.iaas.guess_data_device_in_guest(machine)
            logger.info("Preparing disk %s.", dev)
            machine.shell([self.helper, "prepare-disk", dev])
            logger.info("Creating Postgres instance.")
            machine.shell([
                self.helper, "create-instance",
                instance.data['EngineVersion'],
                instance.data['DBInstanceIdentifier'],
            ])
            machine.shell([self.helper, "start"])
        else:
            logger.info("Reusing Postgres instance.")

        # Master user
        master = instance.data['MasterUsername']
        machine.shell([
            self.helper,
            "create-masteruser", master,
            Password(instance.data['MasterUserPassword']),
        ])

        # Creating database
        dbname = master
        bases = machine.shell([self.helper, "psql", "-l"])
        if f"\n {dbname} " in bases:
            logger.info("Reusing database %s.", dbname)
        else:
            logger.info("Creating database %s.", dbname)
            machine.shell([self.helper, "create-database", dbname, master])

        instance.data['Endpoint'] = dict(
            Address=machine.data['admin_ip'], Port=5432)

    def create_db_snapshot(self, instance, snapshot):
        logger.warn("Snapshot not implemented.")

    def delete_db_snapshot(self, snapshot):
        logger.warn("Snapshot not implemented.")

    def restore_db_instance_from_db_snapshot(self, instance, snapshot):
        logger.warn("Snapshot not implemented.")
        instance.data['MasterUserPassword'] = pw = pwgen(8)
        logger.warn("Creating new instance with master password: '%s'.", pw)
        self.create_db_instance(instance)
        worker.recovery_end.send(instance.id)

    def restore_db_instance_to_point_in_time(self, target, source,
                                             restore_time):
        self.restore_db_instance_from_db_snapshot(target, None)

    def is_running(self, instance):
        # Check whether *Postgres* is running.
        machine = self.machine(instance)
        if not self.iaas.is_running(machine):
            return False

        try:
            machine.shell([self.helper, "psql", "-l"])
            return True
        except Exception as e:
            logger.debug("Failed to query Postgres %s: %s", instance, e)
            raise Exception('VM is running but not Postgres.') from None

        return False
