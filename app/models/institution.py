from app.core import db
from app.models.user import User


class Institution(db.Model):
    __tablename__ = 'institution'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
