from flask import jsonify, request
from functools import wraps
from flask.ext.login import current_user
from app.core import DEBUG
from app.exceptions import IdError


def requires_login(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        else:
            return jsonify(success=False, errors=['Login required.'])
    return wrapped


def requires_keys(*keys):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            errors = []
            json = request.get_json(force=True)
            key_set = set(keys)

            for key in json:
                if key.endswith('_id'):
                    try:
                        int(json[key])
                    except ValueError:
                        raise IdError(key)

            if not key_set.issubset(set(json.keys())):
                missing = key_set.difference(set(json.keys()))
                for expected in missing:
                    errors.append('`' + expected + '` must be specified')
                return jsonify(success=False, errors=errors)
            else:
                return func(*args, **kwargs)
        return wrapped
    return wrapper


def requires_debug(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if not DEBUG:
            return abort(404)
        return func(*args, **kwargs)
    return wrapped
