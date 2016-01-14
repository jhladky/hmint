import datetime
from app.core import db
from app.utils import unix_time
from app.models.user import User


class Institution(db.Model):
    __tablename__ = 'institution'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

    def __init__(self, json):
        self.name = json['name']
        self.create_date = datetime.datetime.now()

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'create_date': unix_time(self.create_date)
        }
