from abc import ABC, abstractmethod
import yaml
from ProjectConfiguration import ProjectConfiguration
from EntityModel import EntityModel


class IYamlInterpreter(ABC):

    @abstractmethod
    def parse(self, file):
        raise NotImplementedError

    @abstractmethod
    def validate(self, content):
        raise NotImplementedError

    @staticmethod
    def read(file):
        return yaml.safe_load(file)


class ConfigurationYAMLInterpreter(IYamlInterpreter):

    def validate(self, content):
        if 'project_name' not in content:
            print("The YAML file must contain 'project_name' at the root.")
            return False

        if 'backend' not in content:
            print("The YAML file must contain 'backend' at the root.")
            return False

        if 'framework' not in content["backend"]:
            print("The backend must contain 'framework'.")
            return False

        if 'database' not in content["backend"]:
            print("The backend must contain 'database'.")
            return False

        if 'production' not in content["database"]:
            print("The database must contain 'production'.")
            return False

        if 'development' not in content["database"]:
            print("The database must contain 'development'.")
            return False

        if 'frontend' not in content:
            print("The YAML file must contain 'frontend' at the root.")
            return False

        if 'framework' not in content["frontend"]:
            print("The backend must contain 'framework'.")
            return False

        if content["backend"]["framework"] not in ["flask"]:
            print(f"Unsupported backend framework: {content['backend']['framework']}")
            return False

        if content["frontend"]["framework"] not in ["react"]:
            print(f"Unsupported frontend framework: {content['frontend']['framework']}")
            return False

        if content["backend"]["database"]["production"] not in ["postgresql", "sqlite"]:
            print(f"Unsupported database: {content['backend']['database']['production'] }")
            return False

        if content["backend"]["database"]["development"] not in ["postgresql", "sqlite"]:
            print(f"Unsupported database: {content['backend']['database']['development'] }")
            return False

        return True

    def parse(self, file):
        yaml_content = self.read(file)
        if self.validate(yaml_content):
            return ProjectConfiguration(yaml_content)
        else:
            # TODO: Raise Exception
            return ProjectConfiguration()


class ModelYAMLInterpreter(IYamlInterpreter):

    def validate(self, content):
        # Validate root
        if 'entities' not in content or 'relationships' not in content:
            print("The YAML file must contain 'entities' and 'relationships' at the root.")
            return False

        # Validate entities
        for entity in content['entities']:
            if 'name' not in entity:
                print("Each entity must have a 'name'.")
                return False
            if 'attributes' not in entity:
                print(f"The entity '{entity['name']}' must have 'attributes'.")
                return False
            for attribute in entity['attributes']:
                if 'name' not in attribute or 'type' not in attribute:
                    print(f"Each attribute in the entity '{entity['name']}' must have 'name' and 'type'.")
                    return False

        # Validate relationships
        for relationship in content['relationships']:
            if 'source' not in relationship or 'target' not in relationship:
                print("Each relationship must have 'source' and 'target'.")
                return False

        return True

    def parse(self, file):
        yaml_content = self.read(file)
        if self.validate(yaml_content):
            return EntityModel(yaml_content)
        else:
            # TODO: Raise Exception
            return EntityModel()
