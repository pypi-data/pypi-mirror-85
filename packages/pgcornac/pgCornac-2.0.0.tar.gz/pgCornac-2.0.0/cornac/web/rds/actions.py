# RDS-like service.
#
# Each method corresponds to a well-known RDS action, returning result as
# XML snippet.

import functools
import inspect
import logging
from itertools import product
from uuid import uuid4

from flask import current_app, g
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError

from . import (
    errors,
    xml,
)
from ...core import list_availability_zones
from ...core.instanceclass import DBInstanceClass
from ..auth import check as check_acl
from cornac import worker
from cornac.core.model import DBInstance, DBSnapshot, db
from cornac.operator import Operator
from cornac.utils import heredoc, validate_password_strength


logger = logging.getLogger(__name__)


def get_instance(identifier, status=None):
    try:
        instance = (
            DBInstance.query.current()
            .filter(DBInstance.identifier == identifier)
            .one())
    except NoResultFound:
        raise errors.DBInstanceNotFound(identifier)
    check_status(instance, status)
    check_acl(resource=instance)
    return instance


def get_snapshot(identifier, status=None):
    try:
        snapshot = (
            DBSnapshot.query.current()
            .filter(DBSnapshot.identifier == identifier)
            .one())
    except NoResultFound:
        raise errors.DBSnapshotNotFound(identifier)
    check_status(snapshot, status)
    check_acl(resource=snapshot)
    return snapshot


def known_args(*args):
    # Decorator to filter request args.

    def decorator(f):
        # Append parameters from signature too.
        sig = inspect.signature(f, follow_wrapped=True)
        command = f.__name__
        callable_args = set(a for a in sig.parameters if a[0].isupper())

        @functools.wraps(f)
        def wrapper(*a, **kw):
            ignored_args = set(kw) - set(args) - callable_args
            if ignored_args:
                logger.debug(
                    "Ignoring %s args %s.",
                    command, ', '.join(ignored_args))
                for arg in ignored_args:
                    kw.pop(arg)
            return f(*a, **kw)
        return wrapper
    return decorator


def check_create_command(command):
    command['AllocatedStorage'] = int(command['AllocatedStorage'])
    command['PerformanceInsightsEnabled'] = command.get(
        'EnablePerformanceInsights', 'false') == 'true'
    command['MultiAZ'] = command.get('MultiAZ', 'false') == 'true'

    if command['MultiAZ']:
        if 'AvailabilityZone' in command:
            raise errors.InvalidParameterCombination(
                "Requesting a specific availability zone is not valid"
                " for Multi-AZ instances."
            )
    else:
        zones = list_availability_zones()
        zone = command.setdefault('AvailabilityZone', zones[0])
        if zone not in zones:
            raise errors.InvalidParameterValue(
                f"{zone} is not a valid availability zone")

    if command['MasterUsername'] in Operator.RESERVED_ROLES:
        raise errors.InvalidParameterValue(
            f"MasterUsername {command['MasterUsername']} cannot be used as it "
            "is a reserved word used by the engine")

    try:
        validate_password_strength(command['MasterUserPassword'])
    except ValueError as e:
        raise errors.InvalidParameterValue(f"Bad master user password: {e}")

    check_instance_class(command['DBInstanceClass'])

    return command


def check_instance_class(value):
    try:
        DBInstanceClass.parse(value)
    except ValueError as e:
        logger.debug("Invalid DBInstanceClass: %s.", e)
        raise errors.InvalidParameterValue(
            f"Invalid DB Instance class: {value}")


@known_args(
    'AllocatedStorage',
    'AvailabilityZone',
    'DBInstanceClass',
    'DBInstanceIdentifier',
    'Engine',
    'EngineVersion',
    'MasterUserPassword',
    'MasterUsername',
    'MultiAZ',
    'EnablePerformanceInsights',
)
def CreateDBInstance(**command):
    check_acl()
    command = check_create_command(command)

    identifier = check_instance_identifier(command['DBInstanceIdentifier'])
    instance = DBInstance.factory(identifier)
    instance.data.update(command)
    db.session.add(instance)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        logger.debug("Integrity error for new DBInstance:", exc_info=True)
        raise errors.DBInstanceAlreadyExists() from None

    worker.create_db_instance.send(instance.id)

    return xml.InstanceEncoder(instance).as_xml()


