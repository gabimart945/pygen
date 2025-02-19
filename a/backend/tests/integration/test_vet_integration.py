import pytest
from flask import Flask
from app import create_app
from app.models import db
from app.models.vet import Vet

@pytest.fixture(scope='module')
def test_client():
    """
    Fixture for setting up the Flask test client.
    """
    flask_app = create_app()
    flask_app.config['TESTING'] = True
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_integration.db'

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            db.create_all()
            yield testing_client
        with flask_app.app_context():
            db.drop_all()

def test_create_vet(test_client):
    """
    Test creating a new Vet.
    """
    payload = {
        
    }
    response = test_client.post('/api/vets/', json=payload)

    
    assert response.status_code == 201
    

def test_get_vet_list(test_client):
    """
    Test retrieving the list of Vet records.
    """
    response = test_client.get('/api/vets/')
   
    assert response.status_code == 200
    

def test_update_vet(test_client):
    """
    Test updating an existing Vet.
    """
    # Replace with a valid ID after creation
    update_payload = {
        
    }
    response = test_client.put('/api/vets/1', json=update_payload)
    
    assert response.status_code == 200
    

def test_delete_vet(test_client):
    """
    Test deleting an existing Vet.
    """
    response = test_client.delete('/api/vets/1')
    
    assert response.status_code == 204
    