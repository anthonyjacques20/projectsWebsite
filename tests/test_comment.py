import pytest
from flask import g, session
from hobbyProjectWebsite.db import db
from hobbyProjectWebsite.models import User, Project, Comment
from flask_login import current_user

def test_index(client, auth):
    response = client.get('/1')
    #Make sure the test comment shows up
    assert b'test comment' in response.data
    assert b'by test on 2021-02-02 00:00' in response.data

@pytest.mark.parametrize('path',(
    '/1/comments/',
    '/1/comments/1/edit',
    '/1/comments/1/delete',
))
def test_comment_login_required(client, path):
    response = client.post(path)
    #After logging in we get redirected to the previous page with Flask-Login's next query parameter
    redirectLocation = response.headers['Location'].replace('%2F','/')
    assert redirectLocation == 'http://localhost/auth/login?next=' + path

def test_comment_author_required(app, client, auth):
    #Change the project author to another user
    with app.app_context():
        db.engine.execute('UPDATE comments SET author_id = 2 WHERE id = 1')

    auth.login()
    #Current user can't modify other user's project
    assert client.post('/1/comments/1/edit').status_code == 403
    assert client.post('/1/comments/1/delete').status_code == 403
    #Current user should not see edit link on project show page
    assert b'href="/1/comments/1/edit"' not in client.get('/1').data

#Return to show page if the comment requested doesn't exist
def test_comment_edit_exists_required(client, auth):
    auth.login()
    response = client.post(
        '/1/comments/2/edit',
        data={
            'text': 'edited comment text'
        }
    )
    #Test that we redirect to the show page
    assert response.headers['Location'] == 'http://localhost/1'

    #Test that the flash message shows the error by following the redireict
    response = client.post(
        '/1/comments/2/edit',
        data={
            'text': 'edited comment text'
        },
        follow_redirects=True
    )
    assert b'Comment not found and is unable to be edited' in response.data
    
#Return to show page if the comment requested doesn't exist
def test_comment_delete_exists_required(client, auth):
    auth.login()
    response = client.post('/1/comments/2/delete')
    #Test that we redirect to the show page
    assert response.headers['Location'] == 'http://localhost/1'
    
    response = client.post('/1/comments/2/delete', follow_redirects=True)
    #Test that the flash message shows the error by following the redirect
    assert b'Comment not found and unable to be deleted' in response.data

# #Confirm we can create a second comment
def test_create_comment(client, auth, app):
    auth.login()

    with app.app_context():
        #Confirm only one comment
        assert db.session.query(Comment).count() == 1

    response = client.post(
        '/1/comments/',
        data={'text': 'This is the second comment'},
    )

    with app.app_context():
        #Another way to grab the count from the comments table
        count = db.engine.execute('SELECT COUNT(id) FROM comments').fetchone()[0]
        assert count == 2

# #Test that we can update a comment
def test_update_comment(client, auth, app):
    auth.login()
    with app.app_context():
        comment = Comment.query.filter_by(id=1).first()

    response = client.post(
        '/1/comments/1/edit',
        data={
            'text': 'edited comment text'
        }
    )

    with app.app_context():
        comment = db.engine.execute('SELECT * FROM comments WHERE id = 1').fetchone()
        assert comment['text'] == 'edited comment text'

#Show an error on invalid comment text data
@pytest.mark.parametrize('path', (
    '/1/comments/',
    '/1/comments/1/edit',
))
def test_create_update_validate_comment(client, auth, path):
    auth.login()
    response = client.post(path, data={'text': ''}, follow_redirects=True)
    assert b'Comment text is required.' in response.data

def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/comments/1/delete')
    assert response.headers['Location'] == 'http://localhost/1'

    with app.app_context():
        comment = db.engine.execute('SELECT * FROM comments WHERE id = 1').fetchone()
        assert comment is None