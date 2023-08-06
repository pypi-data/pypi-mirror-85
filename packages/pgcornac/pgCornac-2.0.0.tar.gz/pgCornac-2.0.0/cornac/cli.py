#
# Main cornac CLI.
#
# Implements few commands for cornac initialization and maintainance. cornac
# CLI extends flask CLI so you don't have to bother with FLASK_APP env nor use
# two CLI entrypoint.
#

import errno
import logging.config
import os.path
import pdb
import sys
from platform import python_version
from textwrap import dedent
from urllib.parse import urlparse

import bjoern
import click
import psycopg2
from flask import current_app, __version__ as flask_version, g
from flask.cli import FlaskGroup
from flask.globals import _app_ctx_stack
from pkg_resources import get_distribution
from werkzeug import __version__ as werkzeug_version

from . import create_app, worker, __version__
from .core import list_availability_zones
from .core.config import require_ssh_key
from .core.orm import connect, db
from .core.model import (
    AccessKey, Account, DBInstance, DBSnapshot, Identity,
)
from .errors import KnownError
from .iaas import IaaS
from .operator import Operator
from .operator.machine import MachineCork
from .ssh import wait_machine
from .utils import canonical_url_for, make_tenant_hash, update_command_defaults


logger = logging.getLogger(__name__)


class CornacGroup(FlaskGroup):
    # Wrapper around FlaskGroup to lint error handling.

    def main(self, *a, **kw):
        try:
            __import__('psycopg2')
        except ModuleNotFoundError:
            raise KnownError("psycopg2 is missing.")

        try:
            return super().main(*a, **kw)
        except OSError as e:
            if errno.EADDRINUSE == e.errno:
                raise KnownError("Address already in use.")
            raise

    def _load_plugin_commands(self):
        if self._loaded_plugin_commands:
            return

        super(CornacGroup, self)._load_plugin_commands()

        update_command_defaults(
            self.commands['worker'],
            # Since we use Postgres LISTEN, we want to limit the number of
            # listening connection. Dramatiq uses one connection per process.
            processes=1,
            threads=2,
        )


def get_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    bjoern = get_distribution('bjoern')
    python = python_version()
    click.echo(
        f"Cornac {__version__} ("
        f"Python {python}, "
        f"Flask {flask_version}, "
        f"Werkzeug {werkzeug_version}, "
        f"Bjoern {bjoern.version}"
        ")"
    )
    ctx.exit()


# Root group of CLI.
@click.group(cls=CornacGroup, create_app=create_app, add_version_option=False)
@click.option('--verbose/--quiet', default=False)
@click.option('--version', is_flag=True, is_eager=True,
              expose_value=False, callback=get_version,
              help='Show cornac version')
@click.pass_context
def root(ctx, verbose):
    appname = ctx.invoked_subcommand or 'cornac'
    systemd = 'SYSTEMD' in os.environ
    setup_logging(appname=appname, verbose=verbose, systemd=systemd)


@root.command(help=dedent(
    """
    Provision guest and Postgres database for cornac itself. Initialize
    database with schema and data.
    """))
@click.option('--pgversion', default='12',
              help="Postgres engine version to deploy.",
              show_default=True, metavar='VERSION')
@click.option('--size', default=5, type=click.IntRange(5, 300),
              help="Allocated storage size in gigabytes.",
              show_default=True, metavar='SIZE_GB',)
@click.option('--root', metavar='EMAIL', required=True,
              help="First user email address.")
@click.pass_context
def bootstrap(ctx, pgversion, size, root):
    require_ssh_key()
    connstring = current_app.config['SQLALCHEMY_DATABASE_URI']
    pgurl = urlparse(connstring or '')

    g.current_account = None
    zone, *_ = list_availability_zones()
    instance = DBInstance.factory(pgurl.path.lstrip('/'), account_id=1)
    instance.data.update(dict(
        AllocatedStorage=size,
        AvailabilityZone=zone,
        DBInstanceClass='db.t2.micro',
        DeletionProtection=True,
        EngineVersion=pgversion,
        MasterUsername=pgurl.username,
    ))

    try:
        logger.debug("Trying to connect to Postgres at %s.", pgurl.hostname)
        with psycopg2.connect(connstring, connect_timeout=3):
            logger.info("Postgres server responding, reusing.")
    except Exception:
        if pgurl.username is None or pgurl.password is None:
            raise KnownError(
                "Unable to parse username or password from PostgreSQL DSN."
                " Is password missing or too complex?")
        if instance.identifier != pgurl.username:
            raise KnownError("Database name %s does not match username %s." % (
                instance.identifier, pgurl.username))
        instance.data['MasterUserPassword'] = pgurl.password
        with worker.operator_manager() as operator:
            logger.info("Creating %s.", instance)
            operator.create_db_instance(instance)
        # Drop master password before saving command in database.
        instance.data.pop('MasterUserPassword')
    else:
        instance.data['Endpoint'] = dict(
            Address=pgurl.hostname, Port=pgurl.port,
        )

    instance.status = 'available'

    ctx.invoke(migratedb, dry=False)

    Account.bootstrap(instance, root)

    if current_app.has_snapshots:  # Create initial snapshot.
        snapshot = DBSnapshot.factory(instance, 'automated')
        db.session.add(snapshot)
        db.session.commit()
        logger.info("Queueing initial snapshot.")
        worker.create_db_snapshot.send(snapshot.id)
        logger.info("Snapshot will be created once a worker is running.")

    reseturl = canonical_url_for('cornac.index') + '#/reset_password/'
    logger.info("Before first login, reset password at %s.", reseturl)


