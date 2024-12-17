from app.models import db
from app.models.pet import Pet


class PetService:

    def get_all(self):
        """
        Retrieves all pet records.
        """
        return Pet.query.all()

    def get_by_id(self, id):
        """
        Retrieves a single pet record by ID.
        """
        return Pet.query.get(id)

    def create(self, data):
        """
        Creates a new pet record.
        """
        new_item = Pet(**data)
        db.session.add(new_item)
        db.session.commit()
        return new_item

    def update(self, id, data):
        """
        Updates an existing pet record by ID.
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
        Deletes an existing pet record by ID.
        """
        item = self.get_by_id(id)
        if not item:
            return False
        db.session.delete(item)
        db.session.commit()
        return True

    
    
    def get_owners_for_pet(self, id):
        """
        Retrieves related owner records for a specific pet.
        """
        item = self.get_by_id(id)
        if not item:
            return []
        return item.owner

    def add_owner_to_pet(self, id, data):
        """
        Adds a new owner related to a specific pet.
        """
        parent = self.get_by_id(id)
        if not parent:
            return None
        from app.services.owner_service import OwnerService
        related_service = OwnerService()
        new_item = related_service.create(data)
        parent.owner.append(new_item)
        db.session.commit()
        return new_item
    
    
    
    def get_pettypes_for_pet(self, id):
        """
        Retrieves related pettype records for a specific pet.
        """
        item = self.get_by_id(id)
        if not item:
            return []
        return item.pettype

    def add_pettype_to_pet(self, id, data):
        """
        Adds a new pettype related to a specific pet.
        """
        parent = self.get_by_id(id)
        if not parent:
            return None
        from app.services.pettype_service import PetTypeService
        related_service = PetTypeService()
        new_item = related_service.create(data)
        parent.pettype.append(new_item)
        db.session.commit()
        return new_item
    
    
    
    def get_visitss_for_pet(self, id):
        """
        Retrieves related visits records for a specific pet.
        """
        item = self.get_by_id(id)
        if not item:
            return []
        return item.visits

    def add_visits_to_pet(self, id, data):
        """
        Adds a new visits related to a specific pet.
        """
        parent = self.get_by_id(id)
        if not parent:
            return None
        from app.services.visit_service import VisitService
        related_service = VisitService()
        new_item = related_service.create(data)
        parent.visits.append(new_item)
        db.session.commit()
        return new_item
    
    