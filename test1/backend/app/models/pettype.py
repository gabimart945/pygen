from app.models import db

class PetType(db.Model):
    __tablename__ = 'pettypes'

    
    id = db.Column(
        db.Integer,
        primary_key=True, 
        
        nullable=False
    )
    
    name = db.Column(
        db.String(255),
        
        
        nullable=True
    )
    

    
    pets = db.relationship(
        'Pet',
        
        back_populates='pettype'
        , cascade="all, delete-orphan"
    )
    
