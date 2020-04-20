from hobbyProjectWebsite import create_app

def test_config():
    db_path = 'postgresql:///hobbyprojectwebsite_test'

    assert not create_app().testing
    assert create_app(
        {
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': db_path,
        }
    ).testing

#Example test that checks what we received is correct
def test_hello(client):
    response = client.get('/helloWorld')
    assert response.data == b'Hello World!'

