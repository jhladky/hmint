import urllib
from flask import request, redirect, url_for
from functools import wraps
from flask.ext.login import current_user


def requires_login(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        if current_user.is_authenticated:
            return func(*args, **kwargs)
        return redirect(url_for('login', message='Login required.'))
    return wrapped
