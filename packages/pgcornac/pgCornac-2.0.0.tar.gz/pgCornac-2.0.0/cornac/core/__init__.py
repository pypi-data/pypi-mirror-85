#
# Core package shares objects and functions used by every pieces of cornac: web
# handlers, CLI scripts, background workers.
#

from flask import current_app


def list_availability_zones():
    return [
        current_app.config['REGION'] + 'a',
        current_app.config['REGION'] + 'b',
    ]
