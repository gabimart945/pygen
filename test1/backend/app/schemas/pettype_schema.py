from marshmallow import Schema, fields

class PetTypeSchema(Schema):
    
    id = fields.db.Integer(required=True)
    
    name = fields.db.String(255)(required=False)
    