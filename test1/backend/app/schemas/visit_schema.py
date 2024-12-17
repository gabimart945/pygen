from marshmallow import Schema, fields

class VisitSchema(Schema):
    
    id = fields.db.Integer(required=True)
    
    visit_date = fields.db.Date(required=False)
    
    description = fields.db.String(255)(required=False)
    
    pet_id = fields.db.Integer(required=True)
    