from marshmallow import Schema, fields, validate, validates_schema, ValidationError
import re

class VisitSchema(Schema):
    
    
    id = fields.Integer(required=False)
    
    
    
    visit_date = fields.Date(required=False)
    
    
    
    description = fields.String(
        required=False,
        validate=validate.Length(min=1, max=255)
    )
    
    
    
    pet_id = fields.Integer(
        required=True,
        validate=validate.Range(min=0)
    )
    
    
    
    vet_id = fields.Integer(
        required=True,
        validate=validate.Range(min=0)
    )
    
    

    
    
    pet = fields.Nested(
        "PetSchema",
        exclude=("visits",)
    )
    
    
    
    vet = fields.Nested(
        "VetSchema",
        exclude=("visits",)
    )
    
    

    @validates_schema(pass_many=True)
    def validate_sql_injection(self, data, many, **kwargs):
        """Validates input fields against SQL injection patterns."""
        sql_injection_pattern = r".*([';/*]).*"
        safe_pattern = r"^[a-zA-Z0-9 _-]+$"

        for field_name, value in (data.items() if isinstance(data, dict) else []):
            if isinstance(value, str):
                if re.match(sql_injection_pattern, value) and not re.match(safe_pattern, value):
                    raise ValidationError(f"Potential SQL injection detected in field '{field_name}'.")