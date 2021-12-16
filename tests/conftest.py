import pytest
from quickhoard import create_app


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'MYSQL_DATABASE_DB': 'qhtest'
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()