class Attribute:
    def __init__(self, yaml_attribute):
        self._name = yaml_attribute['name']
        self._type = yaml_attribute['type']


class Entity:

    def __init__(self, yaml_entity):
        self._name = yaml_entity["name"]
        self._attributes = []
        for attribute in yaml_entity['attributes']:
            self._attributes.append(Attribute(attribute))


class Relationship:
    def __init__(self, yaml_relationship):
        self._source = yaml_relationship['source']
        self._target = yaml_relationship['target']


class EntityModel:

    def __init__(self, yaml_model=None):
        self._entities = []
        self._relationships = []
        if yaml_model is not None:
            for entity in yaml_model['entities']:
                self._entities.append(Entity(entity))
            for relationship in yaml_model['relationships']:
                self._relationships.append(Relationship(relationship))
