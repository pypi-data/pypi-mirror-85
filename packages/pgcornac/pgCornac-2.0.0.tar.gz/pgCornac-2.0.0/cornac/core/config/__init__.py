import logging
import os
import subprocess
from urllib.parse import parse_qs, urlparse
from distutils.util import strtobool

from dotenv import dotenv_values
from flask import current_app

from cornac.errors import KnownError


logger = logging.getLogger(__name__)


def parse_mail_dsn(dsn):
    if dsn in ('console:', 'memory:'):
        return {'MAIL_BACKEND': dsn[:-1]}

    parsed = urlparse(dsn or '')

    if parsed.scheme == 'file':
        return {
            'MAIL_BACKEND': 'file',
            'MAIL_FILE_PATH': parsed.path,
        }

    if not parsed.scheme.startswith('smtp'):
        raise ValueError('invalid SMTP url %s' % dsn)

    use_ssl = parsed.scheme == 'smtps'
    qs = parse_qs(parsed.query)
    use_tls = any(int(v) for v in qs.get('tls', []))

    return {
        'MAIL_BACKEND': 'smtp',
        'MAIL_SERVER': parsed.hostname,
        'MAIL_PORT': parsed.port,
        'MAIL_USERNAME': parsed.username,
        'MAIL_PASSWORD': parsed.password,
        'MAIL_USE_SSL': use_ssl,
        'MAIL_USE_TLS': use_tls,
    }


def configure(app, environ=os.environ):
    app.config.from_object(__name__ + '.defaults')

    c = app.config
    c.from_mapping(filter_env(c, environ=dotenv_values()))
    c.from_mapping(filter_env(c, environ=environ))

    pathes = app.config['CONFIG'].split(',')
    for path in pathes:
        path = os.path.realpath(path)
        if os.path.exists(path):
            app.config.from_pyfile(path)

    if not c['DRAMATIQ_BROKER_URL']:
        c['DRAMATIQ_BROKER_URL'] = c['SQLALCHEMY_DATABASE_URI']

    if not c['DEPLOY_KEY'] and 'SSH_AUTH_SOCK' in environ:
        c['DEPLOY_KEY'] = read_ssh_key()

    if 'development' == c['ENV']:
        c['MAIL_DSN'] = c.get('MAIL_DSN') or 'console:'
        c['MAIL_FROM'] = (
            c.get('MAIL_FROM')
            or 'PostgreSQL DBaaS Dev Server <noreply@acme.tld>'
        )

    if c['MAIL_DSN']:
        try:
            mail_conf = parse_mail_dsn(c['MAIL_DSN'])
        except ValueError as e:
            raise KnownError("Failed to parse %s: %s" % (c['MAIL_DSN'], e))

        for k, v in mail_conf.items():
            c.setdefault(k, v)


def filter_env(config, environ=os.environ):
    known_vars = set(f'CORNAC_{k}' for k in config)
    vars_ = dict(
        (
            k.replace('CORNAC_', ''),
            v.decode('utf-8') if hasattr('v', 'decode') else v,
        )
        for k, v in environ.items()
        if k in known_vars
        )

    # Process booleans and lists.
    for k, v in vars_.items():
        if isinstance(config[k], bool):
            try:
                vars_[k] = strtobool(v)
            except ValueError:
                # Accept non-boolean value like `debug` for SQLALCHEMY_ECHO
                pass

        if isinstance(config[k], list):
            vars_[k] = v.split(',')

    return vars_


def read_ssh_key():
    logger.debug("Reading SSH keys from agent.")
    try:
        out = subprocess.check_output(["ssh-add", "-L"])
    except Exception as e:
        raise KnownError(f"Failed to read SSH public key: {e}") from None

    keys = out.decode('utf-8').splitlines()
    if keys:
        return keys[0]


def require_ssh_key():
    if not current_app.config['CONFIG']:
        raise KnownError("SSH Agent has no key loaded.")
