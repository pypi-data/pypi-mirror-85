from flask import Blueprint

from . import actions
from ..endpoint import XMLEndpoint

blueprint = Blueprint('rds', __name__)
endpoint = XMLEndpoint(
    namespace='rds',
    version='2014-10-31',
    actions=actions,
)
endpoint.register(blueprint)
