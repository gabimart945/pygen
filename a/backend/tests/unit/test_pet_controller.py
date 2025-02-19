import unittest
from flask import Flask
from app import create_app

class TestPetController(unittest.TestCase):
    """
    Unit test class for the PetController.

    This class contains test cases for the Flask controller handling Pet endpoints,
    including methods to test retrieval and creation of Pet entities.
    """

    def setUp(self):
        """
        Set up the testing environment.

        This method initializes the application in testing mode and prepares a test client
        for making requests to the application.
        """
        self.app = create_app("testing")  # Create the Flask application instance
        self.client = self.app.test_client()  # Create a test client for HTTP requests

    def test_get_all_pets(self):
        """
        Test the GET endpoint for retrieving all Pet entities.

        Sends a GET request to the `/api/pets/` endpoint and verifies
        that the response status code is 200, indicating successful retrieval.
        """
        response = self.client.get('/api/pets/')  # Perform a GET request
        
        self.assertEqual(200, response.status_code)  # Assert the response code is 200
        
        # Add more assertions as needed to validate the response content

    def test_create_pet(self):
        """
        Test the POST endpoint for creating a new Pet entity.

        Sends a POST request to the `/api/pets` endpoint with an empty JSON payload
        and verifies that the response status code is 201, indicating successful creation.
        """
        payload = {
            
            "owner_id": 1,  # Replace '1' with a valid foreign key value if necessary
            
        }

        response = self.client.post('/api/pets/', json=payload)  # Perform a POST request
        
        self.assertEqual(201, response.status_code)  # Assert the response code is 200
        
        # Add more assertions as needed to validate the response content