from flask import jsonify, make_response


def api_response(status_code=200, message=None, errors=[], data=[]):
    """
        Status Generator
    """
    rv_data = dict(status_code=status_code, message=message, data=data,
                   errors=errors)
    return make_response(jsonify(rv_data), status_code)


def status_400(message=None, errors=[]):
    if not message:
        message = """ The request could not be understood
                      by the server due to malformed syntax.
                  """
    return api_response(400, message=message, errors=errors)


def status_404(message=None, errors=[]):
    if not message:
        message = """ The requested resource was not found.
                      This can be caused by an ACL constraint
                      or if the resource does not exist. """
    return api_response(404, message=message, errors=errors)


def status_406(message=None, errors=[]):
    if not message:
        message = """The endpoint does not support the response
                     format specified in the request Accept header."""
    if not errors:
        errors = [
            "Not acceptable"
        ]
    return api_response(406, message=message, errors=errors)


def status_200(message=None, data=[]):
    if not message:
        message = """Success"""
    return api_response(200, message=message, data=data)


def status_201(message=None, data=[]):
    if not message:
        message = """Created"""
    return api_response(201, message=message, data=data)


def status_418():
    return api_response(418, message="I'm a teapot")
