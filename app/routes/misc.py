from flask import Blueprint, request, jsonify
from app.decorators import requires_keys

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
