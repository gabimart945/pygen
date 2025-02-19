from marshmallow import ValidationError
from app.models import db
from app.models.vet import Vet
from app.schemas.vet_schema import VetSchema

from app.models.visit import Visit
from app.schemas.visit_schema import VisitSchema


class VetService:
    def __init__(self):
        self._schema = VetSchema()
        
        self._visit_schema = VisitSchema()
        

    def get_all(self):
        """
        Retrieves all records of Vet.

        Returns:
            list: A list of serialized Vet objects.
        """
        items = Vet.query.all()
        return self._schema.dump(items, many=True)

    def get_by_id(self, id):
        """
        Retrieves a single Vet by its ID.

        Args:
            id (int): The ID of the Vet to retrieve.

        Returns:
            dict or None: A serialized Vet object if found, otherwise None.
        """
        item = Vet.query.get(id)
        return self._schema.dump(item) if item else None

    def create(self, data):
        """
        Creates a new record after validating and deserializing the input data.

        Returns:
            tuple(dict or None, dict or None):
            - First element: the created item (serialized) or None if validation failed.
            - Second element: validation errors if any, otherwise None.
        """
        try:
            loaded_data = self._schema.load(data)  # Validation and deserialization
        except ValidationError as err:
            return None, err.messages

        new_item = Vet(**loaded_data)
        db.session.add(new_item)
        db.session.commit()
        return self._schema.dump(new_item), None

    def update(self, id, data):
        """
        Updates an existing record after validating and deserializing the input data.

        Args:
            id (int): The ID of the Vet to update.
            data (dict): The data to update the record with.

        Returns:
            tuple(dict or None, dict or None):
            - First element: the updated item (serialized) or None if it does not exist.
            - Second element: validation errors or an error message if any, otherwise None.
        """
        item = Vet.query.get(id)
        if not item:
            return None, {'error': 'Vet not found'}

        try:
            loaded_data = self._schema.load(data)  # Validation and deserialization
        except ValidationError as err:
            return None, err.messages

        
        loaded_data.pop("visits", None)
        

        for key, value in loaded_data.items():
            setattr(item, key, value)
        db.session.commit()
        return self._schema.dump(item), None

    def delete(self, id):
        """
        Deletes an existing record by its ID.

        Args:
            id (int): The ID of the Vet to delete.

        Returns:
            bool: True if the record was deleted successfully, False if it does not exist.
        """
        item = Vet.query.get(id)
        if not item:
            return False
        db.session.delete(item)
        db.session.commit()
        return True

    
    def get_visitss(self, id):
        """
        Retrieves related visit records for a given Vet ID.

        Args:
            id (int): The ID of the parent Vet.

        Returns:
            tuple(list or None, dict or None):
            - First element: A list or single instance of serialized Visit objects
              (depending on the relationship type) or None if the parent Vet was not found.
            - Second element: Error information if the parent Vet was not found, otherwise None.
        """
        item = Vet.query.get(id)
        if not item:
            return None, {'error': 'Vet not found'}
        related_items = getattr(item, "visits")
        return self._visit_schema.dump(
            related_items,
            many=True
        ), None

    def add_visits(self, id, data):
        """
        Adds a related visit record to a given Vet.

        Args:
            id (int): The ID of the parent Vet.
            data (dict): The data to create the related record.

        Returns:
            tuple(dict or None, dict or None):
            - First element: The newly created related record (serialized) or None if an error occurred.
            - Second element: Validation errors or an error message if the parent was not found, otherwise None.
        """
        parent = Vet.query.get(id)
        if not parent:
            return None, {'error': 'Vet not found'}

        try:
            loaded_data = self._visit_schema.load(data)  # Validation and deserialization
        except ValidationError as err:
            return None, err.messages

        new_related_item = Visit(**loaded_data)
        db.session.add(new_related_item)

        # Add the new item to the relationship
        if "one-to-many" in ["one-to-many", "many-to-many"]:
            getattr(parent, "visits").append(new_related_item)
        elif "one-to-many" in ["many-to-one", "one-to-one"]:
            setattr(parent, "visits", new_related_item)

        db.session.commit()
        return self._visit_schema.dump(new_related_item), None
    