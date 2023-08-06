from flask import make_response
from jinja2 import Environment, StrictUndefined


env = Environment(trim_blocks=True, undefined=StrictUndefined)


def booltostr(value):
    return 'true' if bool(value) is True else 'false'


env.filters['bool'] = booltostr


ERROR_TMPL = env.from_string("""\
<ErrorResponse>
   <Error>
      <Type>{{ type }}</Type>
      <Code>{{ awscode }}</Code>
      <Message>{{ message }}</Message>
   </Error>
   <RequestId>{{ requestid }}</RequestId>
</ErrorResponse>
""")


def make_error_xml(error, requestid):
    xml = ERROR_TMPL.render(
        code=error.code,
        message=error.description,
        awscode=error.awscode,
        requestid=requestid,
        type='Sender' if error.code < 500 else 'Receiver',
    )
    response = make_response(xml)
    response.status_code = error.code
    response.content_type = 'text/xml; charset=utf-8'
    response.headers['X-Amzn-RequestId'] = requestid
    return response


RESPONSE_TMPL = env.from_string("""\
<{{ action }}Response xmlns="{{ xmlns }}">
  <{{ action }}Result>
    {{ (result or '') | indent(4) }}
  </{{ action }}Result>
  <ResponseMetadata>
    <RequestId>{{ requestid }}</RequestId>
  </ResponseMetadata>
</{{ action }}Response>
""")


def make_response_xml(action, requestid, result, xmlns):
    # Wraps result XML snippet in response XML envelope.

    xml = RESPONSE_TMPL.render(**locals())
    response = make_response(xml)
    response.content_type = 'text/xml; charset=utf-8'
    response.headers['X-Amzn-RequestId'] = requestid
    return response
