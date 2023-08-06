import copy
import ipaddress
import logging
import re
from datetime import datetime

from botocore.auth import SigV4Auth, SIGV4_TIMESTAMP, ISO8601
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials
from flask import g, current_app, request
from itsdangerous import BadData, NoneAlgorithm, URLSafeSerializer
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.urls import url_encode
from werkzeug.middleware.proxy_fix import ProxyFix

from . import errors
from ..core.model import AccessKey, ACL


logger = logging.getLogger(__name__)


def authenticate_from_session():
    # Authenticate using a session token from various HTTP request parameter
    # origins. Requires g.signer from make_signer.

    try:
        token = request.headers['X-Amz-Security-Token']
    except KeyError:
        # Prefering cookies and args over json and form allows to pass session
        # token as query argument whithout messing POST data.
        data = request.cookies or request.args or request.json or request.form
        try:
            token = data['session_token']
        except KeyError:
            raise errors.AWSError("Missing session token.")

    try:
        token = g.signer.loads(token)
    except BadData:
        raise errors.AWSError("Invalid session token signature.", code=403)

    try:
        g.access_key = AccessKey.query.valids().get_by(session_token=token)
    except NoResultFound:
        raise errors.AWSError("Invalid session token.", code=403) from None
    except OperationalError as e:
        raise errors.AWSError(f"Failed to query database: {e}") from None

    g.current_account = g.access_key.account
    g.current_identity = g.access_key.identity


class CredentialsFromBase(object):
    def __getitem__(self, access_key):
        try:
            return AccessKey.query.valids().for_auth().get(access_key)
        except NoResultFound:
            raise KeyError(access_key)


class CredentialsFromDict(object):
    class AccessKey(object):
        def __init__(self, id, secret):
            self.access_key = id
            self.account = None
            self.data = dict(secret_key=secret)

        def __str__(self):
            return self.access_key

        def __repr__(self):
            return '<%s %s mock>' % (self.__class__.__name__, self.access_key)

    def __init__(self, credentials):
        self.credentials = credentials

    def __getitem__(self, key):
        return self.AccessKey(key, self.credentials[key])


def authenticate(request, credentials=None):
    """Entrypoint to verify AWS requests signature"""
    if credentials is None:
        credentials = CredentialsFromBase()
    elif isinstance(credentials, dict):
        # For testing purpose
        credentials = CredentialsFromDict(credentials)

    try:
        authorization = request.headers['Authorization']
    except KeyError:
        raise errors.MissingAuthenticationToken()

    try:
        authorization = Authorization.parse(authorization)
    except Exception as e:
        logger.debug(
            "Failed to parse Authorization header: %.40s: %s.",
            authorization, e)
        raise errors.MissingAuthenticationToken()

    try:
        access_key = credentials[authorization.access_key]
    except KeyError:
        logger.debug("Unknown access key %s.", authorization.access_key)
        raise errors.InvalidClientTokenId()

    check_request_signature(
        request,
        authorization, secret_key=access_key.data['SecretAccessKey'],
    )

    g.access_key = access_key
    g.current_account = access_key.account
    g.current_identity = access_key.identity
    return authorization.access_key


def check_request_signature(request, authorization, secret_key):
    # Reuse botocore API to validate signature.
    if 'AWS4-HMAC-SHA256' != authorization.algorithm:
        raise errors.IncompleteSignature(
            f"Unsupported AWS 'algorithm': '{authorization.algorithm}'")

    if 'aws4_request' != authorization.terminator:
        raise errors.SignatureDoesNotMatch(
            "Credential should be scoped with a valid terminator: "
            f"'aws4_request', not '{authorization.terminator}'.")

    if 'host' not in authorization.signed_headers:
        raise errors.SignatureDoesNotMatch(
            "'Host' must be a 'SignedHeader' in the AWS Authorization.")

    headers_key = {k.lower() for k in request.headers.keys()}
    headers_to_sign = set(authorization.signed_headers)
    for h in headers_to_sign:
        if h not in headers_key:
            raise errors.SignatureDoesNotMatch(
                f"Authorization header requires existence of '{h}' header. "
                f"{authorization}")

    creds = Credentials(authorization.access_key, secret_key)
    signer = SigV4Auth(
        creds, authorization.service_name, authorization.region_name)
    awsrequest = make_boto_request(request, headers_to_sign)
    canonical_request = signer.canonical_request(awsrequest)
    string_to_sign = signer.string_to_sign(awsrequest, canonical_request)
    signature = signer.signature(string_to_sign, awsrequest)

    if signature != authorization.signature:
        logger.debug("CanonicalRequest:\n%s", canonical_request)
        logger.debug("StringToSign:\n%s", string_to_sign)
        logger.debug("Signature:\n%s", signature)
        raise errors.SignatureDoesNotMatch(description=(
            "The request signature we calculated does not match the signature "
            "you provided. Check your AWS Secret Access Key and signing "
            "method. Consult the service documentation for details."
        ))


