import pymysql.err
import uuid
from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from quickhoard.db import Database
from quickhoard.model.user import User

bp = Blueprint('auth', __name__)


# Http handler for registering a new user account
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


# Http handler for logging in to an existing user account
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

        # Check that the password provided by the user matches the password for the user account.
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


# Http handler for logging out of a user account
@bp.route('/logout')
def logout():
    # Just clear the session and redirect the user back to the main page
    session.clear()
    return redirect(url_for('index'))


# Http handler for resetting a user password
# code is a randomly generated code the user must provide to reset their password
@bp.route('/resetpassword/', methods=('GET', 'POST'))
@bp.route('/resetpassword/<code>', methods=('GET', 'POST'))
def reset_password(code=None):
    # Resetting a password is a two step process:
    # 1. Request a password reset, which generates a code the user must provide to perform the actual reset.
    # 2. Enter the code and a new password, to update the password

    # Step 1: Requesting a code
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

            # In a real application, this would be emailed or SMSed to the user.
            # To avoid incurring the costs associated with using an email or SMS service, the code is generated and
            #   displayed in a pop-up message instead.
            flash(f'Your reset code is %s' % reset_code, 'alert-info')

            database.close()

        return render_template('resetpassword.html', request_code=True)
    # Step 2: Submitting the password change request with the generated code
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
