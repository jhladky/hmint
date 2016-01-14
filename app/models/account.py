from app.core import db
from app.models.user import User
from app.models.institution import Institution
from app.models.account_category import AccountCategory
from app.exceptions import ItemNotFound
from sqlalchemy.exc import InvalidRequestError


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    user_id =  db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship('User')
    category_id = db.Column(db.Integer, db.ForeignKey(AccountCategory.id),
                            nullable=False)
    category = db.relationship('AccountCategory')
    institution_id = db.Column(db.Integer, db.ForeignKey(Institution.id),
                               nullable=False)
    institution = db.relationship('Institution')
    name = db.Column(db.String(50), nullable=False)
    maintenance_fee = db.Column(db.Numeric(precision=10, scale=4))
    minimum_balance = db.Column(db.Numeric(precision=10, scale=4))
    interest_rate = db.Column(db.Numeric(precision=10, scale=4))
    transactions = db.relationship('Transaction', backref='Account')

    def __init__(self, json):
        account_category = AccountCategory.query.get(json['category_id'])
        institution = Institution.query.get(json['institution_id'])

        if account_category is None:
            raise ItemNotFound('Specified account category does not exist.')

        if institution is None:
            raise ItemNotFound('Specified institution does not exist.')

        self.account_category = account_category
        self.institution = institution
        self.name = json['name']

    @property
    def serialize(self):
        # This is going to need to be fixed in the future,
        # based on what type of account it is
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.serialize,
            'institution': self.institution.serialize,
        }
