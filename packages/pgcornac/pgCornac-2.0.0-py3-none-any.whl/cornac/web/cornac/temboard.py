import logging

from flask import g, redirect

from .blueprint import blueprint, get_account, get_instance
from .. import errors


logger = logging.getLogger(__name__)


@blueprint.route('/temboard/redirect/<account>/<instance>')
def temboard_redirect(account, instance):
    g.current_account = get_account(account)
    instance = get_instance(instance)
    try:
        url = instance.data['XTemboardURL']
    except KeyError:
        raise errors.NoSuchEntity(f"Can't find temBoard URL of {instance}.")

    return redirect(url)
