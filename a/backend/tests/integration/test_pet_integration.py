import pytest
from flask import Flask
from app import create_app
from app.models import db
from app.models.pet import Pet

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

def test_create_pet(test_client):
    """
    Test creating a new Pet.
    """
    payload = {
        
        "owner_id": 1,  # Replace '1' with a valid foreign key value if necessary
        
    }
    response = test_client.post('/api/pets/', json=payload)

    
    assert response.status_code == 201
    

def test_get_pet_list(test_client):
    """
    Test retrieving the list of Pet records.
    """
    response = test_client.get('/api/pets/')
   
    assert response.status_code == 200
    

def test_update_pet(test_client):
    """
    Test updating an existing Pet.
    """
    # Replace with a valid ID after creation
    update_payload = {
        
        "owner_id": 1,  # Replace '1' with a valid foreign key value if necessary
        
    }
    response = test_client.put('/api/pets/1', json=update_payload)
    
    assert response.status_code == 200
    

def test_delete_pet(test_client):
    """
    Test deleting an existing Pet.
    """
    response = test_client.delete('/api/pets/1')
    
    assert response.status_code == 204
    