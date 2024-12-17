from marshmallow import Schema, fields

class OwnerSchema(Schema):
    
    id = fields.db.Integer(required=True)
    
    first_name = fields.db.String(255)(required=False)
    
    last_name = fields.db.String(255)(required=False)
    
    address = fields.db.String(255)(required=False)
    
    city = fields.db.String(255)(required=False)
    
    telephone = fields.db.String(255)(required=False)
    