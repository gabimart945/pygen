from marshmallow import ValidationError
from app.models import db
from app.models.visit import Visit
from app.schemas.visit_schema import VisitSchema

from app.models.pet import Pet
from app.schemas.pet_schema import PetSchema

from app.models.vet import Vet
from app.schemas.vet_schema import VetSchema


class VisitService:
    def __init__(self):
        self._schema = VisitSchema()
        
        self._pet_schema = PetSchema()
        
        self._vet_schema = VetSchema()
        

    def get_all(self):
        """
        Retrieves all records of Visit.

        Returns:
            list: A list of serialized Visit objects.
        """
        items = Visit.query.all()
        return self._schema.dump(items, many=True)

    def get_by_id(self, id):
        """
        Retrieves a single Visit by its ID.

        Args:
            id (int): The ID of the Visit to retrieve.

        Returns:
            dict or None: A serialized Visit object if found, otherwise None.
        """
        item = Visit.query.get(id)
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

        new_item = Visit(**loaded_data)
        db.session.add(new_item)
        db.session.commit()
        return self._schema.dump(new_item), None

    def update(self, id, data):
        """
        Updates an existing record after validating and deserializing the input data.

        Args:
            id (int): The ID of the Visit to update.
            data (dict): The data to update the record with.

        Returns:
            tuple(dict or None, dict or None):
            - First element: the updated item (serialized) or None if it does not exist.
            - Second element: validation errors or an error message if any, otherwise None.
        """
        item = Visit.query.get(id)
        if not item:
            return None, {'error': 'Visit not found'}

        try:
            loaded_data = self._schema.load(data)  # Validation and deserialization
        except ValidationError as err:
            return None, err.messages

        
        loaded_data.pop("pet", None)
        
        loaded_data.pop("vet", None)
        

        for key, value in loaded_data.items():
            setattr(item, key, value)
        db.session.commit()
        return self._schema.dump(item), None

    def delete(self, id):
        """
        Deletes an existing record by its ID.

        Args:
            id (int): The ID of the Visit to delete.

        Returns:
            bool: True if the record was deleted successfully, False if it does not exist.
        """
        item = Visit.query.get(id)
        if not item:
            return False
        db.session.delete(item)
        db.session.commit()
        return True

    
    def get_pets(self, id):
        """
        Retrieves related pet records for a given Visit ID.

        Args:
            id (int): The ID of the parent Visit.

        Returns:
            tuple(list or None, dict or None):
            - First element: A list or single instance of serialized Pet objects
              (depending on the relationship type) or None if the parent Visit was not found.
            - Second element: Error information if the parent Visit was not found, otherwise None.
        """
        item = Visit.query.get(id)
        if not item:
            return None, {'error': 'Visit not found'}
        related_items = getattr(item, "pet")
        return self._pet_schema.dump(
            related_items,
            many=False
        ), None

    def add_pet(self, id, data):
        """
        Adds a related pet record to a given Visit.

        Args:
            id (int): The ID of the parent Visit.
            data (dict): The data to create the related record.

        Returns:
            tuple(dict or None, dict or None):
            - First element: The newly created related record (serialized) or None if an error occurred.
            - Second element: Validation errors or an error message if the parent was not found, otherwise None.
        """
        parent = Visit.query.get(id)
        if not parent:
            return None, {'error': 'Visit not found'}

        try:
            loaded_data = self._pet_schema.load(data)  # Validation and deserialization
        except ValidationError as err:
            return None, err.messages

        new_related_item = Pet(**loaded_data)
        db.session.add(new_related_item)

        # Add the new item to the relationship
        if "many-to-one" in ["one-to-many", "many-to-many"]:
            getattr(parent, "pet").append(new_related_item)
        elif "many-to-one" in ["many-to-one", "one-to-one"]:
            setattr(parent, "pet", new_related_item)

        db.session.commit()
        return self._pet_schema.dump(new_related_item), None
    
    def get_vets(self, id):
        """
        Retrieves related vet records for a given Visit ID.

        Args:
            id (int): The ID of the parent Visit.

        Returns:
            tuple(list or None, dict or None):
            - First element: A list or single instance of serialized Vet objects
              (depending on the relationship type) or None if the parent Visit was not found.
            - Second element: Error information if the parent Visit was not found, otherwise None.
        """
        item = Visit.query.get(id)
        if not item:
            return None, {'error': 'Visit not found'}
        related_items = getattr(item, "vet")
        return self._vet_schema.dump(
            related_items,
            many=False
        ), None

    def add_vet(self, id, data):
        """
        Adds a related vet record to a given Visit.

        Args:
            id (int): The ID of the parent Visit.
            data (dict): The data to create the related record.

        Returns:
            tuple(dict or None, dict or None):
            - First element: The newly created related record (serialized) or None if an error occurred.
            - Second element: Validation errors or an error message if the parent was not found, otherwise None.
        """
        parent = Visit.query.get(id)
        if not parent:
            return None, {'error': 'Visit not found'}

        try:
            loaded_data = self._vet_schema.load(data)  # Validation and deserialization
        except ValidationError as err:
            return None, err.messages

        new_related_item = Vet(**loaded_data)
        db.session.add(new_related_item)

        # Add the new item to the relationship
        if "many-to-one" in ["one-to-many", "many-to-many"]:
            getattr(parent, "vet").append(new_related_item)
        elif "many-to-one" in ["many-to-one", "one-to-one"]:
            setattr(parent, "vet", new_related_item)

        db.session.commit()
        return self._vet_schema.dump(new_related_item), None
    