from app.models import db
from app.models.vet import Vet


class VetService:

    def get_all(self):
        """
        Retrieves all vet records.
        """
        return Vet.query.all()

    def get_by_id(self, id):
        """
        Retrieves a single vet record by ID.
        """
        return Vet.query.get(id)

    def create(self, data):
        """
        Creates a new vet record.
        """
        new_item = Vet(**data)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    def update(self, id, data):
        """
        Updates an existing vet record by ID.
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
        Deletes an existing vet record by ID.
        """
        item = self.get_by_id(id)
        if not item:
            return False
        db.session.delete(item)
        db.session.commit()
        return True

    
    
    def get_specialtyss_for_vet(self, id):
        """
        Retrieves related specialtys records for a specific vet.
        """
        item = self.get_by_id(id)
        if not item:
            return []
        return item.specialtys

    def add_specialtys_to_vet(self, id, data):
        """
        Adds a new specialtys related to a specific vet.
        """
        parent = self.get_by_id(id)
        if not parent:
            return None
        from app.services.specialty_service import SpecialtyService
        related_service = SpecialtyService()
        new_item = related_service.create(data)
        parent.specialtys.append(new_item)
        db.session.commit()
        return new_item
    
    