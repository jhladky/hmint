from app.core import db
from app.models.user import User
from app.models.account_category import AccountCategory


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    user = db.relationship('User')
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    name = db.Column(db.String(50))
    category_id = db.column(db.Integer, db.ForeignKey(AccountCategory,id))
    category = db.relationship('AccountCategory')
