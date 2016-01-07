from flask import Flask, g, render_template
from flask.ext.login import current_user
from core import db, login_manager,\
    DEBUG, TESTING, SQLALCHEMY_DATABASE_URI
from models.user import User

app = Flask(__name__)

app.config.update(
    SQLALCHEMY_DATABASE_URI=SQLALCHEMY_DATABASE_URI,
    DEBUG=DEBUG,
    TESTING=TESTING
)

db.init_app(app)
login_manager.init_app(app)


@app.route('/')
def slash():
    return render_template('index.html')


@app.before_request
def before_request():
        g.user = current_user


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
