class PIMAttribute:
    """
    Represents an attribute in the Platform Independent Model (PIM).

    Attributes:
        name (str): The name of the attribute.
        type (str): The type of the attribute (e.g., String, Integer, etc.).
        nullable (bool): Indicates if the attribute can be null. Defaults to True.
    """
    def __init__(self, name: str, attr_type: str, nullable: bool = True):
        """
        Initializes a PIM attribute.

        Args:
            name (str): The name of the attribute.
            attr_type (str): The type of the attribute (e.g., String, Integer, etc.).
            nullable (bool): Whether the attribute can be null. Defaults to True.
        """
        self.name = name
        self.type = attr_type
        self.nullable = nullable

    def __repr__(self):
        """Returns a string representation of the PIM attribute."""
        return f"PIMAttribute(name={self.name!r}, type={self.type!r}, nullable={self.nullable})"


class PIMRelationship:
    """
    Represents a relationship between entities in the Platform Independent Model (PIM).

    Attributes:
        target (str): The name of the target entity.
        type (str): The type of the relationship (e.g., one-to-one, one-to-many).
    """
    def __init__(self, target: str, rel_type: str):
        """
        Initializes a PIM relationship.

        Args:
            target (str): The name of the target entity.
            rel_type (str): The type of the relationship (e.g., one-to-one, one-to-many).
        """
        self.target = target
        self.type = rel_type

    def __repr__(self):
        """Returns a string representation of the PIM relationship."""
        return f"PIMRelationship(target={self.target!r}, type={self.type!r})"


class PIMEntity:
    """
    Represents an entity in the Platform Independent Model (PIM).

    Attributes:
        name (str): The name of the entity.
        attributes (list): A list of PIMAttribute objects associated with the entity.
        relationships (list): A list of PIMRelationship objects defining relationships with other entities.
    """
    def __init__(self, name: str):
        """
        Initializes a PIM entity.

        Args:
            name (str): The name of the entity.
        """
        self.name = name
        self.attributes = []
        self.relationships = []

    def add_attribute(self, name: str, attr_type: str, nullable: bool = True):
        """
        Adds an attribute to the entity.

        Args:
            name (str): The name of the attribute.
            attr_type (str): The type of the attribute.
            nullable (bool): Whether the attribute can be null. Defaults to True.
        """
        self.attributes.append(PIMAttribute(name, attr_type, nullable))

    def add_relationship(self, target: str, rel_type: str):
        """
        Adds a relationship to the entity.

        Args:
            target (str): The name of the target entity.
            rel_type (str): The type of the relationship.
        """
        self.relationships.append(PIMRelationship(target, rel_type))

    def __repr__(self):
        """Returns a string representation of the PIM entity."""
        return f"PIMEntity(name={self.name!r}, attributes={self.attributes!r}, relationships={self.relationships!r})"


class PIMModel:
    """
    Represents the complete Platform Independent Model (PIM).

    Attributes:
        entities (list): A list of PIMEntity objects representing the entities in the model.
    """
    def __init__(self):
        """
        Initializes an empty PIM model.
        """
        self.entities = []

    def add_entity(self, name: str) -> PIMEntity:
        """
        Adds an entity to the model.

        Args:
            name (str): The name of the entity.

        Returns:
            PIMEntity: The created entity.
        """
        entity = PIMEntity(name)
        self.entities.append(entity)
        return entity

    def __repr__(self):
        """Returns a string representation of the PIM model."""
        return f"PIMModel(entities={self.entities!r})"
