from ..errors import (
    AWSError,
    InvalidAction,
    InvalidParameterCombination,
    NoSuchEntity,
    ValidationError,
)

__all__ = [
    'AWSError',
    'InvalidAction',
    'InvalidParameterCombination',
    'NoSuchEntity',
    'ValidationError',
]


class EntityAlreadyExists(AWSError):
    code = 409


class LimitExceeded(AWSError):
    code = 409
