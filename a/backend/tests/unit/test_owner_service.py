import unittest
from app import create_app
from app.models import db
from app.services.owner_service import OwnerService

class TestOwnerService(unittest.TestCase):
    """
    Unit test class for the OwnerService.

    This class contains test cases for the OwnerService, including methods to test
    the retrieval and creation of Owner entities.
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
        self.service = OwnerService()  # Initialize the service under test

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
        Test the `get_all` method of the OwnerService.

        Verifies that the method returns a list of all Owner entities.
        """
        items = self.service.get_all()  # Call the service method
        self.assertIsInstance(items, list)  # Assert the result is a list
        # Add more assertions as needed

    def test_create(self):
        """
        Test the `create` method of the OwnerService.

        Verifies that a new Owner entity can be created successfully without errors.
        """
        # Generate payload dynamically with only foreign keys
        payload = {
            
        }
        item, errors = self.service.create(payload)  # Call the service method with empty data
        self.assertIsNone(errors)  # Assert no errors occurred
        # Add more assertions as needed