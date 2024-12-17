from app.models import db

class Visit(db.Model):
    __tablename__ = 'visits'

    
    id = db.Column(
        db.Integer,
        primary_key=True, 
        
        nullable=False
    )
    
    visit_date = db.Column(
        db.Date,
        
        
        nullable=True
    )
    
    description = db.Column(
        db.String(255),
        
        
        nullable=True
    )
    
    pet_id = db.Column(
        db.Integer,
        
        db.ForeignKey('pets.id'), 
        nullable=False
    )
    

    
    pet = db.relationship(
        'Pet',
        
        back_populates='visits'
        
    )
    
