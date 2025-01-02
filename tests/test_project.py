import unittest
from unittest.mock import patch, MagicMock
from pygen.project import Project
from pygen.exceptions import ConfigurationException, ModelValidationException

class TestProject(unittest.TestCase):

    @patch('pygen.project.Project.create_directories')
    @patch('pygen.project.Project.generate_backend')
    @patch('pygen.project.Project.generate_frontend')
    @patch('pygen.project.Project.generate_ci_cd')
    @patch('pygen.project.Project.run_tests')
    def generates_project_structure(self, mock_run_tests, mock_generate_ci_cd, mock_generate_frontend, mock_generate_backend, mock_create_directories):
        model = MagicMock()
        config = MagicMock()
        project = Project(model, config)
        project.generate_project()
        mock_create_directories.assert_called_once()
        mock_generate_backend.assert_called_once()
        mock_generate_frontend.assert_called_once()
        mock_generate_ci_cd.assert_called_once()
        mock_run_tests.assert_called_once()

    def raises_configuration_exception(self):
        with self.assertRaises(ConfigurationException):
            raise ConfigurationException("Configuration error")

    def raises_model_validation_exception(self):
        with self.assertRaises(ModelValidationException):
            raise ModelValidationException("Model validation error")

if __name__ == '__main__':
    unittest.main()