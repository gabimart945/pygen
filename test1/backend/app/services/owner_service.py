from app.models import db
from app.models.owner import Owner


class OwnerService:

    def get_all(self):
        """
        Retrieves all owner records.
        """
        return Owner.query.all()

    def get_by_id(self, id):
        """
        Retrieves a single owner record by ID.
        """
        return Owner.query.get(id)

    def create(self, data):
        """
        Creates a new owner record.
        """
        new_item = Owner(**data)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    def update(self, id, data):
        """
        Updates an existing owner record by ID.
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
        Deletes an existing owner record by ID.
        """
        item = self.get_by_id(id)
        if not item:
            return False
        db.session.delete(item)
        db.session.commit()
        return True

    
    
    def get_petss_for_owner(self, id):
        """
        Retrieves related pets records for a specific owner.
        """
        item = self.get_by_id(id)
        if not item:
            return []
        return item.pets

    def add_pets_to_owner(self, id, data):
        """
        Adds a new pets related to a specific owner.
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
    
    