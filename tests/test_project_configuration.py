import unittest
from pygen.project_configuration import ProjectConfiguration, BackendConfiguration, FrontendConfiguration, DbConfiguration
from pygen.sanitizers import sanitize_filename

class TestProjectConfiguration(unittest.TestCase):

    def initializes_with_yaml_data(self):
        yaml_data = {
            "project_name": "TestProject",
            "auth": "basic",
            "backend": {
                "architecture": "monolithic",
                "framework": "flask",
                "database": {
                    "production": "postgresql",
                    "development": "sqlite"
                }
            },
            "frontend": {
                "framework": "react"
            }
        }
        config = ProjectConfiguration(yaml_data)
        self.assertEqual(config.project_name, "TestProject")
        self.assertEqual(config.auth, "basic")
        self.assertEqual(config.backend.architecture, "monolithic")
        self.assertEqual(config.backend.framework, "flask")
        self.assertEqual(config.backend.database.production, "postgresql")
        self.assertEqual(config.backend.database.development, "sqlite")
        self.assertEqual(config.frontend.framework, "react")

    def initializes_without_yaml_data(self):
        config = ProjectConfiguration()
        self.assertIsNone(config.project_name)
        self.assertIsNone(config.auth)
        self.assertIsNone(config.backend.architecture)
        self.assertIsNone(config.backend.framework)
        self.assertIsNone(config.backend.database.production)
        self.assertIsNone(config.backend.database.development)
        self.assertIsNone(config.frontend.framework)

    def sets_project_name(self):
        config = ProjectConfiguration()
        config.set_project_name("NewProject")
        self.assertEqual(config.project_name, sanitize_filename("NewProject"))

    def sets_authentication_method(self):
        config = ProjectConfiguration()
        config.set_auth("basic")
        self.assertEqual(config.auth, "basic")
        with self.assertRaises(ValueError):
            config.set_auth("unsupported_auth")

    def sets_backend_architecture(self):
        config = BackendConfiguration()
        config.set_architecture("monolithic")
        self.assertEqual(config.architecture, "monolithic")
        with self.assertRaises(ValueError):
            config.set_architecture("unsupported_architecture")

    def sets_backend_framework(self):
        config = BackendConfiguration()
        config.set_framework("flask")
        self.assertEqual(config.framework, "flask")
        with self.assertRaises(ValueError):
            config.set_framework("unsupported_framework")

    def sets_database_configuration(self):
        config = BackendConfiguration()
        config.set_database("production", "postgresql")
        self.assertEqual(config.database.production, "postgresql")
        config.set_database("development", "sqlite")
        self.assertEqual(config.database.development, "sqlite")
        with self.assertRaises(ValueError):
            config.set_database("production", "unsupported_database")
        with self.assertRaises(ValueError):
            config.set_database("unsupported_environment", "postgresql")

    def sets_frontend_framework(self):
        config = FrontendConfiguration()
        config.set_framework("react")
        self.assertEqual(config.framework, "react")
        with self.assertRaises(ValueError):
            config.set_framework("unsupported_framework")

if __name__ == '__main__':
    unittest.main()