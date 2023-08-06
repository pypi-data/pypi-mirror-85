from textwrap import dedent

from ..xml import env
from ...utils import format_time


class CredentialsEncoder:
    XML = env.from_string(dedent("""\
    <Credentials>
      <AccessKeyId>{{ access_key.access_key }}</AccessKeyId>
      <SecretAccessKey>{{ secret }}</SecretAccessKey>
      <SessionToken>{{ access_key.session_token }}</SessionToken>
      <Expiration>{{ edate }}</Expiration>
    </Credentials>
    """))

    def __init__(self, access_key):
        self.access_key = access_key

    def as_xml(self):
        return self.XML.render(
            access_key=self.access_key,
            secret=self.access_key.data['SecretAccessKey'],
            edate=format_time(self.access_key.edate),
        )


class IdentityEncoder:
    XML = env.from_string(dedent("""\
    <Arn>{{ identity.arn }}</Arn>
    <UserId>{{ identity.data[id_key] }}</UserId>
    <Account>{{ account }}</Account>
    """))

    def __init__(self, identity):
        self.identity = identity

    def as_xml(self):
        return self.XML.render(
            identity=self.identity,
            id_key='UserId' if self.identity.type == 'user' else 'RoleId',
            account=f'{self.identity.account}',
        )
