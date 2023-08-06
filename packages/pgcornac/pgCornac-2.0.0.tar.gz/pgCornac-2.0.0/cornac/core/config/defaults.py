#
#       D E F A U L T   C O N F I G U R A T I O N
#
# You can override every settings using environment by prefixing setting with
# CORNAC_. e.g CORNAC_IAAS will configure IAAS setting.

import socket

from cornac.core.instanceclass import DBInstanceClass


# Address to backup server. Must be a full URL like ssh://user@hosts:/path.
BACKUPS_LOCATION = None

# Reachable address for cornac service.
CANONICAL_URL = 'http://' + socket.getfqdn() + ':8001'

# Path to config file. By default, config.py in current directory.
CONFIG = 'config.py'

# Path to console assets.
CONSOLE_HTDOCS = '/usr/share/aws-console/htdocs'

# Instead of serving statics, redirect to the following address. e.g.
# http://localhost:8080 .
CONSOLE_REDIRECT = None

# List of allowed origin for requests. This is enforced by browsers. e.g.
# ['https://console.cloud.lan'].
CORS_ORIGINS = '*'

# Domain suffix to resolve guest IP from DNS.
DNS_DOMAIN = ''

# List of client URLs of etcd v3 nodes.
#
# In cornac.py, set a Python list e.g.
# ETCD = ['https://host0', 'https://host1:4002', 'https://host2'].
#
# Env var format is a comma separated list of host:port string. e.g.
# CORNAC_ETCD=http://host0,http://host1:4002,http://host2
ETCD = []

# Credentials to etcd cluster. Requires root privileges.
#
# Format is <user>:<password>
ETCD_CREDENTIALS = None

# IAAS URL, starting with provider prefix, + sign and provider specific URL.
# e.g. libvirt, vcenter+https://me:password@vcenter.acmi.lan/?no_verify=1
IAAS = None

# List of instance classes to expose as orderable.
INSTANCE_CLASSES = list(DBInstanceClass.aliases.values())

# Provider specific name of the template machine to clone. You must install
# Postgres and other tools. See origin/ for how to maintain this template with
# Ansible.
#
# For vSphere, must be a full path to the VM. e.g.
# datacenter1/vm/templates/{MACHINE_PREFIX}-origin.
#
# The doubling of hyphen is wanted. It allow to avoid clashes with a db
# instance named origin.
MACHINE_ORIGIN = '{MACHINE_PREFIX}-origin'

# Prefix of VM in IaaS.
#
# This allow to isolate several instance of cornac in the same IaaS.
MACHINE_PREFIX = 'cornac-'

# Global maintenance window.
#
# Start of a 8 hours time window where maintainances tasks will be applied. The
# format is cron-style as supported by periodiq
# <https://gitlab.com/bersace/periodiq/>.
#
# See.
# https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
# for details.
MAINTAINANCE_WINDOW = '0 22 * * *'

# Provider specific guest network.
#
# For vSphere, use absolute path e.g. 'datacenter1/network/Guest Network'
NETWORK = None

# Name of operator plugin to load.
OPERATOR = 'basic'

# Region name, for ARNs.
REGION = 'local1'

# DSN to Postgres database.
SQLALCHEMY_DATABASE_URI = None

# Provider-specific name of the storage pool (or datastore in vSphere).
STORAGE_POOL_A = 'default'
STORAGE_POOL_B = None  # None disables HA.

# Salt for hostname hash, avoiding conflict with other cornac instances.
TENANT_HASH_SALT = '4'  # https://www.xkcd.com/221/

# URL to temBoard, without credentials, or None.
TEMBOARD = None
# temBoard UI admin access. <username>:<password>
TEMBOARD_CREDENTIALS = None

# SSH Public key used for deployement and maintainance of guests.
DEPLOY_KEY = None

# List of CIDR of trusted proxies addresses. X-Forwarded-* headers will be
# considered for theses addresses.
TRUSTED_PROXIES_ADDRESSES = ['127.0.0.0/8']

# vCenter specific resource pool where to place guests. Could be a host or a
# cluster resource pool. e.g. 'datacenter1/host/esxi1/Resources
VCENTER_RESOURCE_POOL_A = None
VCENTER_RESOURCE_POOL_B = None

# Outgoing mail settings.
MAIL_DSN = None
MAIL_FROM = None

#
#       I N T E R N A L S
#
# Here cornac configures Flask and extensions. You should not overload this
# settings.

DRAMATIQ_BROKER = 'dramatiq_pg:PostgresBroker'
DRAMATIQ_BROKER_URL = None
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
