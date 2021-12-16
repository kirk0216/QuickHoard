from flask import session
from werkzeug.security import check_password_hash
from quickhoard.db import Database


def test_register(app, client):
    assert client.get('/register').status_code == 200

    response = client.post(
        '/register', data={'email': 'patkirk@testing.com', 'password': 'Welcome24!'}
    )

    with app.app_context():
        db = Database()
        db.open()

        result = db.query("SELECT * FROM qh.user WHERE email = %s;", 'patkirk@testing.com').fetchone()
        assert result is not None

        db.close()


def test_login(app, client):
    assert client.get('/login').status_code == 200

    response = client.post(
        '/login', data={'email': 'patkirk@testing.com', 'password': 'Welcome24!'}
    )

    with client:
        client.get('/')
        assert session['user_id'] == 1


def test_failed_login(app, client):
    response = client.post(
        '/login', data={'email': 'patkirk@testing.com', 'password': 'WrongPassword'}
    )

    assert response.status_code == 200

    with app.app_context():
        db = Database()
        db.open()

        result = db.query("SELECT failed_login FROM user WHERE email = %s;", 'patkirk@testing.com').fetchone()
        assert result['failed_login'] == 1

        db.close()


def test_passwordreset_generates_code(app, client):
    response = client.post(
        '/resetpassword',
        data={'email': 'patkirk@testing.com'},
        follow_redirects=True
    )

    with app.app_context():
        db = Database()
        db.open()

        result = db.query('SELECT * FROM user WHERE email = %s;', 'patkirk@testing.com').fetchone()
        assert result['reset_code'] is not None

        db.close()


def test_passwordreset_resets(app, client):
    with app.app_context():
        db = Database()
        db.open()

        # Set the reset code to a known value.
        reset_code = '123456789'
        db.execute('UPDATE user SET reset_code = %s WHERE email = %s;', (reset_code, 'patkirk@testing.com'))
        db.commit()

    response = client.post(
        '/resetpassword/123456789', data={'password': 'Welcome25!', 'confirm_password': 'Welcome25!'}
    )

    with app.app_context():
        db.open()
        result = db.query('SELECT password FROM user WHERE email = %s;', 'patkirk@testing.com').fetchone()
        actual = result['password']

        assert check_password_hash(actual, 'Welcome25!')

        db.close()


def test_logout(app, client):
    response = client.post(
        '/login', data={'email': 'patkirk@testing.com', 'password': 'Welcome24!'}
    )

    with client:
        client.get('/logout')
        assert 'user_id' not in session


def test_add_category(app, client):
    client.post(
        '/login',
        data={'email': 'patkirk@testing.com', 'password': 'Welcome25!'}
    )

    response = client.post(
        '/category/add',
        data={'name': 'Test', 'amount': '20.00'}
    )

    with app.app_context():
        db = Database()
        db.open()

        result = db.query('SELECT name FROM category WHERE id = 1;').fetchone()
        assert result is not None

        db.close()


def test_edit_category(app, client):
    client.post(
        '/login',
        data={'email': 'patkirk@testing.com', 'password': 'Welcome25!'}
    )

    response = client.post(
        '/category/edit',
        data={'category_id': 1, 'name': 'Testing', 'goal_id': 1, 'goal': '20.00'}
    )

    with app.app_context():
        db = Database()
        db.open()

        result = db.query('SELECT name FROM category WHERE id = 1;').fetchone()
        assert result['name'] == 'Testing'

        db.close()


def test_add_transaction(app, client):
    client.post(
        '/login',
        data={'email': 'patkirk@testing.com', 'password': 'Welcome25!'}
    )

    response = client.post(
        '/transaction/add',
        data={'date': '2021-12-12', 'recipient': 'Test Co.', 'category_id': 1, 'amount': '20.00'}
    )

    with app.app_context():
        db = Database()
        db.open()

        result = db.query('SELECT * FROM transaction WHERE id = 1;').fetchone()
        assert result is not None

        db.close()


def test_edit_transaction(app, client):
    client.post(
        '/login',
        data={'email': 'patkirk@testing.com', 'password': 'Welcome25!'}
    )

    response = client.post(
        '/transaction/edit',
        data={'id': 1, 'date': '2021-12-12', 'recipient': 'Test Co.', 'category_id': 1, 'amount': '20.00'}
    )

    with app.app_context():
        db = Database()
        db.open()

        result = db.query('SELECT * FROM transaction WHERE id = 1;').fetchone()
        assert result is not None

        db.close()


def test_delete_transaction(app, client):
    client.post(
        '/login',
        data={'email': 'patkirk@testing.com', 'password': 'Welcome25!'}
    )

    response = client.post(
        '/transaction/delete',
        data={'id': 1}
    )

    with app.app_context():
        db = Database()
        db.open()

        result = db.query('SELECT * FROM transaction WHERE id = 1;').fetchone()
        assert result is None

        db.close()


def test_delete_category(app, client):
    client.post(
        '/login',
        data={'email': 'patkirk@testing.com', 'password': 'Welcome25!'}
    )

    response = client.post(
        '/category/delete',
        data={'category_id': 1}
    )

    with app.app_context():
        db = Database()
        db.open()

        result = db.query('SELECT name FROM category WHERE id = 1;').fetchone()
        assert result is None

        db.close()