def make_boto_request(request, headers_to_sign=None):
    # Adapt a Flask request object to AWSRequest.

    if headers_to_sign is None:
        headers_to_sign = [h.lower() for h in request.headers.keys()]
    headers = {
        k: v for k, v in request.headers.items()
        if k.lower() in headers_to_sign}

    netloc = request.url_root.rstrip('/')
    path = request.headers.get('x-forwarded-path', request.path)

    awsrequest = AWSRequest(
        method=request.method,
        url=netloc + path,
        headers=headers,
        # Re-encode back form data. Flask loose it :/ We may want to subclass
        # Flask/Werkzeug Request class to keep the raw_data value before
        # decoding form-data. Say, only if content-length is below 1024 bytes.
        data=url_encode(request.form, 'utf-8'),
    )

    # Get sig timestamp from headers.
    if 'x-amz-date' in request.headers:
        timestamp = request.headers['X-Amz-Date']
    elif 'date' in request.headers:
        date = datetime.strptime(ISO8601, request.headers['Date'])
        timestamp = date.strftime(SIGV4_TIMESTAMP, date)
    else:
        raise errors.IncompleteSignature(
            "Authorization header requires existence of either "
            "'X-Amz-Date' or 'Date' header. "
            f"{request.headers['Authorization']}")
    awsrequest.context['timestamp'] = timestamp

    return awsrequest


class Authorization(object):
    _parameter_re = re.compile(r'([A-Za-z]+)=([^, ]*)')

    @classmethod
    def parse(cls, raw):
        # raw is Authorization header value as bytes, in the following format:
        #
        #     <algorithm> Credential=<access_key>/<date>/<region>/<service>/aws4_request, SignedHeaders=<header0>;<header1>;…, Signature=xxx  # noqa
        #
        # https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-auth-using-authorization-header.html
        # explains details.

        kw = dict(raw=raw)
        kw['algorithm'], parameters = raw.split(maxsplit=1)

        missing_parameters = {'Credential', 'SignedHeaders', 'Signature'}
        for match in cls._parameter_re.finditer(parameters):
            key, value = match.groups()
            if key in missing_parameters:
                missing_parameters.remove(key)
            if 'Credential' == key:
                value = value.split('/')
                access_key, date, region_name, service_name, terminator = value
                kw.update(
                    access_key=access_key,
                    date=date,
                    region_name=region_name,
                    service_name=service_name,
                    terminator=terminator
                )
            elif 'SignedHeaders' == key:
                kw['signed_headers'] = value.split(';')
            elif 'Signature' == key:
                kw['signature'] = value

        if missing_parameters:
            raise errors.IncompleteSignature(
                ' '.join(
                    f"Authorization header requires '{k}'parameter."
                    for k in missing_parameters) +
                f'Authorization={raw}'
            )

        return cls(**kw)

    def __init__(self, *, access_key, algorithm='AWS4-HMAC-SHA256', date,
                 region_name='local', service_name='rds',
                 signature, signed_headers='host', terminator='aws4_request',
                 raw=None):
        attrs = locals()
        del attrs['self']
        self.__dict__.update(attrs)

    def __str__(self):
        if self.raw is None:
            scope = "/".join([
                self.access_key, self.date, self.region_name,
                self.service_name, self.terminator,
            ])
            signed_headers = ';'.join(self.signed_headers)
            self.raw = (
                f"{self.algorithm} "
                f"Credential={scope}, "
                f"SignepdHeaders={signed_headers}, "
                f"Signature={self.signature}"
            )
        return self.raw

    def __setattr__(self, name, value):
        # Note that self.__dict__.update() bypasses __setattr__.
        if name != 'raw':
            # Invalidate serialization cache.
            self.raw = None
        return super().__setattr__(name, value)

    def copy(self, **kw):
        clone = copy.deepcopy(self)
        clone.__dict__.update(kw)
        return clone


