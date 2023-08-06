from flask import Blueprint

from . import actions
from ..endpoint import XMLEndpoint


blueprint = Blueprint('iam', __name__)
endpoint = XMLEndpoint(
    namespace='iam',
    version='2010-05-08',
    actions=actions,
)
endpoint.register(blueprint)
