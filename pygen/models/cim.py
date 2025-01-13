class CimAttribute:
    """
    Represents an attribute of an entity in the UML model.

    Attributes:
        name (str): The name of the attribute.
        type (str): The type of the attribute (e.g., String, Integer).
    """

    def __init__(self, yaml_attribute):
        """
        Initializes an Attribute instance.

        Args:
            yaml_attribute (dict): Dictionary containing the attribute data, with keys 'name' and 'type'.
        """
        self._name = yaml_attribute['name']
        self._type = yaml_attribute['type']

    @property
    def name(self):
        """Returns the name of the attribute."""
        return self._name

    @property
    def type(self):
        """Returns the type of the attribute."""
        return self._type

    def __repr__(self):
        """Returns a string representation of the attribute."""
        return f"Attribute(name={self._name!r}, type={self._type!r})"


class CimEntity:
    """
    Represents an entity in the UML model.

    Attributes:
        name (str): The name of the entity.
        attributes (list): A list of Attribute objects defining the entity's attributes.
    """

    def __init__(self, yaml_entity):
        """
        Initializes an Entity instance.

        Args:
            yaml_entity (dict): Dictionary containing the entity data, including 'name' and a list of 'attributes'.
        """
        self._name = yaml_entity["name"]
        self._attributes = [CimAttribute(attribute) for attribute in yaml_entity['attributes']]

    @property
    def name(self):
        """Returns the name of the entity."""
        return self._name

    @property
    def attributes(self):
        """Returns the list of attributes of the entity."""
        return self._attributes

    def __repr__(self):
        """Returns a string representation of the entity."""
        return f"Entity(name={self._name!r}, attributes={self._attributes!r})"


class CimRelationship:
    """
    Represents a relationship between two entities in the UML model.

    Attributes:
        source (str): The source entity of the relationship.
        target (str): The target entity of the relationship.
        type (str): The type of the relationship (e.g., association, aggregation, composition).
        source_multiplicity (str): The multiplicity at the source entity (e.g., 1, 1..*, 0..1, 0..*).
        target_multiplicity (str): The multiplicity at the target entity (e.g., 1, 1..*, 0..1, 0..*).
    """

    def __init__(self, yaml_relationship):
        """
        Initializes a Relationship instance.

        Args:
            yaml_relationship (dict): Dictionary containing the relationship data,
                                      including 'source', 'target', 'type', and 'multiplicity'.
                                      Defaults:
                                          'type': 'association'
                                          'multiplicity': 'one-to-one'
        """
        self._source = yaml_relationship['source']
        self._target = yaml_relationship['target']
        self._type = yaml_relationship.get('type', 'association')  # Default to 'association'
        self._source_multiplicity = str(yaml_relationship.get('source_multiplicity', '1'))  # Default to '1'
        self._target_multiplicity = str(yaml_relationship.get('target_multiplicity', '1'))  # Default to '1'

    @property
    def source(self):
        """Returns the source entity of the relationship."""
        return self._source

    @property
    def target(self):
        """Returns the target entity of the relationship."""
        return self._target

    @property
    def type(self):
        """Returns the type of the relationship."""
        return self._type

    @property
    def source_multiplicity(self):
        """Returns the multiplicity at the source entity."""
        return self._source_multiplicity

    @property
    def target_multiplicity(self):
        """Returns the multiplicity at the target entity."""
        return self._target_multiplicity

    def __repr__(self):
        """Returns a string representation of the relationship."""
        return (f"Relationship(source={self._source!r}, target={self._target!r}, "
                f"type={self._type!r}, source_multiplicity={self._source_multiplicity!r}, "
                f"target_multiplicity={self._target_multiplicity!r})")


class CimModel:
    """
    Represents the entire UML conceptual model, including entities and relationships.

    Attributes:
        entities (list): A list of Entity objects in the model.
        relationships (list): A list of Relationship objects in the model.
    """

    def __init__(self, yaml_model=None):
        """
        Initializes a CimModel instance.

        Args:
            yaml_model (dict, optional): Dictionary containing the entire model data,
                                         including lists of 'entities' and 'relationships'.
                                         If provided, entities and relationships are initialized from the YAML data.
        """
        self._entities = []
        self._relationships = []
        if yaml_model is not None:
            for entity in yaml_model['entities']:
                self._entities.append(Entity(entity))
            for relationship in yaml_model['relationships']:
                self._relationships.append(Relationship(relationship))

    @property
    def entities(self):
        """Returns the list of entities in the model."""
        return self._entities

    @property
    def relationships(self):
        """Returns the list of relationships in the model."""
        return self._relationships

    def __repr__(self):
        """Returns a string representation of the UML model."""
        return f"CimModel(entities={self._entities!r}, relationships={self._relationships!r})"
