from marshmallow import ValidationError
from app.models import db
from app.models.owner import Owner
from app.schemas.owner_schema import OwnerSchema

from app.models.pet import Pet
from app.schemas.pet_schema import PetSchema


class OwnerService:
    def __init__(self):
        self._schema = OwnerSchema()
        
        self._pet_schema = PetSchema()
        

    def get_all(self):
        """
        Retrieves all records of Owner.

        Returns:
            list: A list of serialized Owner objects.
        """
        items = Owner.query.all()
        return self._schema.dump(items, many=True)

    def get_by_id(self, id):
        """
        Retrieves a single Owner by its ID.

        Args:
            id (int): The ID of the Owner to retrieve.

        Returns:
            dict or None: A serialized Owner object if found, otherwise None.
        """
        item = Owner.query.get(id)
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

        new_item = Owner(**loaded_data)
        db.session.add(new_item)
        db.session.commit()
        return self._schema.dump(new_item), None

    def update(self, id, data):
        """
        Updates an existing record after validating and deserializing the input data.

        Args:
            id (int): The ID of the Owner to update.
            data (dict): The data to update the record with.

        Returns:
            tuple(dict or None, dict or None):
            - First element: the updated item (serialized) or None if it does not exist.
            - Second element: validation errors or an error message if any, otherwise None.
        """
        item = Owner.query.get(id)
        if not item:
            return None, {'error': 'Owner not found'}

        try:
            loaded_data = self._schema.load(data)  # Validation and deserialization
        except ValidationError as err:
            return None, err.messages

        
        loaded_data.pop("pets", None)
        

        for key, value in loaded_data.items():
            setattr(item, key, value)
        db.session.commit()
        return self._schema.dump(item), None

    def delete(self, id):
        """
        Deletes an existing record by its ID.

        Args:
            id (int): The ID of the Owner to delete.

        Returns:
            bool: True if the record was deleted successfully, False if it does not exist.
        """
        item = Owner.query.get(id)
        if not item:
            return False
        db.session.delete(item)
        db.session.commit()
        return True

    
    def get_petss(self, id):
        """
        Retrieves related pet records for a given Owner ID.

        Args:
            id (int): The ID of the parent Owner.

        Returns:
            tuple(list or None, dict or None):
            - First element: A list or single instance of serialized Pet objects
              (depending on the relationship type) or None if the parent Owner was not found.
            - Second element: Error information if the parent Owner was not found, otherwise None.
        """
        item = Owner.query.get(id)
        if not item:
            return None, {'error': 'Owner not found'}
        related_items = getattr(item, "pets")
        return self._pet_schema.dump(
            related_items,
            many=True
        ), None

    def add_pets(self, id, data):
        """
        Adds a related pet record to a given Owner.

        Args:
            id (int): The ID of the parent Owner.
            data (dict): The data to create the related record.

        Returns:
            tuple(dict or None, dict or None):
            - First element: The newly created related record (serialized) or None if an error occurred.
            - Second element: Validation errors or an error message if the parent was not found, otherwise None.
        """
        parent = Owner.query.get(id)
        if not parent:
            return None, {'error': 'Owner not found'}

        try:
            loaded_data = self._pet_schema.load(data)  # Validation and deserialization
        except ValidationError as err:
            return None, err.messages

        new_related_item = Pet(**loaded_data)
        db.session.add(new_related_item)

        # Add the new item to the relationship
        if "one-to-many" in ["one-to-many", "many-to-many"]:
            getattr(parent, "pets").append(new_related_item)
        elif "one-to-many" in ["many-to-one", "one-to-one"]:
            setattr(parent, "pets", new_related_item)

        db.session.commit()
        return self._pet_schema.dump(new_related_item), None
    