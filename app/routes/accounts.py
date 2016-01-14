from flask import Blueprint, request, jsonify
from flask.ext.login import current_user
from app.core import db
from app.utils import get_items
from app.api_decorators import requires_login, requires_keys
from app.models.account import Account
from app.models.account_category import AccountCategory
from app.models.institution import Institution


blueprint = Blueprint('accounts', __name__, url_prefix='/api/accounts')


@blueprint.route('/', methods=['GET'])
@requires_login
def get_all():
    return jsonify(get_items(Account, request, current_user))


@blueprint.route('/<int:id>/', methods=['GET'])
@requires_login
def get(id):
    return jsonify(get_item(id, Account, current_user))


@blueprint.route('/', methods=['POST'])
@requires_login
@requires_keys('category_id', 'institution_id', 'name')
def new():
    account = Account(request.get_json(force=True))
    db.session.add(account)
    db.session.commit()
    return jsonify(errors=[], success=True, account_id=account.id)


@blueprint.route('/<int:id>/', methods=['PUT'])
@requires_login
@requires_keys('category', 'institution', 'name')
def edit(id):
    pass
