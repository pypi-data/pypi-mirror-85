import logging
from textwrap import dedent

from flask import current_app, make_response

from .blueprint import blueprint
from ..utils import jsonify


logger = logging.getLogger(__name__)


# Implement NoCloud cloud-init metadata endpoint.
# See. https://cloudinit.readthedocs.io/en/18.5/topics/datasources/nocloud.html
@blueprint.route('/cloud-init/<instance>/meta-data')
def cloudinit_metadata(instance):
    return jsonify(**{
        "instance-id": instance,
        "local-hostname": instance,
        "public-keys": [current_app.config['DEPLOY_KEY']],
    })


# Implement NoCloud cloud-init metadata endpoint.
# See. https://cloudinit.readthedocs.io/en/18.5/topics/datasources/nocloud.html
@blueprint.route('/cloud-init/<instance>/user-data')
def cloudinit_userdata(instance):
    return make_response((
        dedent(f"""\
        #cloud-config
        disable_root: false
        hostname: {instance}
        ssh_authorized_keys:
        - "{current_app.config['DEPLOY_KEY']}"
        runcmd:
        # Refresh DHCP configuration to tell DHCP server the current hostname.
        - dhclient -r
        - dhclient -H {instance}
        final_message: "Initialized by Cornac."
        """),
        {
            "Content-Type": "text/cloud-config",
        },
    ))
