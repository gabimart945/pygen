from app.models import db

class Vet(db.Model):
    __tablename__ = 'vets'

    
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
    

    
    visits = db.relationship(
        'Visit',
        
        back_populates='vet'
        , cascade="all, delete-orphan"
    )
    
