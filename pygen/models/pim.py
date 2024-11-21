import yaml


class Attribute:
    """Represents an attribute of an entity."""
    def __init__(self, name, attr_type, primary_key=False, foreign_key=None, nullable=True):
        self._name = name
        self._type = attr_type
        self._primary_key = primary_key
        self._foreign_key = foreign_key
        self._nullable = nullable

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    @property
    def primary_key(self):
        return self._primary_key

    @property
    def foreign_key(self):
        return self._foreign_key

    @property
    def nullable(self):
        return self._nullable

    def to_dict(self):
        """Converts the attribute to a dictionary."""
        return {
            "name": self.name,
            "type": self.type,
            "primary_key": self.primary_key,
            "nullable": self.nullable
        }

    def __repr__(self):
        return f"Attribute(name={self.name}, type={self.type}, primary_key={self.primary_key}, nullable={self.nullable})"


class Relationship:
    """Represents a relationship between entities."""
    def __init__(self, name, target, rel_type):
        self._name = name
        self._target = target
        self._type = rel_type

    @property
    def name(self):
        return self._name

    @property
    def target(self):
        return self._target

    @property
    def type(self):
        return self._type

    def to_dict(self):
        """Converts the relationship to a dictionary."""
        return {
            "name": self.name,
            "target": self.target,
            "type": self.type
        }

    def __repr__(self):
        return f"Relationship(name={self.name}, target={self.target}, type={self.type})"


class Entity:
    """Represents an entity in the model."""
    def __init__(self, name):
        self._name = name
        self._attributes = []
        self._relationships = []

    @property
    def name(self):
        return self._name

    @property
    def attributes(self):
        return self._attributes

    @property
    def relationships(self):
        return self._relationships

    def add_attribute(self, name, attr_type, primary_key=False, foreign_key=None, nullable=True):
        """Adds an attribute to the entity."""
        attribute = Attribute(name, attr_type, primary_key, foreign_key, nullable)
        self._attributes.append(attribute)

    def add_relationship(self, name, target, rel_type):
        """Adds a relationship to the entity."""
        relationship = Relationship(name, target, rel_type)
        self._relationships.append(relationship)

    def to_dict(self):
        """Converts the entity to a dictionary."""
        return {
            "name": self.name,
            "attributes": [attr.to_dict() for attr in self.attributes],
            "relationships": [rel.to_dict() for rel in self.relationships]
        }

    def __repr__(self):
        return f"Entity(name={self.name}, attributes={self.attributes}, relationships={self.relationships})"


class PimModel:
    """Represents the entire PIM model."""
    def __init__(self):
        self._entities = []

    @property
    def entities(self):
        return self._entities

    def add_entity(self, entity):
        """Adds an entity to the model."""
        self._entities.append(entity)

    def export_to_yaml(self, file_path=None):
        """
        Exports the model to YAML format.

        Args:
            file_path (str, optional): If provided, saves the YAML output to the specified file.
                                       If None, returns the YAML string.

        Returns:
            str: The YAML representation of the model (if file_path is None).
        """
        model_dict = {
            "entities": [entity.to_dict() for entity in self.entities]
        }
        yaml_output = yaml.dump(model_dict, sort_keys=False, default_flow_style=False)

        if file_path:
            with open(file_path, "w") as file:
                file.write(yaml_output)
        else:
            return yaml_output

    def __repr__(self):
        return f"PimModel(entities={self.entities})"