def CreateDBSnapshot(*, DBInstanceIdentifier, DBSnapshotIdentifier, **__):
    instance = get_instance(DBInstanceIdentifier)
    check_status(instance, msg=heredoc(f"""\
    Cannot create a snapshot because the database instance
    {DBInstanceIdentifier} is not currently in the available state.
    """))

    identifier = check_snapshot_identifier(DBSnapshotIdentifier)
    snapshot = DBSnapshot.factory(instance, 'manual', identifier)

    db.session.add(snapshot)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise errors.DBSnapshotAlreadyExists(identifier=snapshot.identifier) \
            from None

    worker.create_db_snapshot.send(snapshot.id)

    return xml.SnapshotEncoder(snapshot).as_xml()


def DeleteDBInstance(*, DBInstanceIdentifier, **command):
    skip_snapshot = command.get('SkipFinalSnapshot') == 'true'
    delete_autobackups = command.get('DeleteAutomatedBackups', 'true')
    delete_autobackups = delete_autobackups == 'true'
    snapshot_identifier = command.get('FinalDBSnapshotIdentifier')
    if not current_app.has_snapshots:
        skip_snapshot = True

    instance = get_instance(DBInstanceIdentifier)

    if 'creating' == instance.status and not skip_snapshot:
        raise errors.InvalidDBInstanceState(
            f"Instance {DBInstanceIdentifier} is currently creating "
            "- a final snapshot cannot be taken.")

    if not snapshot_identifier and not skip_snapshot:
        raise errors.InvalidParameterCombination(
            "FinalDBSnapshotIdentifier is required unless SkipFinalSnapshot "
            "is specified.")

    if instance.data.get('DeletionProtection', False):
        raise errors.InvalidParameterCombination(
            "Cannot delete protected DB Instance, please disable deletion "
            "protection and try again.")

    snapshot_id = None
    if not skip_snapshot:
        snapshot = DBSnapshot.factory(
            instance, 'manual', snapshot_identifier)
        db.session.add(snapshot)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise errors.DBSnapshotAlreadyExists(snapshot_identifier) from None
        snapshot_id = snapshot.id
    instance.status = 'deleting'
    db.session.commit()

    worker.delete_db_instance.send(
        instance.id, snapshot_id, delete_autobackups,
    )

    return xml.InstanceEncoder(instance).as_xml()


def DeleteDBSnapshot(*, DBSnapshotIdentifier, **command):
    snapshot = get_snapshot(DBSnapshotIdentifier)
    if snapshot.status not in ('available', 'failed'):
        raise errors.InvalidDBSnapshotState(
            "Cannot delete the snapshot because it is not currently in the "
            "available or failed state.",
        )

    snapshot.status = 'deleted'
    worker.delete_db_snapshot.send(snapshot.id)
    db.session.commit()
    return xml.SnapshotEncoder(snapshot).as_xml()


def DescribeDBInstances(**command):
    check_acl(resource=g.current_account.build_arn(resource='db:*'))
    qry = DBInstance.query.current()
    if 'DBInstanceIdentifier' in command:
        qry = qry.filter(
            DBInstance.identifier == command['DBInstanceIdentifier'])
    instances = qry.order_by(DBInstance.identifier).all()
    return xml.INSTANCE_LIST_TMPL.render(
        instances=[xml.InstanceEncoder(i) for i in instances])


def DescribeDBSnapshots(**command):
    check_acl(resource=g.current_account.build_arn(resource='snapshots:*'))
    qry = DBSnapshot.query.current()
    if 'DBSnapshotIdentifier' in command:
        qry = qry.filter(
            DBSnapshot.identifier == command['DBSnapshotIdentifier'])
    if 'DBInstanceIdentifier' in command:
        needle = dict(DBInstanceIdentifier=command['DBInstanceIdentifier'])
        qry = qry.filter(
            DBSnapshot.data.contains(needle)
        )
    snapshots = qry.order_by(DBSnapshot.identifier).all()
    return xml.SNAPSHOT_LIST_TMPL.render(
        snapshots=[xml.SnapshotEncoder(s) for s in snapshots])


def DescribeOrderableDBInstanceOptions(Engine, **command):
    check_acl()

    if Engine != 'postgres':
        raise errors.InvalidParameterValue("Invalid DB engine")

    default = dict(
        SupportsPerformanceInsights=current_app.has_temboard,
        AvailabilityZones=list_availability_zones(),
        # Same default as AWS RDS.
        DBInstanceClass='db.t2.micro',
    )
    versions = ['12', '11', '10', '9.6', '9.5']
    classes = current_app.config['INSTANCE_CLASSES']

    combinations = product(versions, classes)
    options_list = [
        dict(default, EngineVersion=v, DBInstanceClass=c)
        for v, c in combinations
    ]
    return xml.ORDERABLE_DB_INSTANCE_OPTIONS_LIST_TMPL.render(options_list=[
        xml.OrderableDBInstanceOptions(**options)
        for options in options_list
    ])


