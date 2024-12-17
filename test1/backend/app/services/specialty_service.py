from app.models import db
from app.models.specialty import Specialty


class SpecialtyService:

    def get_all(self):
        """
        Retrieves all specialty records.
        """
        return Specialty.query.all()

    def get_by_id(self, id):
        """
        Retrieves a single specialty record by ID.
        """
        return Specialty.query.get(id)

    def create(self, data):
        """
        Creates a new specialty record.
        """
        new_item = Specialty(**data)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    def update(self, id, data):
        """
        Updates an existing specialty record by ID.
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
        Deletes an existing specialty record by ID.
        """
        item = self.get_by_id(id)
        if not item:
            return False
        db.session.delete(item)
        db.session.commit()
        return True

    
    
    def get_vets_for_specialty(self, id):
        """
        Retrieves related vet records for a specific specialty.
        """
        item = self.get_by_id(id)
        if not item:
            return []
        return item.vet

    def add_vet_to_specialty(self, id, data):
        """
        Adds a new vet related to a specific specialty.
        """
        parent = self.get_by_id(id)
        if not parent:
            return None
        from app.services.vet_service import VetService
        related_service = VetService()
        new_item = related_service.create(data)
        parent.vet.append(new_item)
        db.session.commit()
        return new_item
    
    