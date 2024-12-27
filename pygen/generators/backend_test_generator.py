from jinja2 import Environment, FileSystemLoader
import os


class BackendTestGenerator:
    def __init__(self, config, psm_model, tests_path):
        """
        Initializes the BackendTestGenerator.

        Args:
            config (ProjectConfiguration): Configuration of the project.
            psm_model (PsmModel): Platform-Specific Model for the backend.
            tests_path (str): Path where the test files will be generated.
        """
        self._config = config
        self._psm_model = psm_model
        self._tests_path = tests_path
        self._templates_path = "pygen/generators/templates/backend/tests"
        self._env = Environment(loader=FileSystemLoader(self._templates_path))

    def generate(self):
        """
        Generates unit test files for controllers, services, and models.
        """
        os.makedirs(self._tests_path, exist_ok=True)

        for entity in self._psm_model.entities:
            self._generate_controller_tests(entity)
            self._generate_service_tests(entity)
            self._generate_schema_tests(entity)
            self._generate_model_tests(entity)

    def _generate_controller_tests(self, entity):
        """
        Generates unit tests for the controller of an entity.

        Args:
            entity (Entity): The entity to generate tests for.
        """
        template = self._env.get_template("controller_test_template.jinja2")
        rendered = template.render(entity=entity)
        file_path = os.path.join(self._tests_path, f"test_{entity.name.lower()}_controller.py")
        with open(file_path, "w") as file:
            file.write(rendered)
        print(f"Controller test generated for {entity.name} at {file_path}")

    def _generate_service_tests(self, entity):
        """
        Generates unit tests for the service of an entity.

        Args:
            entity (Entity): The entity to generate tests for.
        """
        template = self._env.get_template("service_test_template.jinja2")
        rendered = template.render(entity=entity)
        file_path = os.path.join(self._tests_path, f"test_{entity.name.lower()}_service.py")
        with open(file_path, "w") as file:
            file.write(rendered)
        print(f"Service test generated for {entity.name} at {file_path}")

    def _generate_schema_tests(self, entity):
        """
        Generates unit tests for the model of an entity.

        Args:
            entity (Entity): The entity to generate tests for.
        """
        template = self._env.get_template("schema_test_template.jinja2")
        rendered = template.render(entity=entity)
        file_path = os.path.join(self._tests_path, f"test_{entity.name.lower()}_schema.py")
        with open(file_path, "w") as file:
            file.write(rendered)
        print(f"Schema test generated for {entity.name} at {file_path}")

    def _generate_model_tests(self, entity):
        """
        Generates unit tests for the model of an entity.

        Args:
            entity (Entity): The entity to generate tests for.
        """
        template = self._env.get_template("model_test_template.jinja2")
        rendered = template.render(entity=entity)
        file_path = os.path.join(self._tests_path, f"test_{entity.name.lower()}_model.py")
        with open(file_path, "w") as file:
            file.write(rendered)
        print(f"Model test generated for {entity.name} at {file_path}")


class SecurityTestGenerator:
    def __init__(self, config, psm_model, tests_path):
        """
        Initializes the SecurityTestGenerator.

        Args:
            config (ProjectConfiguration): Configuration of the project.
            psm_model (PsmModel): Platform-Specific Model for the backend.
            tests_path (str): Path where the security test files will be generated.
        """
        self._config = config
        self._psm_model = psm_model
        self._tests_path = tests_path
        self._templates_path = "pygen/generators/templates/backend/security_tests"
        self._env = Environment(loader=FileSystemLoader(self._templates_path))

    def generate(self):
        """
        Generates security test files for all controllers and the Pyntfile.
        """
        os.makedirs(self._tests_path, exist_ok=True)

        for entity in self._psm_model.entities:
            self._generate_security_tests(entity)

        self._generate_pyntfile()

    def _generate_security_tests(self, entity):
        """
        Generates pytest-based security tests for a specific entity's controller.

        Args:
            entity (Entity): The entity to generate tests for.
        """
        template = self._env.get_template("security_test_template.jinja2")
        rendered = template.render(entity=entity)
        file_path = os.path.join(self._tests_path, f"test_{entity.name.lower()}_security.py")
        with open(file_path, "w") as file:
            file.write(rendered)
        print(f"Security tests generated for {entity.name} at {file_path}")

    def _generate_pyntfile(self):
        """
        Generates a Pyntfile for automating the execution of security tests.
        """
        template = self._env.get_template("pyntfile_template.jinja2")
        rendered = template.render(model=self._psm_model)
        file_path = os.path.join(self._tests_path, "Pyntfile")
        with open(file_path, "w") as file:
            file.write(rendered)
        print(f"Pyntfile generated at {file_path}")


class IntegrationTestGenerator:
    def __init__(self, config, psm_model, tests_path):
        """
        Initializes the IntegrationTestGenerator.

        Args:
            config (ProjectConfiguration): Configuration of the project.
            psm_model (PsmModel): Platform-Specific Model for the backend.
            tests_path (str): Path where the integration test files will be generated.
        """
        self._config = config
        self._psm_model = psm_model
        self._tests_path = tests_path
        self._templates_path = "pygen/generators/templates/backend/integration_tests"
        self._env = Environment(loader=FileSystemLoader(self._templates_path))

    def generate(self):
        """
        Generates integration test files for all entities.
        """
        os.makedirs(self._tests_path, exist_ok=True)

        for entity in self._psm_model.entities:
            self._generate_integration_tests(entity)

    def _generate_integration_tests(self, entity):
        """
        Generates integration tests for a specific entity.

        Args:
            entity (Entity): The entity to generate tests for.
        """
        template = self._env.get_template("integration_test_template.jinja2")
        rendered = template.render(entity=entity)
        file_path = os.path.join(self._tests_path, f"test_{entity.name.lower()}_integration.py")
        with open(file_path, "w") as file:
            file.write(rendered)
        print(f"Integration tests generated for {entity.name} at {file_path}")
