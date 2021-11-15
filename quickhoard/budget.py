from flask import Blueprint, request, render_template, session
from quickhoard.db import Database

bp = Blueprint('budget', __name__)


@bp.route('/')
def index():
    if session.get('user_id') is None:
        return render_template('index.html')

    return render_template('dashboard.html')
