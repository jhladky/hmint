from flask import Flask, g, jsonify
from flask.ext.login import current_user
from core import db, migrate, login_manager, register_blueprints,\
    DEBUG, SQLALCHEMY_DATABASE_URI, SECRET_KEY
from exceptions import AppError
import routes
import routes.api

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
    SECRET_KEY=SECRET_KEY,
    DEBUG=DEBUG
)

db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)
register_blueprints(app, 'app.routes.api', routes.api.__path__)
register_blueprints(app, 'app.routes', routes.__path__)


@app.errorhandler(AppError)
def handle_app_error(error):
    response = jsonify(error.serialize)
    response.status_code = error.status_code
    return response


@app.before_request
def before_request():
    g.user = current_user
