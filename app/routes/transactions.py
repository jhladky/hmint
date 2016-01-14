from flask import Blueprint, request, jsonify
from app.core import db
from app.utils import get_items
from app.api_decorators import requires_login, requires_keys
from app.models.transaction import Transaction

blueprint = Blueprint('transactions', __name__,
                      url_prefix='/api/transactions')


@blueprint.route('/', methods=['GET'])
def get():
    pass
