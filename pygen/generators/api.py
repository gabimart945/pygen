from abc import ABC, abstractmethod
from jinja2 import Environment, FileSystemLoader
import os

from pygen.generators.backend_test_generator import FlaskTestGenerator, SecurityTestGenerator, \
    IntegrationTestGenerator
from pygen.generators.dockerfile_generator import BackendDockerfileGenerator
from pygen.generators.pipeline_generator import AzureDevOpsPipelineGenerator, GithubActionsPipelineGenerator
from pygen.models.flask_psm import PsmModel, Entity


class IBackendApiGenerator(ABC):
    """
    Abstract base class for backend API generators. This class defines the interface
    and required methods for generating various components of a backend API.

    Attributes:
        _config (object): Configuration object containing generation settings.
        _psm_model (PsmModel): The transformed Platform-Specific Model (PSM) for the backend API.
    """

    def __init__(self, config):
        """
        Initializes the API generator with a given configuration.

        Args:
            config (object): The configuration object for the API generation process.
        """
        self._config = config
        self._psm_model = None
        if self._config.cicd == 'azure':
            self._pipeline_generator = AzureDevOpsPipelineGenerator()
        elif self._config.cicd == 'github':
            self._pipeline_generator = GithubActionsPipelineGenerator()
        else:
            self._pipeline_generator = None


    def generate(self, model, root_path, port=5000):
        """
        Generates the backend API by transforming the model and generating necessary files.

        Args:
            model (object): The input Platform-Independent Model (PIM).
            root_path (str): The root directory where the project will be generated.
            port (int): The port number for the service. Default is 5000.
        """
        self._transform_model(model)
        os.environ['SERVICE_PORT'] = str(port)
        self._generate_project_files(root_path)
        self._generate_app(root_path + '/app', port)
        self._generate_controllers(root_path + '/app/controllers')
        self._generate_services(root_path + '/app/services')
        self._generate_models(root_path + '/app/models')
        self._generate_schemas(root_path + '/app/schemas')
        self._generate_tests(root_path + '/tests')
        config = {
            "base_image": "python:3.9-slim",
            "port": port
        }
        generator = BackendDockerfileGenerator(root_path, config)
        generator.generate()
        if self._pipeline_generator:
            self._pipeline_generator.generate_backend_pipeline(os.path.join(root_path,"backend-ci-pipeline.yml"))

        # Si la autenticación es JWT, generamos los archivos adicionales
        if self._config.auth == "jwt":
            self._generate_authentication_files(root_path)

    @abstractmethod
    def _generate_project_files(self, root_path):
        """
        Abstract method to generate the base project structure and configuration files.

        Args:
            root_path (str): The root directory where the project will be generated.
        """
        raise NotImplementedError

    @abstractmethod
    def _generate_app(self, path, port):
        """
        Abstract method to generate the `__init__.py` file for the Flask application.

        Args:
            path (str): Path to the app directory.
            port (int): The port number for the Flask application.
        """
        raise NotImplementedError

    @abstractmethod
    def _generate_controllers(self, path):
        """
        Abstract method to generate controller files for the backend API.

        Args:
            path (str): Path to the controllers directory.
        """
        raise NotImplementedError

    @abstractmethod
    def _generate_services(self, path):
        """
        Abstract method to generate service files for the backend API.

        Args:
            path (str): Path to the services directory.
        """
        raise NotImplementedError

    @abstractmethod
    def _generate_models(self, path):
        """
        Abstract method to generate model files for the backend API.

        Args:
            path (str): Path to the models directory.
        """
        raise NotImplementedError

    @abstractmethod
    def _generate_schemas(self, path):
        """
        Abstract method to generate schema files for the backend API.

        Args:
            path (str): Path to the schemas directory.
        """
        raise NotImplementedError

    @abstractmethod
    def _transform_model(self, model):
        """
        Abstract method to transform the Platform-Independent Model (PIM)
        into a Platform-Specific Model (PSM).

        Args:
            model (object): The input PIM to transform.
        """
        raise NotImplementedError

    @abstractmethod
    def _generate_tests(self, path):
        """
        Abstract method to generate unit, integration, and security tests.

        Args:
            path (str): Path to the tests directory.
        """
        raise NotImplementedError

    @abstractmethod
    def _generate_authentication_files(self, path):
        """
        Abstract method to generate authentication-related files.

        Args:
            path (str): Path to the root project directory.
        """
        raise NotImplementedError


