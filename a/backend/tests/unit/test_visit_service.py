import unittest
from app import create_app
from app.models import db
from app.services.visit_service import VisitService

class TestVisitService(unittest.TestCase):
    """
    Unit test class for the VisitService.

    This class contains test cases for the VisitService, including methods to test
    the retrieval and creation of Visit entities.
    """

    def setUp(self):
        """
        Set up the testing environment.

        This method initializes the application in testing mode, creates an application context,
        and sets up an in-memory database for testing purposes. It also initializes the service
        under test.
        """
        self.app = create_app("testing")  # Create the application instance
        self.app_context = self.app.app_context()
        self.app_context.push()  # Activate the application context
        db.create_all()  # Create all tables in the test database
        self.service = VisitService()  # Initialize the service under test

    def tearDown(self):
        """
        Clean up after each test case.

        This method removes the database session, drops all tables, and pops the application context.
        """
        db.session.remove()  # Clear the session
        db.drop_all()  # Drop all tables
        self.app_context.pop()  # Deactivate the application context

    def test_get_all(self):
        """
        Test the `get_all` method of the VisitService.

        Verifies that the method returns a list of all Visit entities.
        """
        items = self.service.get_all()  # Call the service method
        self.assertIsInstance(items, list)  # Assert the result is a list
        # Add more assertions as needed

    def test_create(self):
        """
        Test the `create` method of the VisitService.

        Verifies that a new Visit entity can be created successfully without errors.
        """
        # Generate payload dynamically with only foreign keys
        payload = {
            
            "pet_id": 1,  # Replace '1' with a valid foreign key value if necessary
            
            "vet_id": 1,  # Replace '1' with a valid foreign key value if necessary
            
        }
        item, errors = self.service.create(payload)  # Call the service method with empty data
        self.assertIsNone(errors)  # Assert no errors occurred
        # Add more assertions as needed