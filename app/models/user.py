from werkzeug import generate_password_hash
from app.core import db
from flask.ext.login import UserMixin
from itsdangerous import URLSafeTimedSerializer


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(50), nullable=False)


    def __init__(self, json):
        self.email = json['email']
        self.password = generate_password_hash(json['password'])
        self.name = json['name']

    # Flask-Login methods
    def get_auth_token(self):
        """Returns the user's authentication token."""
        data = [unicode(self.id), self.password]
        return login_serializer.dumps(data)

    def is_authenticated(self):
        return True
