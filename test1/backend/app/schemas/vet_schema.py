from marshmallow import Schema, fields

class VetSchema(Schema):
    
    id = fields.db.Integer(required=True)
    
    first_name = fields.db.String(255)(required=False)
    
    last_name = fields.db.String(255)(required=False)
    