@root.command(help="Generate access token")
@click.option('--user-name',
              help="User name. Defaults to first created user.")
def generate_credentials(user_name):
    get_user_or_first(user_name)
    logger.info("Saving access key for %s.", g.current_identity)

    access_key = AccessKey.factory(
        access_key=os.environ.get('CORNAC_ACCESS_KEY_ID'),
        secret_key=os.environ.get('CORNAC_SECRET_ACCESS_KEY'),
    )
    db.session.add(access_key)
    db.session.commit()

    sys.stdout.write(dedent(f"""\
    User name,Password,Access key ID,Secret access key,Console login link
    {g.current_identity.name},,{access_key},{access_key.data['SecretAccessKey']},
    """))


@root.command(help="Build predictable instance endpoint address.")
@click.option('--account', default='000000000001',
              help="Account ID.", show_default=True)
@click.option('--region', default=None,
              help="Region name.", show_default=True)
@click.argument('identifier', default='cornac')
def guess_endpoint_address(account, region, identifier):
    print('{prefix}{identifier}-{tenant}{z}{suffix}'.format(
        prefix=current_app.config['MACHINE_PREFIX'],
        identifier=identifier,
        tenant=make_tenant_hash(account, region),
        suffix=current_app.config['DNS_DOMAIN'],
        z='a',
    ))


@root.command(help="Inspect IaaS to update inventory.")
@click.option('--account', default='__all__')
@click.argument('identifier', default='__all__')
def inspect(account, identifier):
    qry = DBInstance.query
    if '__all__' != account:
        account_id = int(account)
        qry = qry.filter_by(account_id=account_id)
    if identifier == '__all__':
        instances = qry.all()
    else:
        instance = qry.filter(DBInstance.identifier == identifier).one()
        instances = [instance]

    for instance in instances:
        logger.debug("Queuing inspection of %s.", instance)
        worker.inspect_instance.send(instance.id)


@root.command(help="Run maintainance window tasks")
def maintainance():
    worker.maintainance(async_=False)


@root.command(help="Serve on HTTP for production.")
@click.argument('listen', default='', metavar='[ADDRESS[:PORT]]')
def serve(listen):
    host, _, port = listen.partition(':')
    host = host or '0.0.0.0'
    port = int(port or 8001)

    # Remove global CLI app context so that app context is set and torn down on
    # each request. This way, Flask-SQLAlchemy app context teardown is called
    # and session is properly remove upon each request.
    ctx = _app_ctx_stack.pop()

    # Ensure IAAS is dropped before serving.
    ctx.app.config['IAAS'] = None

    logger.info("Serving on http://%s:%s/.", host, port)
    try:
        bjoern.run(ctx.app, host, port)
    finally:
        # Push back ctx so that CLI context is preserved
        ctx.push()


@root.command(help="Migrate schema and database of cornac database.")
@click.option('--check', default=False, is_flag=True,
              help="Check whether database is migrated.")
@click.option('--dry/--no-dry', default=True,
              help="Whether to effectively apply migration script.")
def migratedb(check, dry):
    from .core.schema import Migrator
    migrator = Migrator()
    migrator.inspect_available_versions()

    try:
        with connect(current_app.config['SQLALCHEMY_DATABASE_URI']) as conn:
            logger.debug("Postgres server is up.")
    except psycopg2.OperationalError as e:
        raise KnownError("Failed to contact Postgres server: %s" % e)

    with connect(current_app.config['SQLALCHEMY_DATABASE_URI']) as conn:
        migrator.inspect_current_version(conn)
        if migrator.current_version:
            logger.info("Database version is %s.", migrator.current_version)
        else:
            logger.info("Database is not initialized.")

        versions = migrator.missing_versions
        if check:
            if versions:
                logger.info("Latest version is %s.", versions[-1])
                exit(1)
            return

        if dry:
            logger.warning("Dry run. No changes will happen.")

        for version in versions:
            if dry:
                logger.info("Would apply %s.", version)
            else:
                logger.info("Applying %s.", version)
                with conn:  # Wraps in a transaction.
                    migrator.apply(conn, version)

    if versions:
        logger.info("Check terminated." if dry else "Database updated.")
    else:
        logger.info("Database already uptodate.")


@root.command(help="Ensure Cornac service VM are up.")
@click.option('--instances/--no-instances', default=False,
              help="Start/stop instances according to inventory status.")
