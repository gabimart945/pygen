from app.models import db

class Specialty(db.Model):
    __tablename__ = 'specialtys'

    
    id = db.Column(
        db.Integer,
        primary_key=True, 
        
        nullable=False
    )
    
    name = db.Column(
        db.String(255),
        
        
        nullable=True
    )
    
    vet_id = db.Column(
        db.Integer,
        
        db.ForeignKey('vets.id'), 
        nullable=True
    )
    

    
    vet = db.relationship(
        'Vet',
        
        back_populates='specialtys'
        
    )
    