def RebootDBInstance(*, DBInstanceIdentifier, ForceFailover=False):
    instance = get_instance(DBInstanceIdentifier)
    instance.status = 'rebooting'
    db.session.commit()
    worker.reboot_db_instance.send(instance.id, ForceFailover)
    return xml.InstanceEncoder(instance).as_xml()


@known_args(
    'AvailabilityZone',
    'DBInstanceClass',
    'DBInstanceIdentifier',
    'DBSnapshotIdentifier',
    'Engine',
    'MultiAZ',
)
def RestoreDBInstanceFromDBSnapshot(**command):
    snapshot = get_snapshot(
        command['DBSnapshotIdentifier'], status='available')
    identifier = check_instance_identifier(command['DBInstanceIdentifier'])
    instance = DBInstance.factory(identifier, extra=snapshot.data)
    instance.data.update(command)
    instance.recovery_token = str(uuid4())
    recovery_end_callback = instance.recovery_end_callback

    db.session.add(instance)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise errors.DBInstanceAlreadyExists() from None

    worker.restore_db_instance_from_db_snapshot.send(
        instance.id, snapshot.id,
        recovery_end_callback=recovery_end_callback,
    )

    return xml.InstanceEncoder(instance).as_xml()


@known_args(
    'AvailabilityZone',
    'DBInstanceClass',
    'MultiAZ',
)
def RestoreDBInstanceToPointInTime(
        *, SourceDBInstanceIdentifier, TargetDBInstanceIdentifier,
        RestoreTime=None, UseLatestRestorableTime='false', **command):
    source = get_instance(SourceDBInstanceIdentifier)

    UseLatestRestorableTime = UseLatestRestorableTime == 'true'
    if UseLatestRestorableTime:
        RestoreTime = None
    elif RestoreTime is None:
        raise errors.InvalidParameterCombination(
            "If UseLatestRestoreTime is not true, "
            "the RestoreTime parameter must be specified."
        )

    data = dict(source.data, **command)
    del data['DBInstanceIdentifier']
    del data['DeletionProtection']
    identifier = check_instance_identifier(TargetDBInstanceIdentifier)
    target = DBInstance.factory(identifier, extra=data)
    target.recovery_token = str(uuid4())
    recovery_end_callback = target.recovery_end_callback
    source.data.pop('Endpoint', 'ignore-missing')

    db.session.add(target)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise errors.DBInstanceAlreadyExists() from None

    worker.restore_db_instance_to_point_in_time.send(
        target.id, source.id, RestoreTime,
        recovery_end_callback=recovery_end_callback,
    )

    return xml.InstanceEncoder(target).as_xml()


def StartDBInstance(*, DBInstanceIdentifier):
    instance = get_instance(DBInstanceIdentifier, status='stopped')
    instance.status = 'starting'
    db.session.commit()
    worker.start_db_instance.send(instance.id)
    return xml.InstanceEncoder(instance).as_xml()


def StopDBInstance(DBInstanceIdentifier, DBSnapshotIdentifier=None):
    instance = get_instance(DBInstanceIdentifier, status='available')
    snapshot_id = None
    if DBSnapshotIdentifier:
        snapshot = DBSnapshot.factory(
            instance, 'manual', DBSnapshotIdentifier)
        db.session.add(snapshot)
        try:
            db.session.flush()
        except IntegrityError:
            db.session.rollback()
            raise errors.DBSnapshotAlreadyExists(DBSnapshotIdentifier) \
                from None
        snapshot_id = snapshot.id
    instance.status = 'stopping'
    db.session.commit()
    worker.stop_db_instance.send(instance.id, snapshot_id)
    return xml.InstanceEncoder(instance).as_xml()


def check_instance_identifier(identifier, attr='DBInstanceIdentifier'):
    try:
        return DBInstance.check_identifier(identifier)
    except ValueError:
        raise errors.InvalidParameterValue(heredoc(f"""\
        The parameter {attr} is not a valid identifier.
        Identifiers must begin with a letter; must contain only ASCII letters,
        digits, and hyphens; and must not end with a hyphen or contain two
        consecutive hyphens.
        """))


def check_snapshot_identifier(identifier):
    return check_instance_identifier(identifier, attr='DBSnapshotIdentifier')


def check_status(obj, status='available', msg=None):
    if status is None:
        return
    if isinstance(status, str):
        status = status,
    if obj.status not in status:
        cls = getattr(errors, f"Invalid{obj.__class__.__name__}State")
        if msg is None:
            msg = (
                f"{obj.__class__.__name__} must have state {status} but "
                f"actually has {obj.status}"
            )
        raise cls(msg)
