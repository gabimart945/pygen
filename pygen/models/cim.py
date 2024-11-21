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

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type

    def __repr__(self):
        return f"Attribute(name={self._name!r}, type={self._type!r})"


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

    @property
    def name(self):
        return self._name

    @property
    def attributes(self):
        return self._attributes

    def __repr__(self):
        return f"Entity(name={self._name!r}, attributes={self._attributes!r})"


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
        # Default to 'association', Options: association, aggregation, composition
        self._type = yaml_relationship.get('type', 'association')
        # Default to '1', Options: 1, 1..*, 0..1, 0..*
        self._source_multiplicity = str(yaml_relationship.get('source_multiplicity', '1'))
        # Default to '1', Options: 1, 1..*, 0..1, 0..*
        self._target_multiplicity = str(yaml_relationship.get('target_multiplicity', '1'))

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target

    @property
    def type(self):
        return self._type

    @property
    def source_multiplicity(self):
        return self._source_multiplicity

    @property
    def target_multiplicity(self):
        return self._target_multiplicity

    def __repr__(self):
        return (f"Relationship(source={self._source!r}, target={self._target!r}, "
                f"type={self._type!r}, source_multiplicity={self._source_multiplicity!r}, "
                f"target_multiplicity={self._target_multiplicity!r})")


class CimModel:
    """Represents the entire UML conceptual model, including entities and relationships."""

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

    @property
    def entities(self):
        return self._entities

    @property
    def relationships(self):
        return self._relationships

    def __repr__(self):
        return f"CimModel(entities={self._entities!r}, relationships={self._relationships!r})"
