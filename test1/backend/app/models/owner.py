from app.models import db

class Owner(db.Model):
    __tablename__ = 'owners'

    
    id = db.Column(
        db.Integer,
        primary_key=True, 
        
        nullable=False
    )
    
    first_name = db.Column(
        db.String(255),
        
        
        nullable=True
    )
    
    last_name = db.Column(
        db.String(255),
        
        
        nullable=True
    )
    
    address = db.Column(
        db.String(255),
        
        
        nullable=True
    )
    
    city = db.Column(
        db.String(255),
        
        
        nullable=True
    )
    
    telephone = db.Column(
        db.String(255),
        
        
        nullable=True
    )
    

    
    pets = db.relationship(
        'Pet',
        
        back_populates='owner'
        , cascade="all, delete-orphan"
    )
    
