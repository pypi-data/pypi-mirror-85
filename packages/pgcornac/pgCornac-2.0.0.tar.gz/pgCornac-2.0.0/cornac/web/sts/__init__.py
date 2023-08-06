from flask import Blueprint

from . import actions
from ..endpoint import XMLEndpoint


blueprint = Blueprint('sts', __name__)
endpoint = XMLEndpoint(
    namespace='sts',
    version='2011-06-15',
    actions=actions,
)
endpoint.register(blueprint)