def recover(instances):
    machine = MachineCork(identifier='cornac')
    with IaaS.connect(current_app.config['IAAS'], current_app.config) as iaas:
        iaas.start_machine(machine)
    connstring = current_app.config['SQLALCHEMY_DATABASE_URI']
    pgurl = urlparse(connstring)
    port = pgurl.port or 5432
    logger.info("Waiting for %s:%s opening.", pgurl.hostname, port)
    wait_machine(pgurl.hostname, port=port)
    logger.info("Testing PostgreSQL connection.")
    with connect(connstring):
        logger.info("Cornac is ready to run.")

    if instances:
        logger.info("Checking Postgres instances.")
        logger.info("You need to start cornac worker to effectively check "
                    "each instances.")
        worker.recover_instances()


@root.command(help="Execute a Python script in cornac runtime.")
@click.argument('path', default='-')
def script(path):
    # Compile source code to have be file and line aware.
    fo = sys.stdin if path == '-' else open(path)
    with fo:
        source = fo.read()
    code = compile(source, path, 'exec')

    globals_ = dict(
        app=current_app,
        config=current_app.config,
    )

    g = globals()
    for v in {'connect', 'db', 'IaaS', Operator.__name__}:
        globals_[v] = g[v]

    exec(code, globals_, globals_)


def entrypoint():
    debug = os.environ.get('DEBUG', '').lower() in ('1', 'y')
    systemd = 'SYSTEMD' in os.environ
    setup_logging(verbose=debug, systemd=systemd)

    try:
        exit(root())
    except (pdb.bdb.BdbQuit, KeyboardInterrupt):
        logger.info("Interrupted.")
    except KnownError as e:
        logger.critical("%s", e)
        exit(e.exit_code)
    except Exception:
        logger.exception('Unhandled error:')
        if debug and sys.stdout.isatty():
            logger.debug("Dropping in debugger.")
            pdb.post_mortem(sys.exc_info()[2])
        else:
            logger.error(
                "Please report at "
                "https://github.com/dalibo/cornac/issues/new with full log.",
            )
    exit(os.EX_SOFTWARE)


class ColoredStreamHandler(logging.StreamHandler):

    _color_map = {
        logging.DEBUG: '2;37',
        logging.INFO: '1;39',
        logging.WARN: '1;38;5;214',
        logging.ERROR: '91',
        logging.CRITICAL: '1;91',
    }

    def format(self, record):
        lines = logging.StreamHandler.format(self, record)
        color = self._color_map.get(record.levelno, '39')
        lines = ''.join([
            '\033[0;%sm%s\033[0m' % (color, line)
            for line in lines.splitlines(True)
        ])
        return lines


class SystemdFormatter(logging.Formatter):
    # cf. http://0pointer.de/blog/projects/journal-submit.html

    priority_map = {
        logging.NOTSET: 6,
        logging.DEBUG: 7,
        logging.INFO: 6,
        logging.WARNING: 4,
        logging.ERROR: 3,
        logging.CRITICAL: 2,
    }

    def format(self, record):
        s = super().format(record)
        return '<%d>%s' % (self.priority_map[record.levelno], s)


def setup_logging(*, appname='cornac', verbose, systemd=False):
    if systemd:
        format_cls = SystemdFormatter.__module__ + ".SystemdFormatter"
        format = '%(message)s'
    else:
        format_cls = 'logging.Formatter'
        format = '%(levelname)1.1s: %(message)s'
        if verbose:
            format = f'%(asctime)s {appname}[%(process)s] {format}'

    config = {
        'version': 1,
        'formatters': {
            'default': {
                '()': format_cls,
                'format': format,
                'datefmt': '%H:%M:%S',
            },
        },
        'handlers': {
            'default': {
                '()': (
                    __name__ + '.ColoredStreamHandler'
                    if sys.stderr.isatty() else
                    'logging.StreamHandler'
                ),
                'formatter': 'default',
            },
            'null': {
                '()': 'logging.NullHandler',
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['default'],
        },
        'loggers': {
            __package__: {
                'level': 'DEBUG' if verbose else 'INFO',
            },
            'sqlalchemy.engine.base.Engine': {
                # Hack sqlalchemy.log.InstanceLogger to not add spurious
                # handler when SQLALCHEMY_ECHO is set.
                'handlers': ['null'],
            }
        },
    }
    logging.config.dictConfig(config)


def get_user_or_first(user_name):
    """Get user_name or fallback to first user, in master account."""
    g.current_account = Account.query.get_master()
    users = Identity.query.users()
    if user_name is None:
        g.current_identity = users.first()
    else:
        try:
            g.current_identity = users.get_by(name=user_name)
        except db.orm.exc.NoResultFound:
            raise KnownError(f"User {user_name} not found.")
    return g.current_identity


update_command_defaults(
    root.commands['run'],
    # By default, make devserver reachable by VM.
    host='0.0.0.0',
    # 8001 port is allowed to postgres by SELinux with nis_enabled boolean.
    # Let's use it as default.
    port=8001,
)
