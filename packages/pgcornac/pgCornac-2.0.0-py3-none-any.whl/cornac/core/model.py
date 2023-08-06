import logging
import re
from datetime import datetime, timedelta
from ipaddress import ip_interface
from textwrap import dedent

from flask import g, current_app
from sqlalchemy.exc import IntegrityError

from ..errors import KnownError
from ..utils import (
    canonical_url_for, format_arn, format_time, utcnow, make_tenant_hash,
)
from .user import (
    generate_id, generate_secret, generate_session_token,
    hash_password,
)
from .orm import db


logger = logging.getLogger(__name__)


class AccessKey(db.Model):
    __tablename__ = 'access_keys'
    __table_args__ = {'schema': 'cornac'}

    Status = db.ENUM('Active', 'Inactive', name='access_key_status')

    id = db.Column(db.Integer, primary_key=True)
    identity_id = db.Column(db.Integer, db.ForeignKey('cornac.identities.id'))
    access_key = db.Column(db.String)
    edate = db.Column(db.TIMESTAMP(timezone=True))
    status = db.Column(Status)
    session_token = db.Column(db.String)
    data = db.Column(db.JSONB)

    identity = db.relationship(
        'Identity', lazy='select',
        backref=db.backref(
            'access_keys', lazy='select',
            cascade='all, delete-orphan', passive_deletes=True),
    )

    def __str__(self):
        return self.access_key

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.access_key)

    @property
    def account(self):
        return self.identity.account

    class query_class(db.Query):
        def for_auth(self):
            """Setup query for auth.

            Preloads objects and filter invalid access keys."""
            return (
                self
                .options(
                    db
                    .joinedload(self.m.identity)
                    .joinedload(Identity.account),
                    db
                    .joinedload(self.m.identity)
                    .joinedload(Identity.groups)
                )
                .valids()
            )

        def get(self, access_key):
            if isinstance(access_key, int):
                return super().get(access_key)
            else:
                return self.filter(self.m.access_key == access_key).one()

        def with_user(self, name):
            return (
                self
                .options(db.joinedload(self.m.identity))
                .filter(Identity.name == name)
            )

        def valids(self):
            return (
                self
                .filter(self.m.status == 'Active')
                .filter(
                    (self.m.edate.is_(None))
                    | (self.m.edate >= db.func.current_timestamp())
                )
            )

    @classmethod
    def factory(cls, access_key=None, secret_key=None, identity=None,
                temporary=False):
        self = cls()
        self.identity = identity or g.current_identity
        prefix = 'CSIA' if temporary else 'CKIA'
        self.access_key = access_key or generate_id(prefix=prefix)
        self.status = 'Active'
        self.data = dict(
            CreateDate=format_time(),
            SecretAccessKey=secret_key or generate_secret(),
            IdentityArn=self.identity.arn,
        )
        if temporary:
            self.edate = utcnow() + timedelta(hours=1)
            self.session_token = generate_session_token()

        return self


class Account(db.Model):
    __tablename__ = 'accounts'
    __table_args__ = {'schema': 'cornac'}

    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String)
    data = db.Column(db.JSONB)

    def __format__(self, format_spec):
        return '%012d' % self.id

    def __str__(self):
        return self.alias

    class query_class(db.Query):
        def get_master(self):
            return self.get(1)

    @property
    def is_master(self):
        return 1 == self.id

    @classmethod
    def bootstrap(cls, instance, root_username):
        self = cls()
        self.alias = 'Master'
        self.data = dict(AdminGroupName='Admins', AdminRoleArn=None)
        logger.info("Creating Master account.")
        db.session.add(self)
        try:
            db.session.flush()
        except IntegrityError as e:
            logger.debug("Integrity error: %s", e)
            raise KnownError(
                "Unable to create master account."
                " Is database already initialized?")
        if not self.is_master:
            raise KnownError("Can't create master account.")
        g.current_account = self

        logger.info("Creating Admins group.")
        admins = Identity.group_factory(self.data['AdminGroupName'])
        db.session.add(admins)
        ACL.allow(source=admins, action='*', resource='*')

        logger.info("Creating first user %s.", root_username)
        root = Identity.user_factory(root_username)
        root.groups.append(admins)
        db.session.add(root)

        logger.info("Registering own instance to inventory.")
        instance.account = self
        db.session.add(instance)

        # Allow anyone to inspect orderable options.
        ACL.allow(
            source='*',
            action='rds:DescribeOrderableDBInstanceOptions',
            resource='*')

        db.session.commit()

    def build_arn(self, service=None, resource=''):
        if service is None:
            service = g.aws_service
        return format_arn(
            service=service,
            region=current_app.config['REGION'],
            account_id=self.id,
            resource=resource,
        )

    def as_dict(self):
        return dict(
            AccountId=f'{self}',
            AccountAlias=self.alias,
            AdminGroupName=self.data['AdminGroupName'],
            AdminRoleArn=self.data['AdminRoleArn'],
        )


