import os
#Temporary file module
import tempfile
#Unit and functional testing module
import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    #Create and return a temporary unique file for our database file
    #As opposed to our instance/flaskr.sqlite file
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        #Tell flask that the app is in test mode
        'TESTING': True,
        #Override the db_path with the new path of the temporary file
        'DATABASE': db_path,
    })

    with app.app_context():
        #Initialize the DB
        init_db()
        #Ge the database and add our data in tests/data.sql
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)

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

    def logout(self):
        return self._client.get('/auth/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)