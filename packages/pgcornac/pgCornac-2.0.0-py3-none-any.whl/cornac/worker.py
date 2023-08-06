import functools
import logging
import os
import pdb
import sys
from contextlib import contextmanager

from flask import current_app, g
from flask_dramatiq import Dramatiq

from .core.config import require_ssh_key
from .core.model import DBInstance, DBSnapshot, db
from .errors import KnownError
from .iaas import IaaS
from .operator import Operator


dramatiq = Dramatiq()
logger = logging.getLogger(__name__)


class TaskStop(Exception):
    # Exception raised to return task, from anywhere in the stack. e.g. the
    # task is now irrelevant.
    pass


def actor(**kw):
    # Declare and wraps a background task function.

    def decorator(fn):
        @dramatiq.actor(**kw)
        @functools.wraps(fn)
        def actor_wrapper(*a, **actor_kw):
            try:
                return fn(*a, **actor_kw)
            except TaskStop as e:
                logger.info("%s", e)
            except KnownError as e:
                logger.error("Task failed: %s", e)
            except Exception:
                logger.exception("Unhandled error in task:")
                debug = os.environ.get('DEBUG', '').lower() in ('1', 'y')
                if debug and sys.stdout.isatty():
                    logger.debug("Dropping in debugger.")
                    pdb.post_mortem(sys.exc_info()[2])
                else:
                    logger.error(
                        "Please report at "
                        "https://github.com/dalibo/cornac/issues/new"
                        " with full log.",
                    )

            # Swallow errors so that Dramatiq don't retry task. We want
            # Dramatiq to retry task only on SIGKILL.

        return actor_wrapper

    return decorator


def get_instance(instance, message="Working on %s."):
    if isinstance(instance, int):
        instance_id = instance
        instance = DBInstance.query.get(instance_id)
        if not instance:
            raise TaskStop(f"Unknown instance #{instance_id}.")
    if message:
        logger.info(message, instance)
    g.current_account = instance.account
    return instance


def get_snapshot(snapshot, message="Working on %s."):
    if isinstance(snapshot, int):
        snapshot_id = snapshot
        snapshot = DBSnapshot.query.get(snapshot_id)
        if not snapshot:
            raise TaskStop(f"Unknown snapshot #{snapshot_id}.")
    if message:
        logger.info(message, snapshot)
    g.current_account = snapshot.account
    return snapshot


@contextmanager
def operator_manager():
    config = current_app.config
    with IaaS.connect(config['IAAS'], config) as iaas:
        yield Operator.factory(iaas, current_app.config)


@contextmanager
def state_manager(obj, from_=None, to='available', onerror='failed'):
    # Manage the state of an instance, when working with a single instance.
    # Checks if instance status matches from_. On success, instance status is
    # defined as to. On error, the instance state is set to failed. SQLAlchemy
    # db session is always committed.

    if from_ and from_ != obj.status:
        raise KnownError(f"{obj} is not in state {from_}.")

    try:
        yield obj
    except TaskStop:
        # Don't touch object.
        pass
    except Exception as e:
        obj.status = onerror
        obj.status_message = str(e)
        raise
    else:
        if to:
            obj.status = to
            obj.status_message = None
    finally:
        db.session.commit()


@actor()
def create_db_instance(instance_id):
    require_ssh_key()
    with state_manager(get_instance(instance_id), 'creating') as instance:
        instance.data['XDBInstanceId'] = instance.id
        with operator_manager() as operator:
            operator.create_db_instance(instance)
        instance.data.pop('MasterUserPassword')

    if current_app.has_snapshots:  # Create initial snapshot.
        snapshot = DBSnapshot.factory(instance, 'automated')
        db.session.add(snapshot)
        db.session.commit()
        logger.info("Enqueue creation of initial %s.", snapshot)
        create_db_snapshot.send(snapshot.id)

    logger.info("%s.", instance)


@actor(queue_name='snapshots')
def create_db_snapshot(snapshot_id):
    snapshot = get_snapshot(snapshot_id, message="Creating %s.")
    with state_manager(snapshot, from_='creating'):
        instance = get_instance(
            snapshot.data['XDBInstanceId'],
            message="Snapshoting %s.")
        # Snapshoting properties.
        keys = {
            'AllocatedStorage', 'InstanceCreateTime', 'MasterUsername',
            'EngineVersion',
        }
        for k in keys:
            snapshot.data[k] = instance.data[k]

        with operator_manager() as operator:
            instance.status = 'backing-up'
            db.session.commit()
            # On snapshot error, keep instance available.
            with state_manager(instance, onerror='available'):
                operator.create_db_snapshot(instance, snapshot)
        snapshot.data['PercentProgress'] = 100
    logger.info("Saved %s.", snapshot)


