import unittest
from marshmallow import ValidationError
from app.schemas.owner_schema import OwnerSchema

class TestOwnerSchema(unittest.TestCase):
    """
    Unit test class for the OwnerSchema.

    This class tests the functionality of the OwnerSchema, including data validation,
    serialization, and deserialization.
    """

    def setUp(self):
        """
        Set up the testing environment.

        This method initializes the schema instance for testing.
        """
        self.schema = OwnerSchema()

    def test_valid_data(self):
        """
        Test that valid data passes schema validation.

        Ensures that the schema correctly serializes and deserializes valid input data.
        """
        valid_data = {
            
            "id": 1,
            
            "first_name": "example_text",
            
            "last_name": "example_text",
            
        }

        try:
            deserialized_data = self.schema.load(valid_data)
        except ValidationError as e:
            self.fail(f"ValidationError raised unexpectedly: {e}")

        serialized_data = self.schema.dump(deserialized_data)
        self.assertEqual(serialized_data, valid_data)

    def test_invalid_data(self):
        """
        Test that invalid data raises validation errors.

        Ensures that the schema identifies and raises errors for invalid input data.
        """
        invalid_data = {
            
            "first_name": 123,  # Invalid type for string fields
            
            "last_name": 123,  # Invalid type for string fields
            
        }

        with self.assertRaises(ValidationError):
            self.schema.load(invalid_data)

    