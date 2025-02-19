import pytest
from flask import Flask
from app import create_app
from app.models import db
from app.models.visit import Visit

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

def test_create_visit(test_client):
    """
    Test creating a new Visit.
    """
    payload = {
        
        "pet_id": 1,  # Replace '1' with a valid foreign key value if necessary
        
        "vet_id": 1,  # Replace '1' with a valid foreign key value if necessary
        
    }
    response = test_client.post('/api/visits/', json=payload)

    
    assert response.status_code == 201
    

def test_get_visit_list(test_client):
    """
    Test retrieving the list of Visit records.
    """
    response = test_client.get('/api/visits/')
   
    assert response.status_code == 200
    

def test_update_visit(test_client):
    """
    Test updating an existing Visit.
    """
    # Replace with a valid ID after creation
    update_payload = {
        
        "pet_id": 1,  # Replace '1' with a valid foreign key value if necessary
        
        "vet_id": 1,  # Replace '1' with a valid foreign key value if necessary
        
    }
    response = test_client.put('/api/visits/1', json=update_payload)
    
    assert response.status_code == 200
    

def test_delete_visit(test_client):
    """
    Test deleting an existing Visit.
    """
    response = test_client.delete('/api/visits/1')
    
    assert response.status_code == 204
    