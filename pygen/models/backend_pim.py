import yaml


class Attribute:
    """
    Represents an attribute of an entity.

    Attributes:
        name (str): The name of the attribute.
        type (str): The data type of the attribute (e.g., String, Integer).
        primary_key (bool): Indicates if the attribute is a primary key. Defaults to False.
        foreign_key (str): Specifies the foreign key relationship, if any. Defaults to None.
        nullable (bool): Indicates if the attribute can be null. Defaults to True.
    """
    def __init__(self, name, attr_type, primary_key=False, foreign_key=None, nullable=True):
        """
        Initializes an Attribute instance.

        Args:
            name (str): The name of the attribute.
            attr_type (str): The data type of the attribute.
            primary_key (bool, optional): Whether the attribute is a primary key. Defaults to False.
            foreign_key (str, optional): Foreign key relationship, if any. Defaults to None.
            nullable (bool, optional): Whether the attribute can be null. Defaults to True.
        """
        self._name = name
        self._type = attr_type
        self._primary_key = primary_key
        self._foreign_key = foreign_key
        self._nullable = nullable

    @property
    def name(self):
        """Returns the name of the attribute."""
        return self._name

    @property
    def type(self):
        """Returns the data type of the attribute."""
        return self._type

    @property
    def primary_key(self):
        """Returns whether the attribute is a primary key."""
        return self._primary_key

    @property
    def foreign_key(self):
        """Returns the foreign key relationship of the attribute."""
        return self._foreign_key

    @property
    def nullable(self):
        """Returns whether the attribute can be null."""
        return self._nullable

    def to_dict(self):
        """
        Converts the attribute to a dictionary representation.

        Returns:
            dict: A dictionary containing attribute properties.
        """
        return {
            "name": self.name,
            "type": self.type,
            "primary_key": self.primary_key,
            "nullable": self._nullable
        }

    def __repr__(self):
        """Returns a string representation of the attribute."""
        return f"Attribute(name={self.name}, type={self.type}, primary_key={self.primary_key}, nullable={self.nullable})"


class Relationship:
    """
    Represents a relationship between entities.

    Attributes:
        name (str): The name of the relationship.
        target (str): The target entity of the relationship.
        type (str): The type of the relationship (e.g., association, aggregation, composition).
    """
    def __init__(self, name, target, rel_type):
        """
        Initializes a Relationship instance.

        Args:
            name (str): The name of the relationship.
            target (str): The target entity of the relationship.
            rel_type (str): The type of the relationship.
        """
        self._name = name
        self._target = target
        self._type = rel_type

    @property
    def name(self):
        """Returns the name of the relationship."""
        return self._name

    @property
    def target(self):
        """Returns the target entity of the relationship."""
        return self._target

    @property
    def type(self):
        """Returns the type of the relationship."""
        return self._type

    def to_dict(self):
        """
        Converts the relationship to a dictionary representation.

        Returns:
            dict: A dictionary containing relationship properties.
        """
        return {
            "name": self.name,
            "target": self.target,
            "type": self.type
        }

    def __repr__(self):
        """Returns a string representation of the relationship."""
        return f"Relationship(name={self.name}, target={self.target}, type={self.type})"


class Entity:
    """
    Represents an entity in the model.

    Attributes:
        name (str): The name of the entity.
        attributes (list): A list of Attribute objects defining the entity's attributes.
        relationships (list): A list of Relationship objects defining the entity's relationships.
    """
    def __init__(self, name):
        """
        Initializes an Entity instance.

        Args:
            name (str): The name of the entity.
        """
        self._name = name
        self._attributes = []
        self._relationships = []

    @property
    def name(self):
        """Returns the name of the entity."""
        return self._name

    @property
    def attributes(self):
        """Returns the list of attributes of the entity."""
        return self._attributes

    @property
    def relationships(self):
        """Returns the list of relationships of the entity."""
        return self._relationships

    def add_attribute(self, name, attr_type, primary_key=False, foreign_key=None, nullable=True):
        """
        Adds an attribute to the entity.

        Args:
            name (str): The name of the attribute.
            attr_type (str): The data type of the attribute.
            primary_key (bool, optional): Whether the attribute is a primary key. Defaults to False.
            foreign_key (str, optional): Foreign key relationship, if any. Defaults to None.
            nullable (bool, optional): Whether the attribute can be null. Defaults to True.
        """
        attribute = Attribute(name, attr_type, primary_key, foreign_key, nullable)
        self._attributes.append(attribute)

    def add_relationship(self, name, target, rel_type):
        """
        Adds a relationship to the entity.

        Args:
            name (str): The name of the relationship.
            target (str): The target entity of the relationship.
            rel_type (str): The type of the relationship.
        """
        relationship = Relationship(name, target, rel_type)
        self._relationships.append(relationship)

    def to_dict(self):
        """
        Converts the entity to a dictionary representation.

        Returns:
            dict: A dictionary containing entity properties.
        """
        return {
            "name": self.name,
            "attributes": [attr.to_dict() for attr in self.attributes],
            "relationships": [rel.to_dict() for rel in self.relationships]
        }

    def __repr__(self):
        """Returns a string representation of the entity."""
        return f"Entity(name={self.name}, attributes={self.attributes}, relationships={self.relationships})"


class PimModel:
    """
    Represents the entire Platform Independent Model (PIM).

    Attributes:
        entities (list): A list of Entity objects defining the model's entities.
    """
    def __init__(self):
        """Initializes an empty PimModel."""
        self._entities = []

    @property
    def entities(self):
        """Returns the list of entities in the model."""
        return self._entities

    def add_entity(self, entity):
        """
        Adds an entity to the model.

        Args:
            entity (Entity): The entity to add.
        """
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
        """Returns a string representation of the model."""
        return f"PimModel(entities={self.entities})"
