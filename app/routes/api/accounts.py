from flask import Blueprint, request, jsonify
from flask.ext.login import current_user
from app.core import db
from app.utils import get_item, get_items
from app.api_decorators import requires_login, requires_keys, requires_debug
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
    return jsonify(success=True, account_id=account.id)


@blueprint.route('/<int:id>/', methods=['PUT'])
@requires_login
@requires_keys('category', 'institution', 'name')
def edit(id):
    pass


@blueprint.route('/fake/', methods=['POST'])
@requires_debug
def fake():
    json = {
        'name': '',
        'category': '',
        'institution': ''
    }

    # We're going to have to create so much to just get this to work
    # 1. Account Categories (Can just initially by the first
    # 5 or 10 that come to mind)
    # 2. Random institutions
    # 3. Then rewrite account based on the ACCOUNT_CATEGORY!

    return jsonify(success=True, account_id=account.id)