class ACLEvalResult:
    def __init__(
            self, source, action, resource, decision='allowed',
            statements=None):
        self.source = source
        self.action = action
        self.resource = resource
        self.decision = decision
        self.statements = statements or []

    def raise_for_decision(self):
        log_prefix = "Access <%s %s on %s> "
        log_args = (self.source, self.action, self.resource or '*')

        if self.decision == 'allowed':
            logger.debug(
                log_prefix + "allowed by %s",
                *log_args, ', '.join(repr(s) for s in self.statements),
            )
            return True
        else:
            if self.decision == 'implicitDeny':
                logger.debug(log_prefix + "implicitly denied.", *log_args)
            else:
                logger.debug(
                    log_prefix + "denied by %s",
                    *log_args, ', '.join(
                        repr(s) for s in self.statements if s.effect == 'Deny'
                    ),
                )
        raise errors.AccessDenied(self.source.name, self.action, self.resource)

    @property
    def allowed(self):
        return self.decision == 'allowed'


def check(*, source=None, action=None, resource=None, raise_=True):
    """Helper for action handler to check privileges.

    source defaults to g.current_identity and action defaults to
    g.current_action. The XMLEndpoint class sets g.current_action and
    g.current_identity properly. Thus, there is no need to specify something
    else than resource if relevant.
    """
    action = action or g.current_action
    source = source or g.current_identity

    service, _, _ = action.partition(':')
    actions = expand_actions(action)
    sources = ['*'] + [source.arn] + [g.arn for g in source.groups]
    resources = expand_resources(
        resource, service=service, account=g.current_account)

    statements = ACL.query.match(sources, actions, resources).all()
    denies = [s for s in statements if s.effect == 'Deny']
    if not statements:
        result = ACLEvalResult(source, action, resource, 'implicitDeny')
    elif denies:
        result = ACLEvalResult(source, action, resource, 'denied', statements)
    else:
        result = ACLEvalResult(source, action, resource, statements=statements)

    g.last_acl_result = result

    if raise_:
        result.raise_for_decision()
    else:
        return result


def check_access_to_rds(account):
    # Check whether current user has direct or indirect access to RDS resources
    # on account.
    if account.data['AdminRoleArn'] is None:
        return check(
            action='rds:CreateDBInstances',
            resource='*',
            raise_=False,
        ).allowed
    else:
        return check(
            action='sts:AssumeRole',
            resource=account.data['AdminRoleArn'],
            raise_=False,
        ).allowed


def no_check_required():
    # Not checking privileges triggers an AccessDenied error to prevent bug by
    # forgetting check. This function explicitly tells that check is not
    # required.
    g.last_acl_result = True


def expand_actions(action):
    """Returns the list of pattern relevant for this action."""
    actions = ['*']
    if action != '*':
        namespace, _, name = action.partition(':')
        if name != '*':
            actions.append(namespace + ':*')
        actions.append(action)
    return actions


def expand_resources(resource, service=None, *, account):
    # Object having an `arn` attribute will be checked on the ARN value. ACL
    # statements with resource `*`, `arn:cornac::RRRR:AAAAAAAAAAAA:*`,
    # `arn:cornac:SSSS:RRRR:AAAAAAAAAAAA:*` or resource param will match.
    resources = []
    if hasattr(resource, 'arn'):
        resources.append(resource.arn)
    elif resource is not None:
        resources.append(str(resource))
    if service:
        resources.append(account.build_arn(service, resource='*'))
    resources.append(account.build_arn(service='', resource='*'))
    resources.append('*')
    return resources


def make_signer(salt=None):
    # Builds an itsdangerous.Serializer instance for signing tokens.
    secret = current_app.config['SECRET_KEY']
    signer_kw = {}

    if secret is None:
        if current_app.config['ENV'] == 'production':
            current_app.logger.critical(
                "SECRET_KEY configuration is required in production.")
            raise errors.AWSError("Internal Error")
        secret = ''
        signer_kw['algorithm'] = NoneAlgorithm()

    return URLSafeSerializer(
        secret_key=secret, salt=salt, signer_kwargs=signer_kw)


class TrustedProxyFix(ProxyFix):
    # A WSGI middleware applying proxy headers if remote_addr is trusted.

    def __init__(self, app, trusted_addresses):
        super().__init__(app)
        self.trusted_networks = [
            ipaddress.ip_network(network, strict=False)
            for network in trusted_addresses
        ]

    def __call__(self, environ, start_response):
        remote_addr = ipaddress.ip_address(environ['REMOTE_ADDR'])
        for network in self.trusted_networks:
            if remote_addr in network:
                return super().__call__(environ, start_response)
        else:
            return self.app(environ, start_response)
