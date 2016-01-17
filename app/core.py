import pkgutil
import importlib
from os import environ
from ast import literal_eval
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.login import LoginManager

SQLALCHEMY_DATABASE_URI = environ['DATABASE_URL']
SECRET_KEY = environ['SECRET_KEY']
DEBUG = bool(environ.get('DEBUG', False))

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def register_blueprints(app, package_name, package_path):
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('.' + name, package_name)
        if hasattr(m, 'blueprint'):
            if DEBUG:
                print(' * Registering blueprint ' +
                      str(m.blueprint.import_name))
            app.register_blueprint(getattr(m, 'blueprint'))
