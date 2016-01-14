from app.core import db
from app.models.user import User
from app.models.account import Account
from app.models.transaction_category import TransactionCategory


class Transaction(db.Model):
    __tablename__ = 'transaction'
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship('User')
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200))
    occurrence_date = db.Column(db.DateTime())
    booking_date = db.Column(db.DateTime())
    amount = db.Column(db.Numeric(precision=10, scale=4))
    is_credit = db.Column(db.Boolean())
    category_id = db.Column(db.Integer, db.ForeignKey(TransactionCategory.id))
    category = db.relationship('TransactionCategory')
    account_id = db.Column(db.Integer, db.ForeignKey(Account.id))
    account = db.relationship('Account')
