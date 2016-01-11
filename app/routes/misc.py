from flask import Blueprint, request, jsonify
from werkzeug import check_password_hash
from flask.ext.login import login_user, logout_user
from app.core import db
from app.decorators import requires_login, requires_keys
from app.models.user import User

blueprint = Blueprint('misc', __name__, url_prefix='/api')


@blueprint.route('/login/', methods=['POST'])
@requires_keys('email', 'password')
def login():
    errors = []
    json = request.get_json(force=True)
    user = User.query.filter_by(email=json['email']).first()

    if user is None:
        errors.append('Invalid username/password combination.')

    if not errors and not check_password_hash(user.password, json['password']):
        errors.append('Invalid username/password combination.')

    if not errors:
        login_user(user, remember=False)

    return jsonify(success=not errors, errors=errors)


@blueprint.route('/logout/', methods=['GET'])
@requires_login
def logout():
    logout_user()
    return jsonify(success=True)


@blueprint.route('/register/', methods=['POST'])
# Need to add challenge / response captcha stuff in later
# @requires_keys('email', 'password', 'confirm', 'challenge', 'response')
@requires_keys('email', 'name', 'password', 'confirm')
def register():
    json = request.get_json(force=True)
    errors = []
    user_id = None

    # captcha_result = submit(json['challenge'], json['response'],
    #                         RECAPTCHA_PRIVATE_KEY, request.remote_addr)
    # if not captcha_result.is_valid:
    #     errors.append('captcha: Validation failed.')

    if not errors:
        if User.query.filter_by(email=json['email']).first():
            errors.append('An account already exists with this email.')

        # Need better password requirements later
        if len(json['password']) < 6:
            errors.append('Password must be at least 6 characters long.')

        if json['password'] != json['confirm']:
            errors.append('Passwords do not match.')

    if not errors:
        user = User(json)
        db.session.add(user)
        db.session.commit()
        user_id = user.id
        login_user(user)

    return jsonify(success=not errors, errors=errors, id=user_id)
