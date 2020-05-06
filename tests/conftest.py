import os
#Temporary file module
import tempfile
#Unit and functional testing module
import pytest
from hobbyProjectWebsite import create_app
from hobbyProjectWebsite.db import init_db, db

@pytest.fixture
def app():
    #Provide the path to our testing database
    db_path = 'postgresql:///hobbyprojectwebsite_test'

    app = create_app({
        #Tell flask that the app is in test mode
        #This disable error catching so we get better error reports
        'TESTING': True,
        'CSRF_ENABLED': True,
        'SECRET_KEY': os.environ['SECRET_KEY'],
        'SQLALCHEMY_DATABASE_URI': db_path,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    with app.app_context():
        #Initialize the DB
        #This will drop tables, recreate tables, and fill in with default data
        #Note that this happens for EVERY test
        init_db(db)

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    #The user 'test' was inserted into our test DB initially
    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def loginAdmin(self, username='anthonyjacques20', password='testAdmin'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)