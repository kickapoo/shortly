import functools
from flask import request
from .responses import status_406


def accepts_only_json_request(f):
    """
        Decorator for route to accept only application/json
        requests
    """
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return status_406()
        return f(*args, **kwargs)
    return decorated_function
