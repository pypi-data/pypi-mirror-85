from ..errors import (
    AWSError,
    InvalidAction,
    InvalidParameterCombination,
    InvalidParameterValue,
)

__all__ = [
    'InvalidAction',
    'InvalidParameterCombination',
    'InvalidParameterValue',
]


class DBInstanceAlreadyExists(AWSError):
    code = 400
    description = 'DB Instance already exists'


class DBInstanceNotFound(AWSError):
    code = 404

    def __init__(self, identifier):
        super().__init__(description=f"DBInstance {identifier} not found.")


class DBSnapshotAlreadyExists(AWSError):
    code = 400

    def __init__(self, identifier):
        self.identifier = identifier
        super().__init__(description=(
            'Cannot create the snapshot because a snapshot with the '
            f'identifier {identifier} already exists.'))


class DBSnapshotNotFound(AWSError):
    code = 404

    def __init__(self, identifier):
        self.identifier = identifier
        super().__init__(description=f'DBSnapshot not found: {identifier}.')


class InvalidDBInstanceState(AWSError):
    code = 400


class InvalidDBSnapshotState(AWSError):
    code = 400
