import pymysql.err
from flask import Blueprint, request, render_template, session, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from quickhoard.db import Database

bp = Blueprint('auth', __name__)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        database = Database()
        database.open()

        error = None

        if not email or not password:
            error = 'Email and password are required.'

        if error is None:
            try:
                database.execute("INSERT INTO user (`email`, `password`) VALUES (%s, %s)",
                                 (email, generate_password_hash(password)))
                database.commit()
            except pymysql.err.IntegrityError:
                error = 'Email is already registered.'
            else:
                flash('Registration successful! Please login.', 'alert-success')

                return redirect(url_for('auth.login'))

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
        user = result.fetchone()

        error = None

        if user is None or not check_password_hash(user['password'], password):
            error = 'Invalid credentials. Please try again.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']

            return redirect(url_for('index'))

        flash(error, 'alert-danger')

    return render_template('index.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
