import pytest
from api.app.pets import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_say_hello(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {'message': 'Hello!'}

def test_get_pet_success(client):
    response = client.get('/pets/0')
    assert response.status_code == 200
    assert response.json['id'] == 0
    assert response.json['name'] == 'Kitty'
    assert response.json['category'] == 'cat'

def test_get_pet_not_found(client):
    response = client.get('/pets/99')
    assert response.status_code == 404

def test_update_pet_success(client):
    response = client.patch('/pets/0', json={'name': 'Tom'})
    assert response.status_code == 200
    assert response.json['name'] == 'Tom'
    assert response.json['id'] == 0

def test_update_pet_not_found(client):
    response = client.patch('/pets/99', json={'name': 'Ghost'})
    assert response.status_code == 404

def test_update_pet_invalid_category(client):
    response = client.patch('/pets/0', json={'category': 'bird'})
    assert response.status_code == 422 