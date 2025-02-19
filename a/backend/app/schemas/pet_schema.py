from marshmallow import Schema, fields, validate, validates_schema, ValidationError
import re

class PetSchema(Schema):
    
    
    id = fields.Integer(required=False)
    
    
    
    name = fields.String(
        required=False,
        validate=validate.Length(min=1, max=255)
    )
    
    
    
    birth_date = fields.Date(required=False)
    
    
    
    owner_id = fields.Integer(
        required=False,
        validate=validate.Range(min=0)
    )
    
    

    
    
    owner = fields.Nested(
        "OwnerSchema",
        exclude=("pets",)
    )
    
    
    
    visits = fields.Nested(
        "VisitSchema",
        many=True,
        exclude=("pet",)
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