class ACL(db.Model):
    # This class represent an ACL statement. Class methods manage the list of
    # statements.

    Effect = db.ENUM('Deny', 'Allow', name='acl_effect')

    __tablename__ = 'acl_statements'
    __table_args__ = {'schema': 'cornac'}

    id = db.Column(db.Integer, primary_key=True)
    identity_id = db.Column(db.Integer, db.ForeignKey('cornac.identities.id'))
    source = db.Column(db.String)
    effect = db.Column(Effect)
    action = db.Column(db.String)
    resource = db.Column(db.String)
    data = db.Column(db.JSONB)

    identity = db.relationship(
        'Identity', lazy='select',
        backref=db.backref(
            'acl_statements',
            lazy='select',
            cascade='all, delete-orphan',
            passive_deletes=True,
        ),
    )

    class query_class(db.Query):
        def match(self, sources, actions, resources):
            return (
                self
                .filter(self.m.source.in_(sources))
                .filter(self.m.action.in_(actions))
                .filter(self.m.resource.in_(resources))
            )

    def __repr__(self):
        return '<ACL stmt %s %s %s %s>' % (
            self.effect, self.source, self.action, self.resource,
        )

    def __str__(self):
        return f'acl_statement_{self.id}'

    @classmethod
    def register(cls, *, source, action, resource, effect='Allow'):
        self = cls()
        source = source or g.current_identity
        if hasattr(source, 'arn'):
            self.identity = source
            self.source = source.arn
        else:
            self.source = source
        if hasattr(resource, 'arn'):
            resource = resource.arn
        self.resource = resource
        self.action = action
        self.effect = effect
        return self

    allow = register


