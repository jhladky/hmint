from app.core import db
from app.models.user import User
from app.models.institution import Institution
from app.models.account_category import AccountCategory


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
        self.category = AccountCategory.query.\
                        filter_by(name=json['category']).first()
        self.institution = Institution.query.\
                           filter_by(name=json['institution']).first()
        self.name = json['name']

    @property
    def serialize(self):
        # This is going to need to be fixed in the future
        return {
            'id': self.id,
            'category': self.category.name,
            'institution': self.institution.name,
        }
