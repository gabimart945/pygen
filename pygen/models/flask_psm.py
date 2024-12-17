import yaml


class Field:
    """Represents a field of a resource in the PSM model."""
    def __init__(self, name, field_type, primary_key=False, foreign_key=None, nullable=True):
        self._name = name
        self._type = field_type
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
        """Converts the field to a dictionary."""
        return {
            "name": self.name,
            "type": self.type,
            "primary_key": self.primary_key,
            "nullable": self.nullable
        }

    def __repr__(self):
        return (f"Field(name={self._name}, type={self._type}, "
                f"primary_key={self._primary_key}, nullable={self._nullable})")


class Relationship:
    """Represents a relationship between resources in the PSM model."""
    def __init__(self, name, target, rel_type, back_populates=None):
        self._name = name
        self._target = target
        self._type = rel_type
        self._back_populates = back_populates


    @property
    def name(self):
        return self._name

    @property
    def target(self):
        return self._target

    @property
    def type(self):
        return self._type

    @property
    def back_populates(self):
        return self._back_populates

    def to_dict(self):
        """Converts the relationship to a dictionary."""
        return {
            "name": self.name,
            "target": self.target,
            "type": self.type,
            "back_populates": self.back_populates,
            "source": self.source,
            "target_relationship_name": self.target_relationship_name,
        }

    def __repr__(self):
        return (f"Relationship(name={self._name}, target={self._target}, "
                f"type={self._type}, back_populates={self._back_populates}")


class Entity:
    """Represents a resource or entity in the PSM model."""
    def __init__(self, name, table_name=None):
        self._name = name
        self._table_name = table_name or name.lower() + "s"
        self._fields = []
        self._relationships = []

    @property
    def name(self):
        return self._name

    @property
    def table_name(self):
        return self._table_name

    @property
    def fields(self):
        return self._fields

    @property
    def relationships(self):
        return self._relationships

    def add_field(self, name, field_type, primary_key=False, foreign_key=None, nullable=True):
        """Adds a field to the entity."""
        field = Field(name, field_type, primary_key, foreign_key, nullable)
        self._fields.append(field)

    def add_relationship(self, name, target, rel_type, back_populates=None):
        """Adds a relationship to the entity."""
        relationship = Relationship(name, target, rel_type, back_populates)
        self._relationships.append(relationship)

    def to_dict(self):
        """Converts the entity to a dictionary."""
        return {
            "name": self.name,
            "table_name": self.table_name,
            "fields": [field.to_dict() for field in self.fields],
            "relationships": [rel.to_dict() for rel in self.relationships]
        }

    def __repr__(self):
        return (f"Entity(name={self._name}, table_name={self._table_name}, "
                f"fields={self._fields}, relationships={self._relationships})")


class PsmModel:
    """Represents the entire PSM model."""
    def __init__(self):
        self._entities = []

    @property
    def entities(self):
        return self._entities

    def add_entity(self, entity):
        """Adds an entity to the model."""
        self._entities.append(entity)

    def to_yaml(self, file_path=None):
        """
        Exports the PSM model to a YAML format.

        Args:
            file_path (str, optional): If provided, saves the YAML to the specified file.

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
        return f"Model(entities={self.entities})"
