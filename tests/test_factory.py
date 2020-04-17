from hobbyProjectWebsite import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

#Example test that checks what we received is correct
def test_hello(client):
    response = client.get('/helloWorld')
    assert response.data == b'Hello World!'

