import pymysql.err
import re
from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from quickhoard.db import Database

bp = Blueprint('auth', __name__)


class User:
    def __init__(self, email=None, password=None):
        self.id = None
        self.email = email
        self.password = password

    def parse(self, result):
        if result is None:
            return

        self.id = result['id']
        self.email = result['email']
        self.password = result['password']

    def is_valid(self):
        error = None

        if not self.email or not self.password:
            error = 'Email and password are required.'
        elif len(self.password) < 8:
            error = 'Password must be at least 8 characters long.'

        has_letter = re.search(r'\w', self.password) is not None
        has_number = re.search(r'\d', self.password) is not None
        has_special = re.search(r'\W', self.password) is not None

        if not has_letter or not has_number or not has_special:
            error = 'Password is not complex enough. Please include at least 1 letter, 1 number, ' \
                    'and 1 special character (!, @, #, or $).'

        return error is None, error


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        user = User(request.form['email'], request.form['password'])

        database = Database()
        database.open()

        valid, error = user.is_valid()

        if valid:
            try:
                user_id = database.insert("INSERT INTO user (`email`, `password`) VALUES (%s, %s)",
                                 (user.email, generate_password_hash(user.password)))
            except pymysql.err.IntegrityError:
                error = 'Email is already registered.'
            else:
                session.clear()
                session['user_id'] = user_id

                return redirect(url_for('index'))
            finally:
                database.close()

        flash(error, 'alert-danger')

    return render_template('index.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        database = Database()
        database.open()

        result = database.query("SELECT id, email, password FROM user WHERE email = %s;", email)

        user = User()
        user.parse(result.fetchone())

        database.close()

        error = None

        if user is None or not check_password_hash(user.password or '', password):
            error = 'Invalid credentials. Please try again.'

        if error is None:
            session.clear()
            session['user_id'] = user.id

            return redirect(url_for('index'))

        flash(error, 'alert-danger')

    return render_template('index.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
