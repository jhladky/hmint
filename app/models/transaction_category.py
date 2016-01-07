from app.core import db


class TransactionCategory(db.Model):
    __tablename__ = 'transaction_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
