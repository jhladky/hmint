from flask import Blueprint, request, render_template, redirect, url_for
from flask.ext.login import current_user, logout_user
from app.core import login_manager
from app.decorators import requires_login
from app.models.user import User

blueprint = Blueprint('slash', __name__, url_prefix='')


@blueprint.route('/')
@requires_login
def overview():
    return render_template('overview.html')


@blueprint.route('/login/')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('overview'))
    return render_template('login.html')


@blueprint.route('/logout/')
@requires_login
def logout():
    logout_user()
    return redirect(url_for('login'))


@blueprint.route('/transactions/')
@requires_login
def transactions():
    return render_template('transactions.html')


@blueprint.route('/bills/')
@requires_login
def bills():
    return render_template('bills.html')


@blueprint.route('/budgets/')
@requires_login
def budgets():
    return render_template('budgets.html')


@blueprint.route('/goals/')
@requires_login
def goals():
    return render_template('goals.html')


@blueprint.route('/graphs/')
@requires_login
def graphs():
    return render_template('graphs.html')


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)
