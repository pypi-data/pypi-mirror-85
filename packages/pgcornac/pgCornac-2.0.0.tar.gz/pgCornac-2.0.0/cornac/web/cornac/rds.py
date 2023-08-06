import logging
from ipaddress import ip_network

from flask import request
from sqlalchemy.orm import exc

from .auth import login_required
from .blueprint import blueprint
from ..auth import check
from ... import worker
from ..errors import NoSuchEntity, ValidationError
from ..utils import jsonify
from ...core.model import db, DBInstance, VirtualIPRange


logger = logging.getLogger(__name__)


@blueprint.route('/recovery-end-callback', methods=['POST'])
def recovery_end_callback():
    token = request.args['token']
    qry = DBInstance.query.filter(DBInstance.recovery_token == token).one
    try:
        instance = qry()
    except exc.NoResultFound:
        return jsonify(status=404, message="Unknown token.")

    worker.recovery_end.send(instance.id)

    instance.recovery_token = None
    db.session.commit()

    return jsonify(message="Success, recovery end task queued.")


@blueprint.route('/virtual-ip-ranges', methods=['GET', 'POST'])
@login_required
def virtual_ip_ranges():
    check()
    if 'GET' == request.method:
        return jsonify(ranges=[
            r.as_dict()
            for r in VirtualIPRange.query.all()
        ])
    else:
        data = request.json or request.form
        try:
            network = ip_network(data['range'])
        except KeyError:
            raise ValidationError("Missing 'range' value.") from None
        except ValueError as e:
            raise ValidationError(f"Bad 'range' value: {e}") from None

        othernet = (
            VirtualIPRange.query
            .filter(VirtualIPRange.range_.intersects(network))
            .first()
        )
        if othernet:
            raise ValidationError(f"{network} intersects with existing range")

        range_ = VirtualIPRange(
            range_=network,
            comment=data.get('comment'),
        )
        db.session.add(range_)
        db.session.commit()
        return jsonify(message="Range saved.", range=range_.as_dict())


@blueprint.route(
    '/virtual-ip-ranges/<id_>', methods=['DELETE', 'GET', 'PATCH']
)
@login_required
def virtual_ip_range(id_):
    check()
    range_ = VirtualIPRange.query.get(int(id_))
    if range_ is None:
        raise NoSuchEntity("Virtual IP range not found.")
    if 'GET' == request.method:
        return jsonify(range=range_.as_dict())
    elif 'PATCH' == request.method:
        data = request.json or request.form
        try:
            range_.comment = data['comment']
        except KeyError:
            raise ValidationError("Missing 'comment'.")
        db.session.commit()
        return jsonify(range=range_.as_dict())
    elif 'DELETE' == request.method:
        if range_.allocated_ips:
            raise ValidationError("Range has one or more allocated IP.")
        db.session.delete(range_)
        db.session.commit()
        return jsonify(message="Successful deletion of range.")
