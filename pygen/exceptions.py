
class ConfigurationException(Exception):
    """
    Custom exception for configuration errors in PyGen.

    This exception is used to handle errors related to invalid or missing
    configurations in YAML files, enabling a more controlled and specific
    management of these errors in the workflow.
    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"ConfigurationException: {self.message}"


class ModelValidationException(Exception):
    """
    Custom exception for model validation errors in PyGen.

    Used for handling errors in the YAML structure when defining entities
    and relationships, providing specific error messages for missing or
    invalid fields.
    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"ModelValidationException: {self.message}"