class DBInstance(db.Model):
    Status = db.ENUM(
        # Keep it sync with cornac/core/schema/001-instances.sql.
        'available',
        'backing-up',
        'creating',
        'deleting',
        'failed',
        'incompatible-network',
        'incompatible-option-group',
        'incompatible-parameters',
        'incompatible-restore',
        'maintenance',
        'modifying',
        'rebooting',
        'renaming',
        'resetting-master-credentials',
        'restore-error',
        'starting',
        'stopped',
        'stopping',
        'storage-full',
        'storage-optimization',
        'upgrading',
        name='db_instance_status',
    )

    __tablename__ = 'db_instances'
    __table_args__ = {'schema': 'cornac'}

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('cornac.accounts.id'))
    identifier = db.Column(db.String)
    status = db.Column(Status)
    status_message = db.Column(db.String)
    recovery_token = db.Column(db.String)
    data = db.Column(db.JSONB)
    iaas_data = db.Column(db.JSONB)
    operator_data = db.Column(db.JSONB)

    _identifier_re = re.compile(r'[a-z][a-z0-9-]*[a-z0-9]')

    account = db.relationship(
        'Account',
        # Actually, since account is just an Id, it's simpler to access
        # account_id instead of account.id.
        lazy='select',
        # The backref is more useful.
        backref=db.backref('instances', lazy='select'),
    )

    class query_class(db.Query):
        def current(self):
            return self.filter(self.m.account == g.current_account)

    @property
    def arn(self):
        return self.data['DBInstanceArn']

    @classmethod
    def check_identifier(cls, value):
        if '--' in value:
            raise ValueError("Double hyphen detected")
        value = value.lower()
        if not cls._identifier_re.match(value):
            raise ValueError("Invalid identifier")
        return value

    @classmethod
    def factory(cls, identifier, account_id=None, extra=None):
        self = cls()
        self.identifier = identifier
        self.account = g.current_account
        account_id = account_id or self.account.id
        self.status = 'creating'
        self.data = dict(
            DBInstanceIdentifier=identifier,
            DeletionProtection=False,
            Engine='postgres',
            EngineVersion='11',
            MultiAZ=False,
        )
        if extra:
            self.data.update(extra)
        region = current_app.config['REGION']
        self.data.update(dict(
            InstanceCreateTime=format_time(),
            DBInstanceArn=format_arn(
                service='rds',
                region=region,
                account_id=account_id,
                resource=f'db:{self.identifier}',
            ),
            Region=region,
            TenantHash=make_tenant_hash(account_id, region),
        ))
        return self

    def __str__(self):
        return f'instance #{self.id} {self.arn} ({self.status})'

    @property
    def recovery_end_callback(self):
        try:
            return self._recovery_end_callback
        except AttributeError:
            return canonical_url_for(
                'cornac.recovery_end_callback',
                _external=True,
                token=self.recovery_token,
            )

    @recovery_end_callback.setter
    def recovery_end_callback(self, value):
        self._recovery_end_callback = value

    def make_snapshot_identifier(self, date=None):
        if date is None:
            date = datetime.utcnow()
        return f'rds:{self.identifier}-{date:%Y-%m-%d-%H-%M}'


class DBSnapshot(db.Model):
    Status = db.ENUM(
        # Keep it sync with cornac/core/schema/003-snapshots.sql.
        'available',
        'creating',
        'deleted',
        'failed',
        name='db_instance_status',
    )

    # Keep it sync with cornac/core/schema/003-snapshots.sql.
    Type = db.ENUM('automated', 'manual', name='db_snapshot_type')

    __tablename__ = 'db_snapshots'
    __table_args__ = {'schema': 'cornac'}

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('cornac.accounts.id'))
    identifier = db.Column(db.String)
    status = db.Column(Status)
    status_message = db.Column(db.String)
    instance_id = db.Column(
        db.Integer, db.ForeignKey('cornac.db_instances.id'))
    data = db.Column(db.JSONB)
    type_ = db.Column('type', Type)
    iaas_data = db.Column(db.JSONB)
    operator_data = db.Column(db.JSONB)

    account = db.relationship(
        'Account',
        lazy='select',
        backref=db.backref('snapshots', lazy='select'),
    )

    instance = db.relationship(
        'DBInstance',
        # Always load corresponding instance of a snapshot, using a join.
        lazy='joined',
        # Reference all snapshots of an instance, but don't load them until
        # accessed.
        backref=db.backref('snapshots', lazy='select'),
    )

    class query_class(db.Query):
        def current(self):
            return self.filter(self.m.account == g.current_account)

    def __str__(self):
        return f'snapshot #{self.id} {self.arn}'

    @property
    def arn(self):
        return self.data['DBSnapshotArn']

    _instance_attr_whitelist = {
        'AllocatedStorage',
        'AvailabilityZone',
        'DBInstanceClass',
        'DBInstanceIdentifier',
        'Engine',
        'EngineVersion',
        'InstanceCreateTime',
        'MasterUsername',
        'StorageType',
    }

    @classmethod
    def factory(cls, instance, type_, identifier=None):
        self = cls()
        self.account = g.current_account
        self.status = 'creating'
        self.instance = instance
        self.type_ = type_
        if not identifier:
            identifier = instance.make_snapshot_identifier()
        self.identifier = identifier
        self.data = dict(
            {
                k: v for k, v in instance.data.items()
                if k in cls._instance_attr_whitelist
            },
            SnapshotCreateTime=format_time(),
            PercentProgress=0,
            XDBInstanceId=instance.id,
            Port=5432,
            DBSnapshotArn=format_arn(
                service='rds',
                region=current_app.config['REGION'],
                account_id=self.account_id or self.account.id,
                resource=f'snapshot:{self.identifier}',
            )
        )
        return self

    @property
    def siblings(self):
        cls = self.__class__
        return (
            cls.query
            .filter(cls.instance_id == self.instance_id)
            .filter(cls.id != self.id)
        )


