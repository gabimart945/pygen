from marshmallow import Schema, fields, validate, validates_schema, ValidationError
import re

class OwnerSchema(Schema):
    
    
    id = fields.Integer(required=False)
    
    
    
    first_name = fields.String(
        required=False,
        validate=validate.Length(min=1, max=255)
    )
    
    
    
    last_name = fields.String(
        required=False,
        validate=validate.Length(min=1, max=255)
    )
    
    

    
    
    pets = fields.Nested(
        "PetSchema",
        many=True,
        exclude=("owner",)
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