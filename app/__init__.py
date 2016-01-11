import pkgutil
import importlib
from flask import Flask, g, render_template
from flask.ext.login import current_user
from core import db, migrate, login_manager,\
    DEBUG, TESTING, SQLALCHEMY_DATABASE_URI
from models.user import User
import routes

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
    DEBUG=DEBUG,
    TESTING=TESTING
)


def register_blueprints(app, package_name, package_path):
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('.' + name, package_name)
        app.register_blueprint(getattr(m, 'blueprint'))

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
register_blueprints(app, 'app.routes', routes.__path__)


@app.route('/')
def slash():
    return render_template('index.html')


@app.before_request
def before_request():
        g.user = current_user


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
