from flask import g
from werkzeug.exceptions import HTTPException

from ..utils import heredoc


class AWSError(HTTPException):
    code = 500
    description = (
        'The request processing has failed because of an unknown error, '
        'exception or failure.')
    awscode = 'InternalFailure'

    def __init__(self, description=None, code=None, awscode=None, **kw):
        if description is None:
            description = self.description
        super().__init__(description=description, **kw)
        if code:
            self.code = code
        if awscode:
            self.awscode = awscode

    @classmethod
    def __init_subclass__(cls, **kw):
        super().__init_subclass__(**kw)
        cls.awscode = cls.__name__


class AccessDenied(AWSError):
    code = 403

    def __init__(self, description=None,
                 source=None, action=None, resource=None):
        source = source or g.current_identity.name
        action = action or g.current_action
        resource = resource or 'any'
        if description is None:
            description = heredoc(f"""\
            User: {source} is not authorized to perform: {action}
            on resource: {resource}
            """)
        super().__init__(description=description)


class InvalidParameterCombination(AWSError):
    code = 400


class InvalidParameterValue(AWSError):
    code = 400


class IncompleteSignature(AWSError):
    code = 400


class InvalidAction(AWSError):
    code = 400
    description = (
        'The action or operation requested is invalid. '
        'Verify that the action is typed correctly.')


class InvalidClientTokenId(AWSError):
    code = 403
    description = 'The security token included in the request is invalid.'


class MissingAuthenticationToken(AWSError):
    code = 403
    description = 'Missing Authentication Token'


class NoSuchEntity(AWSError):
    code = 404


class ValidationError(AWSError):
    code = 400


class SignatureDoesNotMatch(AWSError):
    code = 403
