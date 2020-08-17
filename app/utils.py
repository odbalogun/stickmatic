from flask import jsonify, make_response

JSON_MIME_TYPE = 'application/json'


def msisdn_formatter(msisdn):
    """
    Formats the number to the International format with the Nigerian prefix
    """
    # remove + and spaces
    msisdn = str(msisdn).replace('+', '').replace(' ', '')

    if msisdn[:3] == '234':
        return msisdn

    if msisdn[0] == '0':
        msisdn = msisdn[1:]
    return f"234{msisdn}"


def json_response(data=None, status=200, headers=None):
    headers = headers or {}
    if 'Content-Type' not in headers:
        headers['Content-Type'] = JSON_MIME_TYPE

    if data:
        payload = jsonify(data)
    else:
        payload = ''

    return make_response(payload, status, headers)


def response_error(code, message, status=400):
    return json_response(data={'code': code, 'error': message}, status=status)
