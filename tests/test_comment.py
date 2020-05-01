import pytest
from flask import g, session
from hobbyProjectWebsite.db import db

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
    assert response.headers['Location'] == 'http://localhost/auth/login'

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
    response = client.post('/1/comments/2/edit',)
    print(response.status_code)
    print(response.data)
    assert response.headers['Location'] == 'http://localhost/1'
    # if 'edit' in path:
    #     assert b'Comment not found and is unable to be edited' in response.data
    # else:
    #     assert b'Comment not found and unable to be deleted' in response.data

#Return to show page if the comment requested doesn't exist
def test_comment_delete_exists_required(client, auth):
    auth.login()
    response = client.post(
        '/1/comments/2/delete',
         data={
            'text': 'edited text'
        }
    )
    print(response.status_code)
    print(response.data)
    assert response.headers['Location'] == 'http://localhost/1'
    # if 'edit' in path:
    #     assert b'Comment not found and is unable to be edited' in response.data
    # else:
    #     assert b'Comment not found and unable 

# #Confirm we can create a second post
# def test_create(client, auth, app):
#     auth.login()

#     assert client.get('/create').status_code == 200
#     response = client.post(
#         '/create',
#         data={'title': 'created', 'body': 'createdBody', 'image': '', 'githuburl': '', 'moreinfourl': ''},
#     )

#     with app.app_context():
#         count = db.engine.execute('SELECT COUNT(id) FROM projects').fetchone()[0]
#         assert count == 2

# #Test that we can update a post
# def test_update(client, auth, app):
#     auth.login()
#     assert client.get('/1/edit').status_code == 200
#     with app.app_context():
#         project = db.engine.execute('SELECT * FROM projects WHERE id = 1').fetchone()

#     print(project)
#     print(project['body'])
#     response = client.post(
#         '/1/edit',
#         data={
#             'title': 'edited',
#             'body': project['body'],
#             'image': project['image'],
#             'githuburl': project['githuburl'],
#             'moreinfourl': project['moreinfourl']
#         }
#     )
#     print(response)

#     with app.app_context():
#         project = db.engine.execute('SELECT * FROM projects WHERE id = 1').fetchone()
#         assert project['title'] == 'edited'

# #Show an error on invalid title/body data
# @pytest.mark.parametrize('path', (
#     '/create',
#     '/1/edit',
# ))
# def test_create_update_validate(client, auth, path):
#     auth.login()
#     response = client.post(path, data={'title': '', 'body': '', 'image': 'image text', 'githuburl': 'github text', 'moreinfourl': 'more info url text'})
#     print(response, response.status_code)
#     assert b'Title is required.' in response.data

# def test_delete(client, auth, app):
#     auth.login()
#     response = client.post('/1/delete')
#     assert response.headers['Location'] == 'http://localhost/'

#     with app.app_context():
#         project = db.engine.execute('SELECT * FROM projects WHERE id = 1').fetchone()
#         assert project is None