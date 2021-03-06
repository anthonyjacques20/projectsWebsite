import pytest
from flask import g, session
from hobbyProjectWebsite.db import db
from flask_login import current_user

def test_register(client, app):
    #Make sure the page responds with status of 200
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'password': 'a'}
    )
    print(response)
    #On a successful register, we get redirected to the login page
    #response.headers will have a `Location` header when the register view redirects to the login view
    assert 'http://localhost/auth/login' == response.headers['Location']

    with app.app_context():
        assert db.engine.execute(
            "SELECT * FROM users WHERE username = 'a'",
        ).first() is not None

#Tell pytest to run the same test function with different arguments
@pytest.mark.parametrize(('username', 'password', 'message'),(
    ('', '', b'Username is required.'),
    ('a', '', b'Password is required.'),
    ('test', 'test', b'already registered'),
))
def test_register_validate_input(client, username, password, message):
    response = client.post(
        '/auth/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    print(response)
    print(response.status_code)
    print(response.headers)
    assert response.headers['Location'] == 'http://localhost/'

    with client:
        client.get('/')
        assert current_user.id == 1
        assert current_user.username == 'test'

@pytest.mark.parametrize(('username', 'password', 'message'),(
    ('a', 'test', b'Incorrect username.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session

