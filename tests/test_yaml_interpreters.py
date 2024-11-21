import pytest
from pygen.yaml_interpreters import ConfigurationYAMLInterpreter, ModelYAMLInterpreter
from pygen.project_configuration import ProjectConfiguration
from pygen.models.cim import CimModel
from pygen.exceptions import ConfigurationException, ModelValidationException


# Tests for ConfigurationYAMLInterpreter
def test_validate_and_parse_valid_config():
    interpreter = ConfigurationYAMLInterpreter()
    with open('tests/fixtures/valid_config.yaml', 'r') as f:
        config = interpreter.parse(f)
    assert isinstance(config, ProjectConfiguration)
    assert config.project_name == 'TestProject'
    assert config.backend.architecture == 'monolithic'
    assert config.backend.framework == 'flask'
    assert config.backend.database.production == 'postgresql'
    assert config.backend.database.development == 'sqlite'
    assert config.frontend.framework == 'react'


def test_invalid_framework():
    interpreter = ConfigurationYAMLInterpreter()
    with pytest.raises(ConfigurationException):
        with open('tests/fixtures/invalid_config_framework.yaml', 'r') as f:
            interpreter.parse(f)


# Tests for ModelYAMLInterpreter
def test_validate_and_parse_valid_model():
    interpreter = ModelYAMLInterpreter()
    with open('tests/fixtures/valid_model.yaml', 'r') as f:
        model = interpreter.parse(f)
    assert isinstance(model, CimModel)
    assert len(model._entities) == 1
    assert len(model._relationships) == 1


def test_missing_entities_in_model():
    interpreter = ModelYAMLInterpreter()
    with pytest.raises(ModelValidationException):
        with open('tests/fixtures/invalid_model_missing_entities.yaml', 'r') as f:
            interpreter.parse(f)
