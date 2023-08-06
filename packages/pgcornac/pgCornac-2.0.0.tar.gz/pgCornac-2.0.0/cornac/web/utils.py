from flask.json import jsonify as plain_jsonify


def jsonify(status=200, **kw):
    response = plain_jsonify(**kw)
    response.status_code = status
    return response


def resolve_payload_arrays(payload):
    """Groups all X.member.Y entries in a X list."""
    payload = payload.copy()
    keys = sorted(k for k in payload if '.member.' in k)
    for k in keys:
        value = payload.pop(k)
        argument, _, index = k.partition('.member.')
        index = int(index)
        array = payload.setdefault(argument, [])
        if index != (len(array) + 1):
            raise ValueError(f"Missing item before {index} in {argument}")
        array.append(value)
    return payload
