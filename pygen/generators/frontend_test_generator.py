from jinja2 import Environment, FileSystemLoader
import os

class ReactTestGenerator:
    def __init__(self, config, psm_model, tests_path):
        """
        Initializes the frontend test generator.

        Args:
            config (ProjectConfiguration): The project configuration.
            psm_model (PSMModel): The frontend platform-specific model.
            tests_path (str): The directory where the test files will be generated.
        """
        self._config = config
        self._psm_model = psm_model
        self._tests_path = tests_path
        self._templates_path = "pygen/generators/templates/frontend/react/tests"
        self._env = Environment(loader=FileSystemLoader(self._templates_path))

    def generate(self):
        """
        Generates unit test files for components and views.
        """
        os.makedirs(self._tests_path, exist_ok=True)

        for component in self._psm_model.components:
            self._generate_component_tests(component)
            self._generate_view_tests(component)

        self._generate_routing_tests()

    def _generate_component_tests(self, component):
        """
        Generates unit tests for the main components (Table, Form, Detail).

        Args:
            component (PSMComponent): The component for which tests will be generated.
        """
        for view in ["Table", "Form"]:
            template = self._env.get_template(f"{view.lower()}_test_template.jinja2")
            rendered = template.render(component=component.to_dict())
            file_path = os.path.join(self._tests_path, f"{component.name}{view}.test.js")
            with open(file_path, "w") as file:
                file.write(rendered)
            print(f"Test generated for {view} of component {component.name} at {file_path}")

    def _generate_view_tests(self, component):
        """
        Generates unit tests for the main view of a component.

        Args:
            component (PSMComponent): The component for which the view will be tested.
        """
        template = self._env.get_template("view_test_template.jinja2")
        rendered = template.render(component=component.to_dict())
        file_path = os.path.join(self._tests_path, f"{component.name}View.test.js")
        with open(file_path, "w") as file:
            file.write(rendered)
        print(f"Test generated for the view {component.name} at {file_path}")

    def _generate_routing_tests(self):
        """
        Generates tests for the main routes defined in `App.js`.
        """
        template = self._env.get_template("app_test_template.jinja2")
        rendered = template.render(components=[component.to_dict() for component in self._psm_model.components])
        file_path = os.path.join(self._tests_path, "..", "App.test.js")
        with open(file_path, "w") as file:
            file.write(rendered)
        print(f"Routing test generated at {file_path}")