class VirtualIPRange(db.Model):
    __tablename__ = 'virtual_ip_ranges'
    __table_args__ = {'schema': 'cornac'}
    __pkname__ = 'cornac.virtual_ip_ranges.id'

    id = db.Column(db.Integer, primary_key=True)
    range_ = db.Column('range', db.IPNetwork)
    comment = db.Column(db.String)

    @classmethod
    def allocate(cls, instance):
        result = db.session.execute(dedent("""\
        WITH addresses AS (
            SELECT
                r.id AS range_id,
                r.range + generate_series(
                    0, (2 ^ (32 - masklen(r.range)) - 1)::INTEGER
                ) AS "value"
            FROM cornac.virtual_ip_ranges AS r
        )
        SELECT
            addresses.range_id,
            addresses."value"::INET
        FROM addresses
        LEFT OUTER JOIN cornac.virtual_ip_allocations AS a
            ON a."address" = addresses."value"
        WHERE a.id IS NULL
        LIMIT 1
        """))
        row0 = result.fetchone()
        if not row0:
            raise KnownError("No virtual IP available.")
        range_id, address = row0
        allocation = VirtualIPAllocation(
            range_id=range_id,
            instance=instance,
            address=ip_interface(address),
        )
        db.session.add(allocation)
        return allocation

    def __len__(self):
        return self.range_.num_addresses

    def as_dict(self):
        return dict(
            id=self.id,
            range=str(self.range_),
            comment=self.comment,
            size=len(self),
            allocated=len(self.allocated_ips),
        )


class VirtualIPAllocation(db.Model):
    __tablename__ = 'virtual_ip_allocations'
    __table_args__ = {'schema': 'cornac'}
    __pkname__ = 'cornac.virtual_ip_allocations.id'

    id = db.Column(db.Integer, primary_key=True)
    range_id = db.Column(
        db.Integer, db.ForeignKey('cornac.virtual_ip_ranges.id'))
    instance_id = db.Column(
        db.Integer, db.ForeignKey('cornac.db_instances.id'))
    address = db.Column(db.IPAddress)

    instance = db.relationship(
        'DBInstance',
        # Lazy load DB instance attached to an IP. Especially when listing IPs
        # in a range.
        lazy='select',
        # Always load virtual_ips with DB instance. It's cheaper than lazy
        # select.
        backref=db.backref(
            'virtual_ips', cascade='all, delete-orphan', lazy='joined'),
    )

    range_ = db.relationship(
        'VirtualIPRange',
        # Always load associated range.
        lazy='joined',
        # Lazy load allocated IPs when loading a range.
        backref=db.backref('allocated_ips', lazy='select'),
    )

    def __repr__(self):
        return '<%s %s for #%s>' % (
            self.__class__.__name__,
            self.address, self.instance_id,
        )


