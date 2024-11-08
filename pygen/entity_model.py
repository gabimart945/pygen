class Attribute:
    """Represents an attribute of an entity in the UML model."""

    def __init__(self, yaml_attribute):
        """
        Initializes an Attribute instance.

        Args:
            yaml_attribute (dict): Dictionary containing the attribute data,
                                   with keys 'name' and 'type'.
        """
        self._name = yaml_attribute['name']
        self._type = yaml_attribute['type']


class Entity:
    """Represents an entity in the UML model."""

    def __init__(self, yaml_entity):
        """
        Initializes an Entity instance.

        Args:
            yaml_entity (dict): Dictionary containing the entity data,
                                including 'name' and a list of 'attributes'.
        """
        self._name = yaml_entity["name"]
        self._attributes = [Attribute(attribute) for attribute in yaml_entity['attributes']]


class Relationship:
    """Represents a relationship between two entities in the UML model."""

    def __init__(self, yaml_relationship):
        """
        Initializes a Relationship instance.

        Args:
            yaml_relationship (dict): Dictionary containing the relationship data,
                                      including 'source', 'target', 'type', and 'multiplicity'.
                                      'type' defaults to 'association' if not provided.
                                      'multiplicity' defaults to 'one-to-one' if not provided.
        """
        self._source = yaml_relationship['source']
        self._target = yaml_relationship['target']
        self._type = yaml_relationship.get('type', 'association')  # Default to 'association'
        self._multiplicity = yaml_relationship.get('multiplicity', 'one-to-one')  # Default to 'one-to-one'


class EntityModel:
    """Represents the entire UML model, including entities and relationships."""

    def __init__(self, yaml_model=None):
        """
        Initializes an EntityModel instance.

        Args:
            yaml_model (dict, optional): Dictionary containing the entire model data,
                                         including lists of 'entities' and 'relationships'.
                                         If provided, entities and relationships are initialized
                                         from the YAML data.
        """
        self._entities = []
        self._relationships = []
        if yaml_model is not None:
            for entity in yaml_model['entities']:
                self._entities.append(Entity(entity))
            for relationship in yaml_model['relationships']:
                self._relationships.append(Relationship(relationship))
