import logging
import re
from itertools import product

from flask import g
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from psycopg2.errors import UniqueViolation

from . import xml
from . import errors
from .. import errors as common_errors
from ..auth import check
from cornac.core.model import AccessKey, Identity, db
from cornac.utils import heredoc


logger = logging.getLogger(__name__)


#       A C C E S S   K E Y

def CreateAccessKey(UserName=None, **_):
    user = get_user(UserName, default=g.current_identity)

    quota = 2
    total = AccessKey.query.filter_by(identity=user).count()
    if total >= quota:
        raise errors.LimitExceeded(
            f"Cannot exceed quota for AccessKeysPerUser: {quota}")

    access_key = AccessKey.factory(identity=user)

    db.session.add(access_key)
    db.session.commit()

    return xml.AccessKeyEncoder(access_key).as_xml(with_secret=True)


def DeleteAccessKey(AccessKeyId, UserName=None, **_):
    access_key = get_access_key(UserName, AccessKeyId)
    db.session.delete(access_key)
    db.session.commit()


def ListAccessKeys(UserName=None, **_):
    user = get_user(UserName, default=g.current_identity)
    access_keys = AccessKey.query.filter_by(identity=user, edate=None).all()
    return xml.AccessKeysListEncoder(access_keys).as_xml()


def UpdateAccessKey(AccessKeyId, Status, UserName=None):
    if Status not in ['Active', 'Inactive']:
        raise errors.ValidationError(heredoc(
            f"Value '{Status}' at 'status' failed to satisfy constraint: "
            "Member must satisfy enum value set: [Active, Inactive]"
        ))
    access_key = get_access_key(UserName, AccessKeyId)
    access_key.status = Status
    db.session.add(access_key)
    db.session.commit()


def get_access_key(UserName, AccessKeyId):
    if UserName is None:
        user = g.current_identity
        qry = AccessKey.query.filter_by(identity=user)
    else:
        qry = AccessKey.query.with_user(UserName)

    try:
        access_key = qry.get(AccessKeyId)
    except NoResultFound:
        raise errors.NoSuchEntity(
            f"The Access Key with id {AccessKeyId} cannot be found.")

    check(resource=access_key.identity)

    return access_key


#       G R O U P S

def AddUserToGroup(UserName, GroupName, **_):
    user = get_user(UserName)
    group = get_group(GroupName)
    logger.info("Adding %s to %s.", user, group)
    user.groups.append(group)
    db.session.commit()


def GetGroup(GroupName, **_):
    group = get_group(GroupName)
    return xml.UserListEncoder(users=group.members).as_xml()


def ListGroups():
    check()
    groups = Identity.query.groups().order_by(Identity.name)
    return xml.GroupListEncoder(groups=groups.all()).as_xml()


def ListGroupsForUser(UserName, **_):
    user = get_user(UserName)
    return xml.GroupListEncoder(groups=user.groups).as_xml()


def RemoveUserFromGroup(UserName, GroupName, **_):
    user = get_user(UserName)
    group = get_group(GroupName)
    if user is g.current_identity and group.is_admins:
        raise errors.InvalidParameterCombination(
            f"Refusing to remove yourself from {group}."
        )

    logger.info("Removing %s from %s.", user, group)
    try:
        user.groups.remove(group)
    except ValueError as e:
        logger.info("%s already removed from %s: %s.", user, group, e)
    else:
        db.session.commit()


#       L O G I N   P R O F I L E

def ChangePassword(OldPassword, NewPassword, **_):
    user = g.current_identity
    check(resource=user)
    if not user.check_password(OldPassword):
        raise common_errors.AccessDenied(description=heredoc("""\
        Either the new password does not conform to the account password policy
        or the old password was incorrect.
        """))
    user.store_password(NewPassword)
    db.session.commit()


def CreateLoginProfile(UserName, Password, **_):
    user = get_user(UserName)
    if user.has_password:
        raise errors.EntityAlreadyExists(
            f"Login Profile for user {UserName} already exists.")

    user.store_password(Password)
    db.session.add(user)
    db.session.commit()

    return xml.LoginProfileEncoder(user=user).as_xml()


def DeleteLoginProfile(UserName):
    user = get_user(UserName, with_password=True)
    user.drop_password()
    db.session.add(user)
    db.session.commit()


def GetLoginProfile(UserName):
    user = get_user(UserName, with_password=True)
    return xml.LoginProfileEncoder(user).as_xml()


def UpdateLoginProfile(UserName, Password, *_):
    user = get_user(UserName, with_password=True)
    user.store_password(Password)
    db.session.add(user)
    db.session.commit()


#       U S E R

_username_re = re.compile(r'[a-z0-9+._-]+@[a-z0-9+._-]+')


def CreateUser(UserName):
    check()

    if not _username_re.match(UserName):
        raise errors.ValidationError(heredoc("""\
        The specified value for userName is invalid.
        It must contain only alphanumeric characters
        and/or the following: +=,.@_-
        """))

    user = Identity.user_factory(UserName)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as e:
        if isinstance(e.orig, UniqueViolation):
            raise errors.EntityAlreadyExists(
                f"User with name {UserName} already exists.") from None
        else:
            raise

    return xml.UserEncoder(user).as_xml()


def DeleteUser(UserName):
    db.session.delete(get_user(UserName))
    db.session.commit()


def GetUser(UserName):
    user = get_user(UserName)
    return xml.UserEncoder(user).as_xml()


def ListUsers():
    check()
    users = Identity.query.users().order_by(Identity.name).all()
    return xml.UserListEncoder(users=users).as_xml()


def UpdateUser(UserName, NewUserName=None, **kw):
    user = get_user(UserName)

    if NewUserName:
        if not _username_re.match(NewUserName):
            raise errors.ValidationError(heredoc("""\
            The specified value for newUserName is invalid.
            It must contain only alphanumeric characters
            and/or the following: +=,.@_-
            """))
        user.rename_to(NewUserName)
        db.session.commit()


def SimulatePrincipalPolicy(
        PolicySourceArn, ActionNames=None, ResourceArns=None, **_):
    ActionNames = ActionNames or ['*']
    ResourceArns = ResourceArns or ['*']
    try:
        source = Identity.query.get_by(arn=PolicySourceArn)
    except NoResultFound:
        raise errors.NoSuchEntity("Unable to retrieve specified IAM entity")
    check(resource=PolicySourceArn)

    results = []
    for action, resource in product(ActionNames, ResourceArns):
        results.append(check(
            source=source,
            action=action,
            resource=resource,
            raise_=False,
        ))

    return xml.PolicyResultsEncoder(results).as_xml()


# Misc.

def get_group(name):
    try:
        group = Identity.query.groups().get_by(name=name)
    except NoResultFound:
        raise errors.NoSuchEntity(
            f"The group with name {name} cannot be found."
        )

    check(resource=group)

    return group


def get_user(name, with_password=False, default=None):
    if name is None and default:
        user = default
        name = default.name
    else:
        try:
            user = Identity.query.users().get_by(name=name)
        except NoResultFound:
            raise errors.NoSuchEntity(
                f"The user with name {name} cannot be found.")

        if with_password and not user.has_password:
            raise errors.NoSuchEntity(
                f"Login Profile for User {name} cannot be found.")

    check(resource=user)

    return user
