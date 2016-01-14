import pkgutil
import importlib
from flask import Flask, g, render_template, redirect, url_for, jsonify
from flask.ext.login import current_user
from core import db, migrate, login_manager,\
    DEBUG, TESTING, SQLALCHEMY_DATABASE_URI, SECRET_KEY
from models.user import User
from decorators import requires_login
from exceptions import ItemNotFound
import routes

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
    SECRET_KEY=SECRET_KEY,
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


@app.route('/login/')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('overview'))
    return render_template('login.html')


@app.route('/')
@requires_login
def overview():
    return render_template('overview.html')


@app.route('/transactions/')
@requires_login
def transactions():
    return render_template('transactions.html')


@app.route('/bills/')
@requires_login
def bills():
    return render_template('bills.html')


@app.route('/budgets/')
@requires_login
def budgets():
    return render_template('budgets.html')


@app.route('/goals/')
@requires_login
def goals():
    return render_template('goals.html')


@app.route('/graphs/')
@requires_login
def graphs():
    return render_template('graphs.html')


@app.errorhandler(ItemNotFound)
def handle_item_not_found(error):
    response = jsonify(error.serialize)
    response.status_code = error.status_code
    return response


@app.before_request
def before_request():
        g.user = current_user


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