class Identity(db.Model):
    __tablename__ = 'identities'
    __table_args__ = {'schema': 'cornac'}
    __pkname__ = 'cornac.identities.id'  # shorthand to build FK.

    Type = db.ENUM('group', 'role', 'user', name='identity_type')

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('cornac.accounts.id'))
    arn = db.Column(db.String)
    type = db.Column(Type)
    name = db.Column(db.String)
    reset_token = db.Column(db.String)
    reset_edate = db.Column(db.TIMESTAMP(timezone=True))
    data = db.Column(db.JSONB)

    account = db.relationship(
        'Account', lazy='select',
        backref=db.backref('identities', lazy='select'),
    )

    group_membership = db.Table(
        'group_memberships', db.Model.metadata,
        db.Column('group_id', db.Integer, db.ForeignKey(__pkname__)),
        db.Column('member_id', db.Integer, db.ForeignKey(__pkname__)),
        schema='cornac',
    )

    members = db.relationship(
        'Identity', lazy='select',
        secondary=group_membership,
        primaryjoin=(id == group_membership.c.group_id) & (type == 'group'),
        secondaryjoin=id == group_membership.c.member_id,
        backref=db.backref('groups', passive_deletes=True),
    )

    class query_class(db.Query):
        def groups(self):
            if g.get('current_account'):
                self = self.filter(self.m.account == g.current_account)
            return self.filter(self.m.type == 'group')

        def roles(self, account):
            return (
                self
                .filter(self.m.account == account)
                .filter(self.m.type == 'role')
            )

        def users(self):
            if g.get('current_account'):
                self = self.filter(self.m.account == g.current_account)
            return self.filter(self.m.type == 'user')

        def get_password_reset(self, token):
            return (
                self
                .filter(self.m.reset_token == token)
                .filter(self.m.reset_edate > db.func.current_timestamp())
                .one()
            )

    def __repr__(self):
        return '<%s #%s %s>' % (self.type, self.id, self.name)

    def __str__(self):
        return '%s %s' % (self.type, self.name)

    @property
    def is_admins(self):
        return 1 == self.id and 'group' == self.type

    @property
    def has_password(self):
        return 'PasswordHash' in self.data

    @classmethod
    def group_factory(cls, name):
        self = cls()
        self.account = g.current_account
        self.name = name
        self.type = 'group'
        self.update_arn()
        self.data = dict(
            GroupId=generate_id(prefix='CGPA'),
            CreateDate=format_time(),
        )
        return self

    @classmethod
    def role_factory(cls, name, account):
        self = cls()
        self.account = account
        self.name = name
        self.type = 'role'
        self.update_arn()
        self.data = dict(
            RoleId=generate_id(prefix='CROA'),
            CreateDate=format_time(),
        )
        return self

    @classmethod
    def user_factory(cls, name):
        self = cls()
        self.account = g.current_account
        self.name = name
        self.type = 'user'
        self.update_arn()
        self.data = dict(
            UserId=generate_id(prefix='CIDA'),
            CreateDate=format_time(),
        )

        # Apply hard coded policy to allow user to create self access keys.
        for v in 'Create', 'Delete', 'Update':
            ACL.allow(source=self, action=f'iam:{v}AccessKey', resource=self)
        # As well as seeing owns groups, changing own password.
        for action in 'ListAccessKeys', 'ListGroupsForUser', 'ChangePassword':
            ACL.allow(source=self, action=f'iam:{action}', resource=self)
        # Allow users to inspect their authorized accounts.
        ACL.allow(source=self, action='cornac:GetAccounts', resource='*')

        return self

    def check_password(self, password):
        if not self.has_password:
            return False
        h = hash_password(password, self.data['PasswordSalt'])
        return h == self.data['PasswordHash']

    def drop_password(self):
        for k in list(self.data.keys()):
            if k.startswith('Password'):
                del self.data[k]

    def make_reset_password_url(self):
        self.reset_token = generate_id(prefix='CPTA', length=28)
        self.reset_edate = utcnow() + timedelta(hours=1)
        return canonical_url_for(
            'cornac.reset_password', token=self.reset_token)

    def rename_to(self, new_name):
        oldarn = self.arn
        self.name = new_name
        self.update_arn()
        (
            ACL.query
            .filter(ACL.source == oldarn)
            .update({ACL.source: self.arn})
        )
        (
            ACL.query
            .filter(ACL.resource == oldarn)
            .update({ACL.resource: self.arn})
        )
        db.session.flush()

    def store_password(self, password):
        salt = generate_secret()
        self.data.update(
            PasswordSalt=salt,
            PasswordHash=hash_password(password, salt=salt),
            PasswordDate=format_time(),
        )
        # Invalidate reset token if any.
        self.reset_token = self.reset_edate = None

    def update_arn(self):
        self.arn = format_arn(
            service='iam',
            region='',
            account_id=self.account_id or self.account.id,
            resource=f'{self.type}/{self.name}'
        )
