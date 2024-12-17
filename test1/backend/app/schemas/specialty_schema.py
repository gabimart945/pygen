from marshmallow import Schema, fields

class SpecialtySchema(Schema):
    
    id = fields.db.Integer(required=True)
    
    name = fields.db.String(255)(required=False)
    
    vet_id = fields.db.Integer(required=False)
    