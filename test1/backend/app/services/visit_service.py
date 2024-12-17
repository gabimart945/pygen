from app.models import db
from app.models.visit import Visit


class VisitService:

    def get_all(self):
        """
        Retrieves all visit records.
        """
        return Visit.query.all()

    def get_by_id(self, id):
        """
        Retrieves a single visit record by ID.
        """
        return Visit.query.get(id)

    def create(self, data):
        """
        Creates a new visit record.
        """
        new_item = Visit(**data)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    def update(self, id, data):
        """
        Updates an existing visit record by ID.
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
        Deletes an existing visit record by ID.
        """
        item = self.get_by_id(id)
        if not item:
            return False
        db.session.delete(item)
        db.session.commit()
        return True

    
    
    def get_pets_for_visit(self, id):
        """
        Retrieves related pet records for a specific visit.
        """
        item = self.get_by_id(id)
        if not item:
            return []
        return item.pet

    def add_pet_to_visit(self, id, data):
        """
        Adds a new pet related to a specific visit.
        """
        parent = self.get_by_id(id)
        if not parent:
            return None
        from app.services.pet_service import PetService
        related_service = PetService()
        new_item = related_service.create(data)
        parent.pet.append(new_item)
        db.session.commit()
        return new_item
    
    