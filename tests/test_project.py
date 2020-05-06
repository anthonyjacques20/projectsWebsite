import pytest
from flask import g, session
from hobbyProjectWebsite.db import db
from hobbyProjectWebsite.models import User, Project, Comment
from flask_login import current_user

def test_index(client, auth):
    response = client.get('/projects/')
    #Make sure the log in and register buttons show up when no one is logged in
    assert b'Log In' in response.data
    assert b'Register' in response.data
    #Check for the edit button since the logged in user wrote this test project
    assert b'href="/projects/1/edit"' not in response.data


    auth.login()
    response = client.get('/projects/')
    #Once we are logged in, check if the log out button is visible
    assert b'Log Out' in response.data
    #Check the data
    assert b'test title' in response.data
    assert b'by anthonyjacques20 on 2018-01-01' in response.data
    assert b'test body' in response.data
    #Check for the edit button since the logged in user wrote this test project
    assert b'href="/projects/1/edit"' not in response.data

def test_index_admin(client, auth):
    auth.loginAdmin()
    response = client.get('/projects/')
    #Once we are logged in, check if the log out button is visible
    assert b'Log Out' in response.data
    #Check the data
    assert b'test title' in response.data
    assert b'by anthonyjacques20 on 2018-01-01' in response.data
    assert b'test body' in response.data
    #Check for the edit button since the logged in user wrote this test project
    assert b'href="/projects/1/edit"' in response.data



@pytest.mark.parametrize('path', (
    '/projects/1',
    '/projects/'
))
def test_edit_button(client, auth, path):
    auth.login()
    response = client.get(path)
    assert b'href="/projects/1/edit"' not in response.data

@pytest.mark.parametrize('path', (
    '/projects/1',
    '/projects/'
))
def test_edit_button_admin(client, auth, path):
    auth.loginAdmin()
    response = client.get(path)
    assert b'href="/projects/1/edit"' in response.data

@pytest.mark.parametrize('path',(
    '/projects/create',
    '/projects/1/edit',
    '/projects/1/delete',
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

    auth.loginAdmin()
    #Current user can't modify other user's project
    assert client.post('/projects/1/edit').status_code == 403
    assert client.post('/projects/1/delete').status_code == 403
    #Current user should not see edit link
    assert b'href="/projects/1/edit"' not in client.get('/projects/').data
    assert b'href="/projects/1/edit"' not in client.get('/projects/1').data

@pytest.mark.parametrize('path',(
    '/projects/2/edit',
    '/projects/2/delete',
))
#Return 404 if the post requested doesn't exist
def test_exists_required(client, auth, path):
    auth.loginAdmin()
    assert client.post(path).status_code == 404

#Confirm we can create a second post
def test_create(client, auth, app):
    auth.login()

    assert client.get('/projects/create').status_code == 403
    response = client.post(
        '/projects/create',
        data={'title': 'created', 'body': 'createdBody', 'image': '', 'githuburl': '', 'moreinfourl': ''},
    )

#Confirm we can create a second post
def test_create_admin(client, auth, app):
    auth.loginAdmin()

    assert client.get('/projects/create').status_code == 200
    response = client.post(
        '/projects/create',
        data={'title': 'created', 'body': 'createdBody', 'image': '', 'githuburl': '', 'moreinfourl': '', 'supportimages': ''},
    )

    with app.app_context():
        count = db.engine.execute('SELECT COUNT(id) FROM projects').fetchone()[0]
        assert count == 2

#Test that we can update a project
def test_update(client, auth, app):
    auth.loginAdmin()
    assert client.get('/projects/1/edit').status_code == 200
    with app.app_context():
        project = db.engine.execute('SELECT * FROM projects WHERE id = 1').fetchone()

    print(project)
    print(project['body'])
    response = client.post(
        '/projects/1/edit',
        data={
            'title': 'edited',
            'body': project['body'],
            'image': project['image'],
            'githuburl': project['githuburl'],
            'moreinfourl': project['moreinfourl'],
            'supportimages': project['supportimages']
        }
    )
    print(response)

    with app.app_context():
        project = db.engine.execute('SELECT * FROM projects WHERE id = 1').fetchone()
        assert project['title'] == 'edited'

#Show an error on invalid title/body data
@pytest.mark.parametrize('path', (
    '/projects/create',
    '/projects/1/edit',
))
def test_create_update_validate(client, auth, path):
    auth.loginAdmin()
    response = client.post(path, data={'title': '', 'body': '', 'image': 'image text', 'githuburl': 'github text', 'moreinfourl': 'more info url text', 'supportimages': 'supporimage1'})
    print(response, response.status_code)
    assert b'Title is required.' in response.data

def test_delete(client, auth, app):
    auth.login()
    with app.app_context():
        #Confirm there is a comment
        assert db.session.query(Comment).filter(Comment.project_id == 1).count() == 1

    response = client.post('/projects/1/delete')
    assert response.status_code == 403

def test_delete_admin(client, auth, app):
    auth.loginAdmin()
    with app.app_context():
        #Confirm there is a comment
        assert db.session.query(Comment).filter(Comment.project_id == 1).count() == 1

    response = client.post('/projects/1/delete')
    assert response.headers['Location'] == 'http://localhost/projects/'

    with app.app_context():
        #Confirm comments are deleted
        assert db.session.query(Comment).filter(Comment.project_id == 1).count() == 0
        #Confirm project is deleted
        project = db.engine.execute('SELECT * FROM projects WHERE id = 1').fetchone()
        assert project is None

def test_projects_nav(client):
    response = client.get('/projects/')
    assert b'Projects' in response.data
    assert b'navbarDropdown' in response.data