from os import environ
from ast import literal_eval
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.login import LoginManager

SQLALCHEMY_DATABASE_URI = environ['DATABASE_URL']
SECRET_KEY = environ['SECRET_KEY']
DEBUG = bool(environ.get('DEBUG', False))
TESTING = bool(environ.get('TESTING', False))

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
