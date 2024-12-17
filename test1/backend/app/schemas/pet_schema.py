from marshmallow import Schema, fields

class PetSchema(Schema):
    
    id = fields.db.Integer(required=True)
    
    name = fields.db.String(255)(required=False)
    
    birth_date = fields.db.Date(required=False)
    
    owner_id = fields.db.Integer(required=True)
    
    pettype_id = fields.db.Integer(required=False)
    