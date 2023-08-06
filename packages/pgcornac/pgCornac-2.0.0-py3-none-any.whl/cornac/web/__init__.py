from flask import current_app, make_response, request

from .iam import blueprint as iam
from .rds import blueprint as rds
from .sts import blueprint as sts
from .cornac import blueprint as cornacbp, root


def set_server_header(response):
    response.headers['Server'] = current_app.app_version
    return response


def fallback(e):
    # By default, log every requests.
    current_app.logger.info(
        "Unhandled request: %s %s %s",
        request.method, request.path, dict(request.form))
    return make_response('Not Found', 404)


__all__ = ['cornacbp', 'fallback', 'iam', 'rds', 'root', 'sts']
