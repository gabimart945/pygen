import unittest
from marshmallow import ValidationError
from app.schemas.visit_schema import VisitSchema

class TestVisitSchema(unittest.TestCase):
    """
    Unit test class for the VisitSchema.

    This class tests the functionality of the VisitSchema, including data validation,
    serialization, and deserialization.
    """

    def setUp(self):
        """
        Set up the testing environment.

        This method initializes the schema instance for testing.
        """
        self.schema = VisitSchema()

    def test_valid_data(self):
        """
        Test that valid data passes schema validation.

        Ensures that the schema correctly serializes and deserializes valid input data.
        """
        valid_data = {
            
            "id": 1,
            
            "visit_date": "2023-01-01",
            
            "description": "example_text",
            
            "pet_id": 1,
            
            "vet_id": 1,
            
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
            
            "description": 123,  # Invalid type for string fields
            
        }

        with self.assertRaises(ValidationError):
            self.schema.load(invalid_data)

    
    def test_missing_foreign_key(self):
        """
        Test that missing foreign key raises validation errors.

        Ensures that the schema correctly identifies missing foreign key fields.
        """
        missing_fk_data = {
            
            "id": 1,
            
            "visit_date": "2023-01-01",
            
            "description": "example_text",
            
        }

        with self.assertRaises(ValidationError):
            self.schema.load(missing_fk_data)
    
    def test_missing_foreign_key(self):
        """
        Test that missing foreign key raises validation errors.

        Ensures that the schema correctly identifies missing foreign key fields.
        """
        missing_fk_data = {
            
            "id": 1,
            
            "visit_date": "2023-01-01",
            
            "description": "example_text",
            
        }

        with self.assertRaises(ValidationError):
            self.schema.load(missing_fk_data)
    