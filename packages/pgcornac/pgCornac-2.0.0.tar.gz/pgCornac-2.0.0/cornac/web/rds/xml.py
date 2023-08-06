from textwrap import dedent

from ..xml import env, booltostr


INSTANCE_LIST_TMPL = env.from_string(dedent("""\
<DBInstances>
{% for instance in instances %}
  {{ instance.as_xml() | indent(2) }}
{% endfor %}
</DBInstances>
"""))


ORDERABLE_DB_INSTANCE_OPTIONS_LIST_TMPL = env.from_string(dedent("""\
<OrderableDBInstanceOptions>
{% for options in options_list %}
  {{ options.as_xml() | indent(2) }}
{% endfor %}
</OrderableDBInstanceOptions>
"""))


SNAPSHOT_LIST_TMPL = env.from_string(dedent("""\
<DBSnapshots>
{% for snapshot in snapshots %}
  {{ snapshot.as_xml() | indent(2) }}
{% endfor %}
</DBSnapshots>
"""))


class InstanceEncoder:
    # Adapt DBInstance object to RDS XML response.

    XML_SNIPPET_TMPL = env.from_string(dedent("""\
    <DBInstance>
      <DBInstanceIdentifier>{{ identifier }}</DBInstanceIdentifier>
      <Engine>postgres</Engine>
      <DBInstanceStatus>{{ status }}</DBInstanceStatus>
    {% if endpoint_address %}
      <Endpoint>
        <Address>{{ endpoint_address }}</Address>
        <Port>5432</Port>
      </Endpoint>
    {% endif %}
    {% for field in known_fields %}
      <{{ field }}>{{ data[field] }}</{{ field }}>
    {% endfor %}
    </DBInstance>
    """))

    def __init__(self, instance):
        self.instance = instance

    _known_fields = [
        'AllocatedStorage',
        'AvailabilityZone',
        'DBInstanceArn',
        'DBInstanceClass',
        'DeletionProtection',
        'PerformanceInsightsEnabled',
        'EngineVersion',
        'InstanceCreateTime',
        'LatestRestorableTime',
        'MasterUsername',
        'MultiAZ',
    ]

    def as_xml(self):
        data = self.instance.data or {}
        try:
            endpoint_address = data['Endpoint']['Address']
        except KeyError:
            endpoint_address = None

        data = {
            k: booltostr(v) if v in (True, False) else v
            for k, v in data.items()
        }
        known_fields = [
            h for h in self._known_fields
            if h in data]

        kw = dict(self.instance.__dict__, data=data)
        return self.XML_SNIPPET_TMPL.render(
            endpoint_address=endpoint_address,
            known_fields=known_fields,
            **kw,
        )


class OrderableDBInstanceOptions:
    XML_SNIPPET_TMPL = env.from_string(dedent("""\
    <OrderableDBInstanceOption>
      <Engine>postgres</Engine>
      <EngineVersion>{{ EngineVersion }}</EngineVersion>
      <ReadReplicaCapable>false</ReadReplicaCapable>
      <DBInstanceClass>{{ DBInstanceClass }}</DBInstanceClass>
      <AvailableProcessorFeatures/>
      <AvailabilityZones>
      {% for zone in AvailabilityZones %}
        <AvailabilityZone><Name>{{ zone }}</Name></AvailabilityZone>
      {% endfor %}
      </AvailabilityZones>
      <SupportsPerformanceInsights>{{ SupportsPerformanceInsights }}</SupportsPerformanceInsights>
      <LicenseModel>postgresql-license</LicenseModel>
      <MultiAZCapable>false</MultiAZCapable>
      <RequiresCustomProcessorFeatures>false</RequiresCustomProcessorFeatures>
      <MinStorageSize>5</MinStorageSize>
      <MaxStorageSize>3072</MaxStorageSize>
    </OrderableDBInstanceOption>
    """))  # noqa

    def __init__(self, **kw):
        self.kw = kw

    def as_xml(self):
        return self.XML_SNIPPET_TMPL.render(**self.kw)


class SnapshotEncoder:
    # Adapt DBSnapshot object to RDS XML response.

    XML_SNIPPET_TMPL = env.from_string(dedent("""\
    <DBSnapshot>
      <DBSnapshotIdentifier>{{ identifier }}</DBSnapshotIdentifier>
      <SnapshotType>{{ type_ }}</SnapshotType>
      <Engine>postgres</Engine>
      <Status>{{ status }}</Status>
    {% for field in known_fields %}
      <{{ field }}>{{ data[field] }}</{{ field }}>
    {% endfor %}
    </DBSnapshot>
    """))

    def __init__(self, snapshot):
        self.snapshot = snapshot

    _known_fields = [
        'AvailabilityZone',
        'DBInstanceIdentifier',
        'DBSnapshotArn',
        'AllocatedStorage',
        'SnapshotCreateTime',
        'InstanceCreateTime',
        'MasterUsername',
        'Port',
        'EngineVersion',
        'PercentProgress',
    ]

    def as_xml(self):
        data = self.snapshot.data or {}

        data = {
            k: booltostr(v) if v is True or v is False else v
            for k, v in data.items()
        }
        known_fields = [
            h for h in self._known_fields
            if h in data]
        kw = dict(self.snapshot.__dict__, data=data)
        return self.XML_SNIPPET_TMPL.render(
            known_fields=known_fields,
            **kw,
        )
