import yaml


class FlaskPsmField:
    """
    Represents a field of a resource in the Platform-Specific Model (PSM).

    Attributes:
        name (str): The name of the field.
        type (str): The data type of the field (e.g., String, Integer).
        primary_key (bool): Indicates if the field is a primary key. Defaults to False.
        foreign_key (str): Specifies the foreign key relationship, if any. Defaults to None.
        nullable (bool): Indicates if the field can be null. Defaults to True.
    """
    def __init__(self, name, field_type, primary_key=False, foreign_key=None, nullable=True):
        """
        Initializes a Field instance.

        Args:
            name (str): The name of the field.
            field_type (str): The data type of the field.
            primary_key (bool, optional): Whether the field is a primary key. Defaults to False.
            foreign_key (str, optional): Foreign key relationship, if any. Defaults to None.
            nullable (bool, optional): Whether the field can be null. Defaults to True.
        """
        self._name = name
        self._type = field_type
        self._primary_key = primary_key
        self._foreign_key = foreign_key
        self._nullable = nullable

    @property
    def name(self):
        """Returns the name of the field."""
        return self._name

    @property
    def type(self):
        """Returns the data type of the field."""
        return self._type

    @property
    def primary_key(self):
        """Returns whether the field is a primary key."""
        return self._primary_key

    @property
    def foreign_key(self):
        """Returns the foreign key relationship of the field."""
        return self._foreign_key

    @property
    def nullable(self):
        """Returns whether the field can be null."""
        return self._nullable

    def to_dict(self):
        """
        Converts the field to a dictionary representation.

        Returns:
            dict: A dictionary containing field properties.
        """
        return {
            "name": self.name,
            "type": self.type,
            "primary_key": self.primary_key,
            "nullable": self.nullable
        }

    def __repr__(self):
        """Returns a string representation of the field."""
        return (f"Field(name={self._name}, type={self._type}, "
                f"primary_key={self._primary_key}, nullable={self._nullable})")


class FlaskPsmRelationship:
    """
    Represents a relationship between resources in the Platform-Specific Model (PSM).

    Attributes:
        name (str): The name of the relationship.
        target (str): The target entity of the relationship.
        type (str): The type of the relationship (e.g., one-to-one, one-to-many).
        back_populates (str): The back reference to the source entity. Defaults to None.
    """
    def __init__(self, name, target, rel_type, back_populates=None):
        """
        Initializes a Relationship instance.

        Args:
            name (str): The name of the relationship.
            target (str): The target entity of the relationship.
            rel_type (str): The type of the relationship.
            back_populates (str, optional): Back reference to the source entity. Defaults to None.
        """
        self._name = name
        self._target = target
        self._type = rel_type
        self._back_populates = back_populates

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

    @property
    def back_populates(self):
        """Returns the back reference to the source entity."""
        return self._back_populates

    def to_dict(self):
        """
        Converts the relationship to a dictionary representation.

        Returns:
            dict: A dictionary containing relationship properties.
        """
        return {
            "name": self.name,
            "target": self.target,
            "type": self.type,
            "back_populates": self.back_populates,
        }

    def __repr__(self):
        """Returns a string representation of the relationship."""
        return (f"Relationship(name={self._name}, target={self._target}, "
                f"type={self._type}, back_populates={self._back_populates})")


class FlaskPsmEntity:
    """
    Represents a resource or entity in the Platform-Specific Model (PSM).

    Attributes:
        name (str): The name of the entity.
        table_name (str): The name of the table in the database.
        fields (list): A list of Field objects defining the entity's fields.
        relationships (list): A list of Relationship objects defining the entity's relationships.
    """
    def __init__(self, name, table_name=None):
        """
        Initializes an Entity instance.

        Args:
            name (str): The name of the entity.
            table_name (str, optional): The name of the database table. Defaults to the pluralized entity name.
        """
        self._name = name
        self._table_name = table_name or name.lower() + "s"
        self._fields = []
        self._relationships = []

    @property
    def name(self):
        """Returns the name of the entity."""
        return self._name

    @property
    def table_name(self):
        """Returns the name of the database table."""
        return self._table_name

    @property
    def fields(self):
        """Returns the list of fields of the entity."""
        return self._fields

    @property
    def relationships(self):
        """Returns the list of relationships of the entity."""
        return self._relationships

    def add_field(self, name, field_type, primary_key=False, foreign_key=None, nullable=True):
        """
        Adds a field to the entity.

        Args:
            name (str): The name of the field.
            field_type (str): The data type of the field.
            primary_key (bool, optional): Whether the field is a primary key. Defaults to False.
            foreign_key (str, optional): Foreign key relationship, if any. Defaults to None.
            nullable (bool, optional): Whether the field can be null. Defaults to True.
        """
        field = FlaskPsmField(name, field_type, primary_key, foreign_key, nullable)
        self._fields.append(field)

    def add_relationship(self, name, target, rel_type, back_populates=None):
        """
        Adds a relationship to the entity.

        Args:
            name (str): The name of the relationship.
            target (str): The target entity of the relationship.
            rel_type (str): The type of the relationship.
            back_populates (str, optional): Back reference to the source entity. Defaults to None.
        """
        relationship = FlaskPsmRelationship(name, target, rel_type, back_populates)
        self._relationships.append(relationship)

    def to_dict(self):
        """
        Converts the entity to a dictionary representation.

        Returns:
            dict: A dictionary containing entity properties.
        """
        return {
            "name": self.name,
            "table_name": self.table_name,
            "fields": [field.to_dict() for field in self.fields],
            "relationships": [rel.to_dict() for rel in self.relationships]
        }

    def __repr__(self):
        """Returns a string representation of the entity."""
        return (f"Entity(name={self._name}, table_name={self._table_name}, "
                f"fields={self._fields}, relationships={self._relationships})")


class FlaskPsmModel:
    """
    Represents the entire Platform-Specific Model (PSM).

    Attributes:
        entities (list): A list of Entity objects in the model.
    """
    def __init__(self):
        """Initializes an empty PSM model."""
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

    def to_yaml(self, file_path=None):
        """
        Exports the PSM model to YAML format.

        Args:
            file_path (str, optional): If provided, saves the YAML output to the specified file.

        Returns:
            str: The YAML representation of the model if `file_path` is None.
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
        return f"Model(entities={self.entities})"