class FlaskApiGenerator(IBackendApiGenerator):
    """
    Concrete implementation of IBackendApiGenerator for Flask-based APIs.
    This class provides methods for generating Flask-specific project files,
    application components, and tests.

    Attributes:
        _templates_path (str): Path to the directory containing Jinja2 templates.
    """

    def __init__(self, config):
        """
        Initializes the Flask API generator with a given configuration.

        Args:
            config (object): The configuration object for the Flask API generation process.
        """
        super().__init__(config)
        # Obtener la ruta dentro del paquete
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self._templates_path = template_dir + "/backend/flask"

    def _generate_project_files(self, root_path):
        """
        Generates the base project structure, a `run.py` file, a `requirements.txt` file,
        and a `config.py` file.

        Args:
            root_path (str): The root directory where the project will be generated.
        """
        # Setup Jinja2 environment
        env = Environment(loader=FileSystemLoader(self._templates_path))

        # Create the `app` directory inside the project
        app_path = os.path.join(root_path, "app")
        os.makedirs(app_path, exist_ok=True)

        # Generate `run.py` using a template
        template = env.get_template('run_template.jinja2')
        run_py_content = template.render()
        run_py_path = os.path.join(root_path, "run.py")

        with open(run_py_path, "w") as run_file:
            run_file.write(run_py_content)

        print(f"`run.py` generated at {run_py_path}")

        # Generate `requirements.txt`
        requirements = [
            "Flask",
            "Flask-Migrate",
            "Flask-SQLAlchemy",
            "marshmallow",
            "flask-cors",
            "pytest",
            "requests",
            "pynt",
            "Flask-JWT-Extended",
            "cryptography",
        ]

        requirements_path = os.path.join(root_path, "requirements.txt")
        with open(requirements_path, "w") as req_file:
            req_file.write("\n".join(requirements))

        print(f"`requirements.txt` generated at {requirements_path}")

        # Generate `config.py`
        config_template = env.get_template('config_template.jinja2')
        context = {
            "config": self._config
        }
        config_content = config_template.render(context)
        config_path = os.path.join(root_path, "config.py")

        with open(config_path, "w") as config_file:
            config_file.write(config_content)

        print(f"`config.py` generated at {config_path}")

        print(f"Project structure created at {root_path}")


    def _generate_app(self, path, port):
        """
        Generates the `__init__.py` file for the Flask application.
        """
        # Set up Jinja2 environment
        env = Environment(loader=FileSystemLoader(self._templates_path))
        template = env.get_template('app_template.jinja2')

        # Extract entities from the PSM model
        entities = self._psm_model.entities

        # Context for rendering the template
        context = {
            "entities": entities,
            "config": self._config,
        }

        # Render the template
        rendered_code = template.render(context)

        # Output path
        init_file = os.path.join(path, "__init__.py")

        # Write the generated file
        with open(init_file, "w") as output_file:
            output_file.write(rendered_code)

        print(f"`__init__.py` has been generated at {init_file}")

    def _generate_controllers(self, path):
        """
        Generates Flask controllers for each entity using their respective services.

        Args:
            path (str): The path to the `app` directory.
        """
        # Setup Jinja2 environment
        env = Environment(loader=FileSystemLoader(self._templates_path))

        # Path to the controllers directory
        os.makedirs(path, exist_ok=True)

        # Generate a controller file for each entity
        for entity in self._psm_model.entities:
            # Render the controller template
            template = env.get_template('controller_template.jinja2')
            context = {
                "entity": entity,
                "config": self._config
            }
            rendered_code = template.render(context)

            # Write the controller to a file
            controller_file_path = os.path.join(path, f"{entity.name.lower()}_controller.py")
            with open(controller_file_path, "w") as controller_file:
                controller_file.write(rendered_code)

            print(f"Controller generated for {entity.name} at {controller_file_path}")

    def _generate_services(self, path):
        """
        Generates services for each entity, including logic to handle relationships.

        Args:
            path (str): The path to the `app` directory.
        """
        # Setup Jinja2 environment
        env = Environment(loader=FileSystemLoader(self._templates_path))

        # Path to the services directory
        os.makedirs(path, exist_ok=True)

        # Generate a service file for each entity
        for entity in self._psm_model.entities:
            # Render the service template
            template = env.get_template('service_template.jinja2')
            context = {
                "entity": entity,
                "config": self._config.backend
            }
            rendered_code = template.render(context)

            # Write the service to a file
            service_file_path = os.path.join(path, f"{entity.name.lower()}_service.py")
            with open(service_file_path, "w") as service_file:
                service_file.write(rendered_code)

            print(f"Service generated for {entity.name} at {service_file_path}")

    def _generate_models(self, path):
        """
        Generates SQLAlchemy models for each entity and a `__init__.py` file in the `models` directory.

        Args:
            path (str): The path to the `app` directory.
        """
        # Setup Jinja2 environment
        env = Environment(loader=FileSystemLoader(self._templates_path))

        # Path to the models directory
        os.makedirs(path, exist_ok=True)

        # Generate `__init__.py` for models
        init_template = env.get_template('models_init_template.jinja2')
        init_context = {"entities": self._psm_model.entities, "config": self._config}
        init_rendered = init_template.render(init_context)
        init_file_path = os.path.join(path, "__init__.py")
        with open(init_file_path, "w") as init_file:
            init_file.write(init_rendered)
        print(f"`__init__.py` generated at {init_file_path}")

        # Generate a model file for each entity
        model_template = env.get_template('model_template.jinja2')

        for entity in self._psm_model.entities:
            model_context = {"entity": entity}
            model_rendered = model_template.render(model_context)

            model_file_path = os.path.join(path, f"{entity.name.lower()}.py")
            with open(model_file_path, "w") as model_file:
                model_file.write(model_rendered)
            print(f"Model generated for {entity.name} at {model_file_path}")

    def _generate_schemas(self, path):
        """
        Generates Marshmallow schemas for each entity and its related entities.
        Each schema is saved in a separate file.

        Args:
            path (str): The path to the `app` directory.
        """
        # Setup Jinja2 environment
        env = Environment(loader=FileSystemLoader(self._templates_path))

        # Path to the schemas directory
        os.makedirs(path, exist_ok=True)

        # Generate schemas for each entity
        for entity in self._psm_model.entities:
            # Generate the main schema for the entity
            self._generate_single_schema(env, path, entity)

            # If microservices, also generate schemas for related entities
            if self._config.backend.architecture == "microservices":
                for relationship in entity.relationships:
                    related_entity = next((e for e in self._psm_model.entities if e.name == relationship.target), None)
                    if related_entity:
                        self._generate_single_schema(env, path, related_entity)

    @staticmethod
    def _generate_single_schema(env, schemas_path, entity):
        """
        Generates a single schema for an entity.

        Args:
            env (Environment): The Jinja2 environment.
            schemas_path (str): Path to the schemas' directory.
            entity (Entity): The entity for which the schema is generated.
        """
        # Render the schema template
        template = env.get_template('schema_template.jinja2')
        context = {"entity": entity}
        rendered_code = template.render(context)

        # Write the schema to a file
        schema_file_path = os.path.join(schemas_path, f"{entity.name.lower()}_schema.py")
        with open(schema_file_path, "w") as schema_file:
            schema_file.write(rendered_code)

        print(f"Schema generated for {entity.name} at {schema_file_path}")

    def _transform_model(self, model):
        """
        Transforms the PIM model to a neutral PSM model compatible with Flask and SQLAlchemy.

        Args:
            model (PimModel): The PIM model to be transformed.

        Sets:
            self._psm_model (PsmModel): The transformed PSM model.
        """
        psm_model = PsmModel()  # Create a new PSM model
        relationship_map = {}

        # First pass: Build the relationship map for direct relationships
        for pim_entity in model.entities:
            for pim_relationship in pim_entity.relationships:
                # Determine the name of the relationship (singular or plural)
                if pim_relationship.type in ["one-to-many", "many-to-many"]:
                    relationship_name = pim_relationship.name + "s"  # Plural for these types
                else:
                    relationship_name = pim_relationship.name  # Singular for others

                # Add the relationship to the map
                relationship_map[(pim_entity.name, pim_relationship.target)] = {
                    "name": relationship_name,
                    "type": pim_relationship.type,
                }

        # Second pass: Create PSM entities and assign relationships
        for pim_entity in model.entities:
            psm_entity = Entity(pim_entity.name, table_name=pim_entity.name.lower() + "s")

            # Add fields
            for pim_attribute in pim_entity.attributes:
                field_type = self._map_type_to_sqlalchemy(pim_attribute.type)
                psm_entity.add_field(
                    pim_attribute.name,
                    field_type,
                    primary_key=pim_attribute.primary_key,
                    nullable=pim_attribute.nullable,
                    foreign_key=pim_attribute.foreign_key
                )

            # Add relationships
            for pim_relationship in pim_entity.relationships:
                relationship_data = relationship_map[(pim_entity.name, pim_relationship.target)]
                reverse_relationship_data = relationship_map.get((pim_relationship.target, pim_entity.name))

                # Use reverse relationship name for back_populates
                back_populates = reverse_relationship_data["name"] if reverse_relationship_data else None

                # Add the relationship to the PSM entity
                psm_entity.add_relationship(
                    name=relationship_data["name"],
                    target=pim_relationship.target,
                    rel_type=pim_relationship.type,
                    back_populates=back_populates
                )

            # Add the PSM entity to the PSM model
            psm_model.add_entity(psm_entity)

        self._psm_model = psm_model  # Assign the transformed model to the class attribute

    @staticmethod
    def _map_type_to_sqlalchemy(pim_type):
        """
        Maps PIM attribute types to SQLAlchemy field types.

        Args:
            pim_type (str): The type of the attribute in the PIM model.

        Returns:
            str: The corresponding SQLAlchemy field type.
        """
        type_mapping = {
            "String": "db.String(255)",  # Default length for strings
            "Integer": "db.Integer",  # Integer types
            "Date": "db.Date",  # Date types
            "Boolean": "db.Boolean",  # Boolean types
            "Float": "db.Float",  # Floating-point types
            "Text": "db.Text",  # Larger text fields
            "DateTime": "db.DateTime",  # Date and time types
        }

        # Return the mapped type or a default (e.g., db.String(255) for unknown types)
        return type_mapping.get(pim_type, "db.String(255)")

    def _generate_tests(self, path):
        unit_test_generator = FlaskTestGenerator(self._config, self._psm_model, path + '/unit')
        unit_test_generator.generate()
        integration_test_generator = IntegrationTestGenerator(self._config, self._psm_model, path + '/integration')
        integration_test_generator.generate()
        security_test_generator = SecurityTestGenerator(self._config, self._psm_model, path + '/security')
        security_test_generator.generate()

    def _generate_authentication_files(self, root_path):
        """
        Generates necessary files for JWT authentication.
        """
        auth_templates_path = os.path.join(self._templates_path, "jwt_auth")
        env = Environment(loader=FileSystemLoader(auth_templates_path))

        # Create directories if they don't exist
        os.makedirs(os.path.join(root_path, "app/controllers"), exist_ok=True)
        os.makedirs(os.path.join(root_path, "app/services"), exist_ok=True)
        os.makedirs(os.path.join(root_path, "app/schemas"), exist_ok=True)
        os.makedirs(os.path.join(root_path, "app/models"), exist_ok=True)

        # Generate user model
        user_model_template = env.get_template("user_model_template.jinja2")
        with open(os.path.join(root_path, "app/models/user.py"), "w") as file:
            file.write(user_model_template.render())

        # Generate user schema
        user_schema_template = env.get_template("user_schema_template.jinja2")
        with open(os.path.join(root_path, "app/schemas/user_schema.py"), "w") as file:
            file.write(user_schema_template.render())

        # Generate auth service
        auth_service_template = env.get_template("auth_service_template.jinja2")
        with open(os.path.join(root_path, "app/services/auth_service.py"), "w") as file:
            file.write(auth_service_template.render())

        # Generate auth controller
        auth_controller_template = env.get_template("auth_controller_template.jinja2")
        with open(os.path.join(root_path, "app/controllers/auth_controller.py"), "w") as file:
            file.write(auth_controller_template.render())

        # Generate add_admin script
        auth_service_template = env.get_template("add_user_script_template.jinja2")
        with open(os.path.join(root_path, "add_admin.py"), "w") as file:
            file.write(auth_service_template.render())

        print("Authentication files generated successfully.")
