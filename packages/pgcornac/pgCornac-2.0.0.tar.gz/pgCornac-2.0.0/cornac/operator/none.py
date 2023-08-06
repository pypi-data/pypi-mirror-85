#
# A None operator for test purpose.
#

import logging
from random import randint
from time import sleep

from .. import worker
from ..errors import KnownError
from ..utils import pwgen
from .base import Operator
from .machine import Machine


logger = logging.getLogger(__name__)


def randsleep(min_=1, max_=5):
    seconds = randint(min_, max_)
    if seconds:
        logger.debug("None operator sleeping %ss.", seconds)
        sleep(seconds)


class NoneOperator(Operator):
    def create_db_instance(self, instance, *_, **__):
        randsleep(5, 10)
        if 'errcreate' in instance.identifier:
            raise KnownError("Forged failure")

    def create_db_snapshot(self, instance, snapshot, *_, **__):
        randsleep()
        if 'errcreate' in snapshot.identifier:
            raise KnownError("Forged failure")
        machine = self.machine(instance, zone=Machine.auto_zone)
        instance.data['Endpoint'] = dict(Address=machine.fqdn, Port=5432)

    def delete_db_instance(self, instance, *_, **__):
        randsleep()
        if 'errdelete' in instance.identifier:
            raise KnownError("Forged failure")

    def delete_db_snapshot(self, snapshot, *_, **__):
        randsleep(1, 3)
        if 'errdelete' in snapshot.identifier:
            raise KnownError("Forged failure")

    def is_running(self, *_, **__):
        randsleep(0, 2)
        return True

    def restore_db_instance_from_db_snapshot(self, instance, snapshot):
        randsleep(5, 15)
        instance.data['MasterUserPassword'] = pwgen(8)
        worker.recovery_end.send(instance.id)
        if 'errcreate' in instance.identifier:
            raise KnownError("Forged failure")

    def restore_db_instance_to_point_in_time(self, target, source,
                                             restore_time):
        self.restore_db_instance_from_db_snapshot(target, None)

    def start_db_instance(self, instance, *_, **__):
        randsleep()
        if 'errstart' in instance.identifier:
            raise KnownError("Forged failure")

    def stop_db_instance(self, instance, *_, **__):
        randsleep()
        if 'errstop' in instance.identifier:
            raise KnownError("Forged failure")
