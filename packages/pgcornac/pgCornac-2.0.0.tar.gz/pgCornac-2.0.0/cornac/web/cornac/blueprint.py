import json
import logging

from flask import Blueprint, current_app, redirect
from sqlalchemy.orm import exc
from werkzeug.exceptions import HTTPException, InternalServerError

from .. import errors
from ...core.model import Account, DBInstance


logger = logging.getLogger(__name__)
blueprint = Blueprint('cornac', __name__)


@blueprint.record
def init_statics(state):
    if state.app.config['CONSOLE_REDIRECT']:
        logger.info(
            "Redirecting static files to %s.",
            state.app.config['CONSOLE_REDIRECT'],
        )
        return

    state.blueprint.static_folder = state.app.config['CONSOLE_HTDOCS']
    state.add_url_rule(
        "/static/<path:filename>",
        view_func=state.blueprint.send_static_file,
        endpoint="static",
    )


@blueprint.route('/')
def index():
    if current_app.config['CONSOLE_REDIRECT']:
        return redirect(current_app.config['CONSOLE_REDIRECT'])

    index_html = current_app.config['CONSOLE_HTDOCS'] + '/index.html'
    try:
        with open(index_html) as fo:
            html = fo.read()
    except OSError as e:
        logger.critical("Failed to open console static file: %s", e)
        raise errors.AWSError()
    endpoint = current_app.config['CANONICAL_URL'] + '/'
    config = f'var endpoint = "{endpoint}";\n'
    if current_app.has_temboard:
        config += f'''var temboard = "{current_app.config['TEMBOARD']}";\n'''
    needle = '// var endpoint = "https://prod.cornac.company.lan/";'
    return html.replace(needle, config)


@blueprint.errorhandler(HTTPException)
@blueprint.errorhandler(InternalServerError)
def json_errorhandler(e):
    response = e.get_response()
    response.data = json.dumps(dict(
        error=e.__class__.__name__,
        message=e.description,
    ))
    response.content_type = 'application/json'
    return response


def get_account(id_):
    id_ = int(id_.lstrip('0'))
    account = Account.query.get(id_)
    if account is None:
        raise errors.NoSuchEntity("Account not found.")
    return account


def get_instance(identifier, status=None):
    try:
        instance = (
            DBInstance.query.current()
            .filter(DBInstance.identifier == identifier)
            .one())
    except exc.NoResultFound:
        raise errors.DBInstanceNotFound(identifier)
    return instance
