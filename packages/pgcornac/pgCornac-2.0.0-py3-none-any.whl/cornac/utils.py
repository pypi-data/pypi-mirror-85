import string
from contextlib import contextmanager
from datetime import datetime, timezone
from hashlib import sha256
from random import choice
from textwrap import dedent

from flask import (
    current_app,
    url_for,
    _app_ctx_stack,
    _request_ctx_stack,
)


def parse_time(timestamp):
    return datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')


def format_arn(*, partition='cornac', service, region, account_id, resource):
    # See
    # https://docs.aws.amazon.com/fr_fr/general/latest/gr/aws-arns-and-namespaces.html
    return f'arn:{partition}:{service}:{region}:{account_id:012d}:{resource}'


def format_time(date=None):
    date = date or datetime.utcnow()
    if date.tzinfo:
        utcoffset = date.tzinfo.utcoffset(date)
        date = date - utcoffset
    date = date.replace(tzinfo=None)
    return date.isoformat(timespec='seconds') + 'Z'


def heredoc(string):
    # Ease writing long error message by trimming indentation and unwrapping
    # lines.
    return dedent(string).replace('\n', ' ').strip()


def make_tenant_hash(account_id, region=None, salt=None, length=8):
    account_id = int(account_id)
    region = region or current_app.config['REGION']
    salt = salt or current_app.config['TENANT_HASH_SALT']
    # cf.https://stackoverflow.com/questions/45761279/aws-rds-endpoint-address
    s = f'{salt}-{account_id}-{region}'
    h = sha256(s.encode('utf-8'))
    return h.hexdigest()[:length]


def pwgen(length=32):
    valid = False
    while not valid:
        _pwchars = string.ascii_letters + string.digits
        pw = ''.join([choice(_pwchars) for _ in range(length)])
        try:
            validate_password_strength(pw)
            valid = True
        except ValueError:
            pass

    return pw


@contextmanager
def patch_dict(dict_, **values):
    new = {k for k in values if k not in dict_}
    backup = {k: dict_[k] for k in values if k not in new}
    dict_.update(values)
    try:
        yield dict_
    finally:
        dict_.update(backup)
        for k in new:
            dict_.pop(k)


@contextmanager
def patch_url_adapter(adapter):
    ctx = _request_ctx_stack.top or _app_ctx_stack.top
    old = ctx.url_adapter
    ctx.url_adapter = adapter
    try:
        yield ctx.url_adapter
    finally:
        ctx.url_adapter = old


def canonical_url_for(endpoint, **kw):
    """ Alternative of url_for to build constant canonical URL """
    # We want cornac webservice to be accessible from any address, e.g. to
    # listen on 0.0.0.0. At the same time, we need to set SERVER_NAME to forge
    # URL from background worker or commands, but also to forge canonical URL
    # while queried from any IP.
    #
    # But once SERVER_NAME is set in config, Flask requires every request's
    # HTTP Host header to match SERVER_NAME. This breaks querying from
    # localhost or by IP.
    #
    # To workaround this, cornac has a dedicated CANONICAL_URL config option,
    # combining PREFERRED_URL_SCHEME, SERVER_NAME and APPLICATION_ROOT, but
    # only for URL building, not routing.
    kw['_external'] = True
    with patch_url_adapter(current_app.canonical_url_adapter):
        return url_for(endpoint, **kw)


def update_command_defaults(command, **new_defaults):
    params = {
        p.name: p
        for p in command.params
        if p.name in new_defaults
    }
    for k, v in new_defaults.items():
        params[k].default = v


def utcnow():
    return datetime.now(tz=timezone.utc)


def validate_password_strength(password):
    if len(password) < 8:
        raise ValueError("Length is less than 8 chars.")

    has_lower = has_upper = has_number = has_punct = False

    for char in password:
        if not 32 <= ord(char) <= 126:
            raise ValueError(
                "Special char denied. "
                "Only letters, number, space and ASCII-7 punctation are "
                "allowed.")
        if 'a' <= char <= 'z':
            has_lower = True
        elif 'A' <= char <= 'Z':
            has_upper = True
        elif '0' <= char <= '9':
            has_number = True
        else:
            has_punct = True

    if sum([has_lower, has_upper, has_number, has_punct]) < 3:
        raise ValueError(
            "Missing kind of chars. "
            "Password must contains 3 of the following items: "
            "lowercase letters, uppercase letters, numbers, punctuation.")


def zoned_config(zone, prefix):
    # Returns Flask config value depending on instance availability zone.
    return current_app.config[prefix + zone[-1].upper()]
