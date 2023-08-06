import logging

from flask import request, current_app
from sqlalchemy.exc import IntegrityError

from .auth import login_required
from .blueprint import blueprint, get_account
from .. import errors
from ..auth import (
    check, check_access_to_rds,
)
from ..utils import jsonify
from ...core.model import db, Account, ACL, Identity


logger = logging.getLogger(__name__)


@blueprint.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
    check()
    if 'GET' == request.method:
        accounts = [
            a.as_dict()
            for a in Account.query.all() if
            check_access_to_rds(a)
        ]
        return jsonify(accounts=accounts)
    elif 'POST' == request.method:
        data = request.json or request.form
        if 'Alias' not in data:
            return jsonify(400, message='Missing Alias.')
        account = Account()
        account.alias = data['Alias']
        account.data = dict(
            AdminGroupName=f'DBA-{account.alias}',
        )
        db.session.add(account)
        db.session.flush()  # Get account id.
        dbas = Identity.group_factory(account.data['AdminGroupName'])
        db.session.add(dbas)
        role = Identity.role_factory('CornacExternalDBAs', account)
        db.session.add(role)
        account.data['AdminRoleArn'] = role.arn

        try:
            db.session.flush()
        except IntegrityError:
            return jsonify(400, message="Account alias already used.")

        # Hard code AmazonRDSFullAccess policy on role.
        ACL.allow(source=role, action='rds:*', resource='*')
        # Hard code allow DBA members to assume role on target account.
        ACL.allow(source=dbas, action='sts:AssumeRole', resource=role.arn)

        db.session.commit()

        return jsonify(account=account.as_dict())


@blueprint.route('/accounts/<id_>', methods=['DELETE', 'GET', 'PATCH'])
@login_required
def account(id_):
    account = get_account(id_)

    check()

    if 'GET' == request.method:
        return jsonify(account=account.as_dict())
    elif 'DELETE' == request.method:
        if account.is_master:
            raise errors.InvalidParameterValue("Master account is protected.")
        (
            Identity.query
            .groups()
            .filter_by(name=account.data['AdminGroupName'])
            .delete()
        )
        (
            Identity.query
            .roles(account)
            .filter_by(arn=account.data['AdminRoleArn'])
            .delete()
        )
        db.session.delete(account)
        try:
            db.session.commit()
        except IntegrityError as e:
            current_app.logger.error("Failed to delete account: %s", e)
            return jsonify(
                400, message="Failed to delete. Account may have resources.")
        return jsonify(200, message="Account deleted.")
    elif 'PATCH' == request.method:
        data = request.form or request.json
        try:
            account.alias = data['NewAlias']
        except KeyError:
            raise errors.ValidationError("Missing NewAlias parameter.")
        group = (
            Identity.query.groups()
            .get_by(name=account.data['AdminGroupName'])
        )
        account.data['AdminGroupName'] = new_name = f'DBA-{account.alias}'
        group.rename_to(new_name)
        db.session.commit()
        return jsonify(
            message="Account and associated group renamed.",
            account=account.as_dict(),
        )