@actor()
def delete_db_instance(
        instance_id, snapshot_id=None, delete_automated_snapshots=True):
    instance = get_instance(instance_id, message="Deleting %s.")
    with state_manager(instance, from_='deleting'):
        if snapshot_id:  # Create final snapshot.
            snapshot = get_snapshot(snapshot_id, "Creating final %s...")
            # Create snapshot immediately before dropping instance!
            create_db_snapshot(snapshot.id)
            if 'available' != snapshot.status:
                logger.warning("Failed to create final snapshot. Stopping.")
                return

        else:
            logger.info("Skipping final snapshot.")

        with operator_manager() as operator:
            operator.delete_db_instance(instance)

        if delete_automated_snapshots:
            to_delete = []
            for snapshot in instance.snapshots:
                if snapshot.type_ == 'automated':
                    snapshot.status = 'deleted'
                    to_delete.append(snapshot)
            db.session.commit()

            for snapshot in to_delete:
                logger.info("Queuing deletion of %s.", snapshot)
                delete_db_snapshot.send(snapshot.id)

        db.session.delete(instance)
    logger.info("Deleted %s.", instance)


@actor()
def delete_db_snapshot(snapshot_id):
    snapshot = get_snapshot(snapshot_id, message="Deleting %s.")
    with state_manager(snapshot, 'deleted', to='deleted'):
        with operator_manager() as operator:
            operator.delete_db_snapshot(snapshot)
        db.session.delete(snapshot)
    logger.info("Deleted %s.", snapshot)


@actor()
def inspect_instance(instance_id):
    require_ssh_key()
    instance = get_instance(instance_id)
    with operator_manager() as operator:
        try:
            if operator.is_running(instance):
                instance.status = 'available'
                instance.status_message = None
            else:
                instance.status = 'stopped'
                instance.status_message = None
        except Exception as e:
            instance.status = 'failed'
            instance.status_message = str(e)
    db.session.commit()
    logger.info("%s inspected.", instance)


@actor(queue_name='maintenance')
def maintainance(async_=True):
    logger.info("Starting maintainance task.")
    callable_ = maintain_instance.send if async_ else maintain_instance
    qry = DBInstance.query.filter(DBInstance.status == 'available')
    for instance in qry:
        callable_(instance.id)


@actor(queue_name='maintenance')
def maintain_instance(instance_id):
    instance = get_instance(instance_id)
    with operator_manager() as operator:
        operator.maintainance(instance)
    db.session.commit()
    logger.info("Maintainance done on %s.", instance)


@actor()
def reboot_db_instance(instance_id, force_failover=False):
    instance = get_instance(instance_id, message="Rebooting %s.")
    with state_manager(get_instance(instance_id)) as instance:
        with operator_manager() as operator:
            operator.reboot_db_instance(instance, force_failover)
    logger.info("Rebooted %s.", instance)


@actor()
def recovery_end(instance_id):
    instance = get_instance(instance_id)
    with state_manager(instance, from_='creating'):
        with operator_manager() as operator:
            operator.recovery_end(instance)
    logger.info("%s restored.", instance)

    snapshot = DBSnapshot.factory(instance, 'automated')
    db.session.add(snapshot)
    db.session.commit()
    create_db_snapshot.send(snapshot.id)


_restore_state_kw = dict(from_='creating', to=None, onerror='restore-error')


@actor(queue_name='snapshots')
def restore_db_instance_from_db_snapshot(
        instance_id, snapshot_id, recovery_end_callback):
    snapshot = get_snapshot(snapshot_id, message=None)
    instance = get_instance(instance_id, f"Restoring %s from {snapshot}.")
    instance.recovery_end_callback = recovery_end_callback

    with state_manager(instance, **_restore_state_kw):
        with operator_manager() as operator:
            operator.restore_db_instance_from_db_snapshot(instance, snapshot)
    logger.info("Started restoration of %s from %s.", instance, snapshot)


@actor(queue_name='snapshots')
def restore_db_instance_to_point_in_time(
        target_id, source_id, restore_time, recovery_end_callback):
    source = get_instance(source_id, message=None)
    restore_time_str = restore_time or 'latest restorable time'
    target = get_instance(
        target_id, f"Restoring {source} at {restore_time_str} in %s")
    target.recovery_end_callback = recovery_end_callback

    with state_manager(target, **_restore_state_kw):
        with operator_manager() as operator:
            operator.restore_db_instance_to_point_in_time(
                target, source, restore_time)
    logger.info(
        "Started restoration of %s from %s at %s.",
        target, source, restore_time_str)


@actor()
def recover_instances():
    instances = (
        DBInstance.query
        .filter(DBInstance.status.in_(('available', 'stopped')))
        .filter(DBInstance.identifier != 'cornac')
    )
    for instance in instances:
        logger.info("Ensuring %s is %s.", instance.identifier, instance.status)
        if instance.status == 'available':
            start_db_instance.send(instance.id)
        elif instance.status == 'stopped':
            stop_db_instance.send(instance.id)


@actor()
def start_db_instance(instance_id):
    instance = get_instance(instance_id, message="Starting %s.")
    with state_manager(instance):
        with operator_manager() as operator:
            operator.start_db_instance(instance)
    logger.info("Started %s.", instance)


@actor()
def stop_db_instance(instance_id, snapshot_id=None):
    instance = get_instance(instance_id, message="Stopping %s.")
    with state_manager(instance, to='stopped'):
        if snapshot_id:
            snapshot = get_snapshot(snapshot_id, "Creating %s...")
            # Create snapshot immediately before stopping instance!
            create_db_snapshot(snapshot.id)

        with operator_manager() as operator:
            operator.stop_db_instance(instance)
    logger.info("Stopped %s.", instance)
