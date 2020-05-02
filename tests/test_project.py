import pytest
from flask import g, session
from hobbyProjectWebsite.db import db
from hobbyProjectWebsite.models import User, Project, Comment
from flask_login import current_user

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
    #Check for the edit button since the logged in user wrote this test project
    assert b'href="/1/edit"' in response.data

@pytest.mark.parametrize('path',(
    '/create',
    '/1/edit',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    #After logging in we get redirected to the previous page with Flask-Login's next query parameter
    redirectLocation = response.headers['Location'].replace('%2F','/')
    assert redirectLocation == 'http://localhost/auth/login?next=' + path

def test_author_required(app, client, auth):
    #Change the project author to another user
    with app.app_context():
        db.engine.execute('UPDATE projects SET author_id = 2 WHERE id = 1')

    auth.login()
    #Current user can't modify other user's project
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

#Test that we can update a project
def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/edit').status_code == 200
    with app.app_context():
        project = db.engine.execute('SELECT * FROM projects WHERE id = 1').fetchone()

    print(project)
    print(project['body'])
    response = client.post(
        '/1/edit',
        data={
            'title': 'edited',
            'body': project['body'],
            'image': project['image'],
            'githuburl': project['githuburl'],
            'moreinfourl': project['moreinfourl']
        }
    )
    print(response)

    with app.app_context():
        project = db.engine.execute('SELECT * FROM projects WHERE id = 1').fetchone()
        assert project['title'] == 'edited'

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
    with app.app_context():
        #Confirm there is a comment
        assert db.session.query(Comment).filter(Comment.project_id == 1).count() == 1

    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'

    with app.app_context():
        #Confirm comments are deleted
        assert db.session.query(Comment).filter(Comment.project_id == 1).count() == 0
        #Confirm project is deleted
        project = db.engine.execute('SELECT * FROM projects WHERE id = 1').fetchone()
        assert project is None

def test_projects_nav(client):
    response = client.get('/')
    assert b'Projects' in response.data
    assert b'navbarDropdown' in response.data