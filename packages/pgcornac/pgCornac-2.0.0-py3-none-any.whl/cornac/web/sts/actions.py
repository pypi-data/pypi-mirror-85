from flask import g
from sqlalchemy.orm.exc import NoResultFound

from . import xml
from .. import errors
from ..auth import check, no_check_required
from cornac.core.model import AccessKey, Identity, db


def AssumeRole(RoleArn, **_):
    check(resource=RoleArn)
    try:
        role = Identity.query.get_by(arn=RoleArn)
    except NoResultFound:
        raise errors.NoSuchEntity(f"Role {RoleArn} does not exists.")
    access = AccessKey.factory(identity=role, temporary=True)
    db.session.add(access)
    db.session.commit()
    return xml.CredentialsEncoder(access_key=access).as_xml()


def GetCallerIdentity():
    no_check_required()
    return xml.IdentityEncoder(g.current_identity).as_xml()
