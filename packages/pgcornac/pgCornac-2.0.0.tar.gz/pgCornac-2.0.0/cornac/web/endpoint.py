import logging
from functools import partial
from uuid import uuid4

from flask import current_app, g, request
from sqlalchemy import exc as saerrors
from werkzeug.exceptions import HTTPException

from . import (
    errors,
    xml,
)
from .auth import authenticate
from .utils import resolve_payload_arrays


logger = logging.getLogger(__name__)


class XMLEndpoint:
    # This is a generic XML entrypoint as used for RDS and IAM. It's a single
    # POST request handler.
    #
    # To implement a new action, one must define a function in action module.
    # If the action requires background processing or worker privileges, one
    # must define a corresponding task (or actor) in cornac.worker. Finally, if
    # the action require effective operation on Postgres host or in IaaS, one
    # must add new methods in cornac.operator.Operator or its implementation,
    # as well as cornac.iaas.IaaS and its implementation.
    def __init__(self, namespace, version, actions):
        self.logger = logging.getLogger(__package__ + '.' + namespace)
        self.namespace = namespace
        self.NAMESPACE = namespace.upper()
        self.version = version
        self.xmlns = f"https://{namespace}.amazonaws.com/doc/{version}"
        self.actions = actions
        self.__name__ = namespace

    def __call__(self):
        g.aws_service = self.namespace
        payload = dict(request.form.items(multi=False))
        requestid = uuid4()
        log_ = partial(
            self.log, requestid, payload.get('Action', '*UndefinedAction*'))

        try:
            payload = resolve_payload_arrays(payload)
            action, payload = self.check_payload(payload)
            g.current_action = f'{self.namespace}:{action.__name__}'
            g.last_acl_result = False
            g.access_key = authenticate(request)
            log_.keywords.update(dict(
                account=g.current_account,
                user=g.current_identity.name,
            ))

            response = xml.make_response_xml(
                action=action.__name__,
                result=action(**payload),
                requestid=requestid,
                xmlns=self.xmlns,
            )
            if g.last_acl_result is False:
                # This prevent information leaking, but not damage.
                logger.error(
                    "Permission not checked by %s, refusing to answer.",
                    action.__name__)
                raise errors.AccessDenied()

            log_(result='OK')
        except HTTPException as e:
            if not isinstance(e, errors.AWSError):
                e = errors.AWSError(code=e.code, description=str(e))
            # Still log user error at INFO level.
            log_(code=e.code, result=e.awscode)
            response = xml.make_error_xml(error=e, requestid=requestid)
        except saerrors.OperationalError as sae:
            e = errors.AWSError()
            current_app.logger.error("Database error: %s", sae)
            response = xml.make_error_xml(error=e, requestid=requestid)
        except Exception:
            # Don't expose error.
            e = errors.AWSError()
            current_app.logger.exception(
                "Unhandled %s error:", self.NAMESPACE)
            log_(code=e.code, result=e.awscode, level=logging.ERROR)
            response = xml.make_error_xml(error=e, requestid=requestid)

        return response

    def check_payload(self, payload):
        action_name = payload.pop('Action', None)
        if action_name is None:
            raise errors.InvalidAction()

        version = payload.pop('Version', None)
        if version != self.version:
            raise errors.InvalidAction(
                description=f"Unsupported API version {version}.")

        action = getattr(self.actions, action_name, None)
        if action is None:
            self.logger.warning("Unknown %s action: %s.", action_name)
            self.logger.debug("payload=%r", payload)
            raise errors.InvalidAction()
        action.__name__ = action_name

        return action, payload

    def log(self, requestid, action_name, result, code=200,
            level=logging.INFO, account='-', user='-'):
        current_app.logger.log(
            level, "%s %s %s %s %s %s",
            self.NAMESPACE, account, user, action_name, code, result
        )

    def register(self, blueprint):
        return blueprint.route('/', methods=['POST'])(self)
