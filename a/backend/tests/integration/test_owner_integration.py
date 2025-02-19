import pytest
from flask import Flask
from app import create_app
from app.models import db
from app.models.owner import Owner

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

def test_create_owner(test_client):
    """
    Test creating a new Owner.
    """
    payload = {
        
    }
    response = test_client.post('/api/owners/', json=payload)

    
    assert response.status_code == 201
    

def test_get_owner_list(test_client):
    """
    Test retrieving the list of Owner records.
    """
    response = test_client.get('/api/owners/')
   
    assert response.status_code == 200
    

def test_update_owner(test_client):
    """
    Test updating an existing Owner.
    """
    # Replace with a valid ID after creation
    update_payload = {
        
    }
    response = test_client.put('/api/owners/1', json=update_payload)
    
    assert response.status_code == 200
    

def test_delete_owner(test_client):
    """
    Test deleting an existing Owner.
    """
    response = test_client.delete('/api/owners/1')
    
    assert response.status_code == 204
    