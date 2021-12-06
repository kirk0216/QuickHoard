import pymysql.err
import re, uuid
from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from quickhoard.db import Database

bp = Blueprint('auth', __name__)


class User:
    def __init__(self, email=None, password=None):
        self.id = None
        self.email = email
        self.password = password
        self.failed_login = 0
        self.last_login = None

    def parse(self, result):
        if result is None:
            return

        self.id = result['id']
        self.email = result['email']
        self.password = result['password']
        self.failed_login = result['failed_login']
        self.last_login = result['last_login']

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

        result = database.query("SELECT id, email, password, failed_login, last_login FROM user WHERE email = %s;", email)

        user = User()
        user.parse(result.fetchone())

        error = None

        if user is None or user.failed_login >= 5:
            error = 'Invalid credentials. Please try again.'

        if not check_password_hash(user.password or '', password):
            error = 'Invalid credentials. Please try again.'

            sql = (
                'UPDATE user SET '
                'failed_login = %s WHERE email = %s;'
            )

            database.execute(sql, (user.failed_login + 1, email))
            database.commit()

        if error is None:
            session.clear()
            session['user_id'] = user.id

            sql = (
                'UPDATE user SET failed_login = 0, last_login = CURRENT_TIMESTAMP WHERE email = %s;'
            )

            database.execute(sql, email)
            database.commit()

            database.close()

            return redirect(url_for('index'))

        flash(error, 'alert-danger')

        database.close()

    return render_template('index.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@bp.route('/resetpassword/', methods=('GET', 'POST'))
@bp.route('/resetpassword/<code>', methods=('GET', 'POST'))
def reset_password(code=None):
    if code is None:
        if request.method == 'POST':
            email = request.form['email'] if 'email' in request.form else None

            sql = (
                'UPDATE user SET reset_code = %s WHERE email = %s;'
            )

            database = Database()
            database.open()

            reset_code = uuid.uuid4()

            database.execute(sql, (reset_code, email))
            database.commit()

            flash(f'Your reset code is %s' % reset_code, 'alert-info')

            database.close()

        return render_template('resetpassword.html', request_code=True)
    else:
        if request.method == 'POST':
            password = request.form['password'] if 'password' in request.form else None
            confirm_password = request.form['confirm_password'] if 'confirm_password' in request.form else None

            if password is not None and confirm_password is not None and password == confirm_password:
                hash_password = generate_password_hash(password)

                database = Database()
                database.open()

                sql = (
                    'UPDATE user SET password = %s, failed_login = 0, reset_code = NULL '
                    'WHERE reset_code = %s;'
                )

                database.execute(sql, (hash_password, code))
                database.commit()

                database.close()

                return redirect(url_for('index'))

        return render_template('resetpassword.html', request_code=False)
