from app.models import db

class Pet(db.Model):
    __tablename__ = 'pets'

    
    id = db.Column(
        db.Integer,
        primary_key=True, 
        
        nullable=False
    )
    
    name = db.Column(
        db.String(255),
        
        
        nullable=True
    )
    
    birth_date = db.Column(
        db.Date,
        
        
        nullable=True
    )
    
    owner_id = db.Column(
        db.Integer,
        
        db.ForeignKey('owners.id'), 
        nullable=False
    )
    
    pettype_id = db.Column(
        db.Integer,
        
        db.ForeignKey('pettypes.id'), 
        nullable=True
    )
    

    
    owner = db.relationship(
        'Owner',
        
        back_populates='pets'
        
    )
    
    pettype = db.relationship(
        'PetType',
        
        back_populates='pets'
        
    )
    
    visits = db.relationship(
        'Visit',
        
        back_populates='pet'
        , cascade="all, delete-orphan"
    )
    
