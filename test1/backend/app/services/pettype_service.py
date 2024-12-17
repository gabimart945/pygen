from app.models import db
from app.models.pettype import PetType


class PetTypeService:

    def get_all(self):
        """
        Retrieves all pettype records.
        """
        return PetType.query.all()

    def get_by_id(self, id):
        """
        Retrieves a single pettype record by ID.
        """
        return PetType.query.get(id)

    def create(self, data):
        """
        Creates a new pettype record.
        """
        new_item = PetType(**data)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    def update(self, id, data):
        """
        Updates an existing pettype record by ID.
        """
        item = self.get_by_id(id)
        if not item:
            return None
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
        return item

    def delete(self, id):
        """
        Deletes an existing pettype record by ID.
        """
        item = self.get_by_id(id)
        if not item:
            return False
        db.session.delete(item)
        db.session.commit()
        return True

    
    
    def get_petss_for_pettype(self, id):
        """
        Retrieves related pets records for a specific pettype.
        """
        item = self.get_by_id(id)
        if not item:
            return []
        return item.pets

    def add_pets_to_pettype(self, id, data):
        """
        Adds a new pets related to a specific pettype.
        """
        parent = self.get_by_id(id)
        if not parent:
            return None
        from app.services.pet_service import PetService
        related_service = PetService()
        new_item = related_service.create(data)
        parent.pets.append(new_item)
        db.session.commit()
        return new_item
    
    