from flask import Blueprint, redirect, url_for, render_template, session
from quickhoard.db import Database

bp = Blueprint('budget', __name__)


@bp.route('/')
def index():
    if session.get('user_id') is None:
        return redirect(url_for('auth.login'))

    return render_template('dashboard.html')
