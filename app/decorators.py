from flask import jsonify, request
from functools import wraps
from flask.ext.login import current_user


def requires_login(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated():
            return jsonify(success=False, errors=['Login required.'])
        return func(*args, **kwargs)
    return wrapped


def requires_keys(*keys):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            errors = []
            json = request.get_json(force=True)
            key_set = set(keys)

            if not key_set.issubset(set(json.keys())):
                missing = key_set.difference(set(json.keys()))
                for expected in missing:
                    errors.append('Key `' + expected + '` must be specified.')
                return jsonify(success=False, errors=errors)
            else:
                return func(*args, **kwargs)
        return wrapped
    return wrapper
