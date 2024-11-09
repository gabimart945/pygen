from abc import ABC, abstractmethod
import yaml
from pygen.project_configuration import ProjectConfiguration
from pygen.entity_model import EntityModel
from pygen.exceptions import ConfigurationException, ModelValidationException


class IYamlInterpreter(ABC):
    """
    Interface for YAML interpreters in PyGen.

    Provides abstract methods for parsing and validating YAML content,
    along with a static method for reading YAML files.
    """

    @abstractmethod
    def parse(self, file):
        """
        Parses a YAML file into a specific configuration object.

        Args:
            file (str): Path to the YAML file to parse.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @abstractmethod
    def _validate(self, content):
        """
        Validates the structure and contents of the YAML data.

        Args:
            content (dict): Parsed YAML content to validate.

        Raises:
            NotImplementedError: If the method is not implemented.
        """
        raise NotImplementedError

    @staticmethod
    def read(file):
        """
        Reads and parses a YAML file.

        Args:
            file (str): Path to the YAML file to read.

        Returns:
            dict: Parsed content of the YAML file.
        """
        return yaml.safe_load(file)


class ConfigurationYAMLInterpreter(IYamlInterpreter):
    """
    YAML interpreter for project configuration files.

    Validates and parses project configuration data in YAML format
    and transforms it into a ProjectConfiguration object.
    """

    def _validate(self, content):
        """
        Validates the YAML content for project configuration.

        Args:
            content (dict): Parsed YAML content for project configuration.

        Returns:
            bool: True if the validation is successful, otherwise raises an exception.

        Raises:
            ConfigurationException: If any required configuration item is missing or invalid.
        """
        try:
            self._validate_project_name(content)
            self._validate_backend(content["backend"])
            self._validate_database(content["backend"]["database"])
            self._validate_frontend(content["frontend"])
            return True
        except ConfigurationException as ex:
            print(f"Validation Error: {ex}")
            raise ex

    @staticmethod
    def _validate_project_name(content):
        """
        Validates the presence of 'project_name' in the YAML content.

        Args:
            content (dict): Parsed YAML content.

        Raises:
            ConfigurationException: If 'project_name' is missing.
        """
        if 'project_name' not in content:
            raise ConfigurationException("The YAML file must contain 'project_name' at the root.")

    @staticmethod
    def _validate_backend(backend):
        """
        Validates the backend configuration in the YAML content.

        Args:
            backend (dict): Backend section of the YAML content.

        Raises:
            ConfigurationException: If backend framework is missing or unsupported.
        """
        if 'architecture' not in backend:
            raise ConfigurationException("The backend must contain 'architecture'.")
        if 'framework' not in backend:
            raise ConfigurationException("The backend must contain 'framework'.")
        if backend["architecture"] not in ["monolithic"]:
            raise ConfigurationException(f"Unsupported backend architecture: {backend['architecture']}")
        if backend["framework"] not in ["flask"]:
            raise ConfigurationException(f"Unsupported backend framework: {backend['framework']}")

    @staticmethod
    def _validate_database(database):
        """
        Validates the database configuration in the YAML content.

        Args:
            database (dict): Database section of the YAML content.

        Raises:
            ConfigurationException: If production or development databases are missing or unsupported.
        """
        if 'production' not in database or 'development' not in database:
            raise ConfigurationException("The database configuration must include 'production' and 'development'.")
        if database["production"] not in ["postgresql", "sqlite"]:
            raise ConfigurationException(f"Unsupported production database: {database['production']}")
        if database["development"] not in ["postgresql", "sqlite"]:
            raise ConfigurationException(f"Unsupported development database: {database['development']}")

    @staticmethod
    def _validate_frontend(frontend):
        """
        Validates the frontend configuration in the YAML content.

        Args:
            frontend (dict): Frontend section of the YAML content.

        Raises:
            ConfigurationException: If frontend framework is missing or unsupported.
        """
        if 'framework' not in frontend:
            raise ConfigurationException("The frontend must contain 'framework'.")
        if frontend["framework"] not in ["react"]:
            raise ConfigurationException(f"Unsupported frontend framework: {frontend['framework']}")

    def parse(self, file):
        """
        Parses the YAML configuration file into a ProjectConfiguration object.

        Args:
            file (File): YAML file.

        Returns:
            ProjectConfiguration: The project configuration object.
        """
        yaml_content = self.read(file)
        if self._validate(yaml_content):
            return ProjectConfiguration(yaml_content)


class ModelYAMLInterpreter(IYamlInterpreter):
    """
    YAML interpreter for entity model files.

    Validates and parses model data in YAML format and transforms it
    into an EntityModel object.
    """

    def _validate(self, content):
        """
        Validates the YAML content for the entity model.

        Args:
            content (dict): Parsed YAML content for the entity model.

        Returns:
            bool: True if validation is successful, otherwise raises an exception.

        Raises:
            ModelValidationException: If any required model item is missing or invalid.
        """
        # Validate root
        if 'entities' not in content or 'relationships' not in content:
            raise ModelValidationException("The YAML file must contain 'entities' and 'relationships' at the root.")

        # Validate entities
        for entity in content['entities']:
            if 'name' not in entity:
                raise ModelValidationException("Each entity must have a 'name'.")
            if 'attributes' not in entity:
                raise ModelValidationException(f"The entity '{entity['name']}' must have 'attributes'.")
            for attribute in entity['attributes']:
                if 'name' not in attribute or 'type' not in attribute:
                    raise ModelValidationException(f"Each attribute in the entity '{entity['name']}' "
                                                   f"must have 'name' and 'type'.")

        # Validate relationships
        for relationship in content['relationships']:
            if 'source' not in relationship or 'target' not in relationship:
                raise ModelValidationException("Each relationship must have 'source' and 'target'.")

        return True

    def parse(self, file):
        """
        Parses the YAML model file into an EntityModel object.

        Args:
            file (File): YAML file.

        Returns:
            EntityModel: The entity model object.
        """
        yaml_content = self.read(file)
        if self._validate(yaml_content):
            return EntityModel(yaml_content)
