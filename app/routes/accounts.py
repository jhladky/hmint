from flask import Blueprint, request, jsonify
from app.core import db
from app.utils import get_items
from app.api_decorators import requires_login, requires_keys
from app.models.account import Account


blueprint = Blueprint('accounts', __name__, url_prefix='/api/accounts')


@blueprint.route('/', methods=['GET'])
@requires_login
def get_all():
    return jsonify(get_items(Account, request))


@blueprint.route('/<int:id>/', methods=['GET'])
@requires_login
def get(id):
    return jsonify(get_item(id, Account))


@blueprint.route('/', methods=['POST'])
@requires_login
@requires_keys('category', 'institution', 'name')
def new():
    json = request.get_json(force=True)
    errors = []
    account_id = None

    return jsonify(errors=errors, success=not errors, account_id=account_id)
