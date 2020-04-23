import pytest
from flask import g, session
from hobbyProjectWebsite.db import db

def test_index(client, auth):
    response = client.get('/')
    #Make sure the log in and register buttons show up when no one is logged in
    assert b'Log In' in response.data
    assert b'Register' in response.data

    auth.login()
    response = client.get('/')
    #Once we are logged in, check if the log out button is visible
    assert b'Log Out' in response.data
    #Check the data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test body' in response.data
    #Check for the edit button since the logged in user wrote this test post
    assert b'href="/1/edit"' in response.data

@pytest.mark.parametrize('path',(
    '/create',
    '/1/edit',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'

def test_author_required(app, client, auth):
    #Change the post author to another user
    with app.app_context():
        db.engine.execute('UPDATE projects SET author_id = 2 WHERE id = 1')

    auth.login()
    #Current user can't modify other user's post
    assert client.post('/1/edit').status_code == 403
    assert client.post('/1/delete').status_code == 403
    #Current user should not see edit link
    assert b'href="/1/edit"' not in client.get('/').data

@pytest.mark.parametrize('path',(
    '/2/edit',
    '/2/delete',
))
#Return 404 if the post requested doesn't exist
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404

#Confirm we can create a second post
def test_create(client, auth, app):
    auth.login()

    assert client.get('/create').status_code == 200
    response = client.post(
        '/create',
        data={'title': 'created', 'body': 'createdBody', 'image': '', 'githuburl': '', 'moreinfourl': ''},
    )

    with app.app_context():
        count = db.engine.execute('SELECT COUNT(id) FROM projects').fetchone()[0]
        assert count == 2

#Test that we can update a post
def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/edit').status_code == 200
    with app.app_context():
        post = db.engine.execute('SELECT * FROM projects WHERE id = 1').fetchone()

    print(post)
    print(post['body'])
    response = client.post(
        '/1/edit',
        data={
            'title': 'edited',
            'body': post['body'],
            'image': post['image'],
            'githuburl': post['githuburl'],
            'moreinfourl': post['moreinfourl']
        }
    )
    print(response)

    with app.app_context():
        post = db.engine.execute('SELECT * FROM projects WHERE id = 1').fetchone()
        assert post['title'] == 'edited'

#Show an error on invalid title/body data
@pytest.mark.parametrize('path', (
    '/create',
    '/1/edit',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': '', 'image': 'image text', 'githuburl': 'github text', 'moreinfourl': 'more info url text'})
    print(response, response.status_code)
    assert b'Title is required.' in response.data

def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        post = db.engine.execute('SELECT * FROM projects WHERE id = 1').fetchone()
        assert post is None