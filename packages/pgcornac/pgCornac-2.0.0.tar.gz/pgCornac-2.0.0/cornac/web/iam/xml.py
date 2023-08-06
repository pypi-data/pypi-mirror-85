from textwrap import dedent

from ..xml import env


class AccessKeyEncoder:
    XML = env.from_string(dedent("""\
    <AccessKey>
      {{ metadata.as_xml() | indent(2) }}
      {% if secret %}
      <SecretAccessKey>{{ secret }}</SecretAccessKey>
      {% endif %}
    </AccessKey>
    """))

    def __init__(self, access_key):
        self.access_key = access_key

    def as_xml(self, with_secret=False):
        return self.XML.render(
            metadata=AccessKeyMetadataEncoder(self.access_key),
            secret=with_secret and self.access_key.data['SecretAccessKey'],
        )


class AccessKeyMetadataEncoder:
    XML = env.from_string(dedent("""\
    <AccessKeyId>{{ access_key }}</AccessKeyId>
    <UserName>{{ username }}</UserName>
    <Status>{{ status  }}</Status>
    <CreateDate>{{ cdate }}</CreateDate>
    """))

    def __init__(self, access_key):
        self.access_key = access_key

    def as_xml(self):
        return self.XML.render(
            access_key=self.access_key.access_key,
            cdate=self.access_key.data['CreateDate'],
            status=self.access_key.status,
            username=self.access_key.identity.name,
        )


class AccessKeysListEncoder:
    XML = env.from_string(dedent("""\
    <IsTruncated>false</IsTruncated>
    <AccessKeyMetadata>
      {% for access_key in access_keys %}
      <member>
        {{ access_key.as_xml() | indent(2) }}
      </member>
      {% endfor %}
    </AccessKeyMetadata>
    """))

    def __init__(self, access_keys):
        self.access_keys = access_keys

    def as_xml(self):
        return self.XML.render(
            access_keys=[AccessKeyMetadataEncoder(k)
                         for k in self.access_keys],
        )


#       L O G I N   P R O F I L E

class LoginProfileEncoder:
    XML = env.from_string(dedent("""\
    <LoginProfile>
      <UserName>{{ user.name }}</UserName>
      <PasswordResetRequired>false</PasswordResetRequired>
      <CreateDate>{{ user.data['PasswordDate'] }}</CreateDate>
    </LoginProfile>
    """))

    def __init__(self, user):
        self.user = user

    def as_xml(self):
        return self.XML.render(user=self.user)


#       G R O U P S

class GroupFieldsEncoder:

    XML = env.from_string(dedent("""\
    <Path>/</Path>
    <GroupName>{{ group.name }}</GroupName>
    <Arn>{{ group.arn }}</Arn>
    <GroupId>{{ group.data['GroupId'] }}</GroupId>
    <CreateDate>{{ group.data['CreateDate'] }}</CreateDate>
    """))

    def __init__(self, group):
        self.group = group

    def as_xml(self):
        return self.XML.render(group=self.group)


class GroupListEncoder:
    XML = env.from_string(dedent("""\
    <IsTruncated>false</IsTruncated>
    <Groups>
      {% for group in groups %}
      <member>
        {{ group.as_xml() | indent(4) }}
      </member>
      {% endfor %}
    </Groups>
    """))

    def __init__(self, groups):
        self.groups = groups

    def as_xml(self):
        return self.XML.render(
            groups=(GroupFieldsEncoder(g) for g in self.groups),
        )


#       P O L I C Y

class PolicyResultsEncoder:
    XML = env.from_string(dedent("""\
    <IsTruncated>false</IsTruncated>
    <EvaluationResults>
      {% for result in results %}
      <member>
        {% if result.statements %}
        <MatchedStatements>
          {% for statement in result.statements %}
          <member>
            <SourcePolicyId>{{ statement }}</SourcePolicyId>
          </member>
          {% endfor %}
        </MatchedStatements>
        {% endif %}
        <MissingContextValues/>
        <EvalResourceName>{{ result.resource }}</EvalResourceName>
        <EvalDecision>{{ result.decision }}</EvalDecision>
        <EvalActionName>{{ result.action }}</EvalActionName>
      </member>
      {% endfor %}
    </EvaluationResults>
    """))

    def __init__(self, results):
        self.results = results

    def as_xml(self):
        return self.XML.render(results=self.results)


#       U S E R

class UserEncoder:
    XML = env.from_string(dedent("""\
    <User>
      {{ fields.as_xml() | indent(2) }}
    </User>
    """))

    def __init__(self, user):
        self.user = user

    def as_xml(self):
        return self.XML.render(fields=UserFieldsEncoder(self.user))


class UserFieldsEncoder:
    XML = env.from_string(dedent("""\
    <Path>/</Path>
    <UserName>{{ user.name }}</UserName>
    <Arn>{{ user.arn }}</Arn>
    <UserId>{{ user.data['UserId'] }}</UserId>
    <CreateDate>{{ user.data['CreateDate'] }}</CreateDate>
    """))

    def __init__(self, user):
        self.user = user

    def as_xml(self):
        return self.XML.render(
            user=self.user,
        )


class UserListEncoder:
    XML = env.from_string(dedent("""\
    <IsTruncated>false</IsTruncated>
    <Users>
      {% for user in users %}
      <member>
        {{ user.as_xml() | indent(2) }}
      </member>
      {% endfor %}
    </Users>
    """))

    def __init__(self, users):
        self.users = users

    def as_xml(self):
        return self.XML.render(
            users=[UserFieldsEncoder(u) for u in self.users],
        )
