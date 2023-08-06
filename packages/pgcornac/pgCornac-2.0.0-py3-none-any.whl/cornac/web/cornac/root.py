import logging
import os

from flask import Blueprint, request, redirect
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import OperationalError

from ..utils import jsonify

logger = logging.getLogger(__name__)
root = Blueprint('root', __name__)


# For development purpose, we want /js, /css, etc. to behave like webpack
# devserver, with publicPath empty.
#
# However, we don't redirect / to /cornac until we get ansible modules able to
# access RDS endpoint somewhere else than /.


@root.route('/css/<path:filename>')
@root.route('/fonts/<path:filename>')
@root.route('/img/<path:filename>')
@root.route('/js/<path:filename>')
def assets(filename):
    return redirect('/cornac/static' + request.path)


@root.route('/favicon.png')
def favicon():
    return redirect('/cornac/static' + request.path)


if 'development' == os.environ.get('FLASK_ENV'):
    @root.route('/')
    def index():
        return redirect('/cornac')

    @root.route('/_dev/sqlquery')
    def sqlquery():
        from cornac.core.model import Account
        Account.query.all()
        assert False

    @root.route('/_dev/error')
    def error():
        raise Exception("Pouet")

    @root.route('/_dev/error/http')
    def httperror():
        e = HTTPException(description="Error Message.")
        e.code = 500
        raise e


@root.app_errorhandler(Exception)
def errorhandler(error):
    logger.exception("Unhandled error: %s", error)
    return jsonify(500, message=str(error))


@root.app_errorhandler(HTTPException)
def http_errorhandler(error):
    return jsonify(error.code, message=error.description)


@root.app_errorhandler(OperationalError)
def sqlalchemy_operational_error_handler(error):
    logger.warning("Database error: %s", error)
    return jsonify(500, message="Internal error")
