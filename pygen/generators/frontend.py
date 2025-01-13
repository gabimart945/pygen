from abc import ABC, abstractmethod
import os
from jinja2 import Environment, FileSystemLoader
import subprocess

from pygen.generators.frontend_test_generator import ReactTestGenerator
from pygen.models.cim import CimModel
from pygen.models.frontend_pim import PIMModel
from pygen.models.react_psm import PSMModel


class FrontendGenerator(ABC):
    """
    Abstract base class for generating frontend applications from a Computation Independent Model (CIM).

    Attributes:
        _config (object): Configuration object containing generation settings.
        _cim_model (CimModel): The CIM representing entities, attributes, and relationships.
        _pim_model (PIMModel): The Platform Independent Model generated from the CIM.
        _path (str): Path to the directory where the frontend will be generated.
    """
    def __init__(self, config, cim_model, path):
        """
        Initializes the frontend generator with a CIM model.

        Args:
            config (object): Configuration object for the frontend generator.
            cim_model (CimModel): The conceptual independent model.
            path (str): Path to the output directory for the generated frontend.
        """
        self._config = config
        self._cim_model = cim_model
        self._pim_model = None  # Will be populated after the CIM to PIM transformation
        self._transform_cim_to_pim()
        self._path = path

    def _transform_cim_to_pim(self):
        """
        Transforms the CIM model into a PIM model for frontend generation.

        Converts entity attributes and relationships into forms, views, and components
        suitable for frontend development.
        """
        self._pim_model = PIMModel()

        type_mapping_to_form = {
            "String": "text",
            "Integer": "number",
            "Date": "date",
            "Boolean": "checkbox",
        }

        for cim_entity in self._cim_model.entities:
            pim_entity = self._pim_model.add_entity(cim_entity.name)

            # Define base components: form, list, detail view
            for attribute in cim_entity.attributes:
                form_type = type_mapping_to_form.get(attribute.type, "text")
                pim_entity.add_attribute(attribute.name, form_type)

            # Add relationships to configure nested tables, dropdowns
            for relationship in self._cim_model.relationships:
                if relationship.source == cim_entity.name:
                    if relationship.type == "composition":
                        # Handle one-to-many relationships as nested tables
                        pim_entity.add_relationship(relationship.target, "nested_table")
                    elif relationship.type == "aggregation":
                        # Handle many-to-one relationships as dropdowns
                        pim_entity.add_relationship(relationship.target, "select_dropdown")

                # Ensure bidirectional relationships are added
                if relationship.target == cim_entity.name:
                    if relationship.type == "composition":
                        # Handle reverse of one-to-many as parent reference
                        pim_entity.add_relationship(relationship.source, "parent_reference")
                    elif relationship.type == "aggregation":
                        # Handle reverse of many-to-one as related item
                        pim_entity.add_relationship(relationship.source, "related_item")

    @abstractmethod
    def _transform_pim_to_psm(self):
        """
        Abstract method to transform the PIM model into a PSM model specific to a frontend framework.

        Must be implemented by subclasses to support framework-specific requirements.
        """
        raise NotImplementedError

    @abstractmethod
    def generate(self):
        """
        Abstract method to generate the frontend application.

        Must be implemented by subclasses to produce the final application using templates.
        """
        raise NotImplementedError


class ReactFrontendGenerator(FrontendGenerator, ABC):
    """
    Concrete implementation of FrontendGenerator for generating React applications.

    Attributes:
        _psm_model (PSMModel): The Platform Specific Model tailored for React components.
        _templates_path (str): Path to the directory containing React-specific Jinja2 templates.
        _test_generator (ReactTestGenerator): Generator for creating React component tests.
    """
    def __init__(self, config, cim_model, path):
        """
        Initializes the React frontend generator.

        Args:
            config (object): Configuration object for the React generator.
            cim_model (CimModel): The conceptual independent model.
            path (str): Path to the output directory for the React frontend.
        """
        super().__init__( config, cim_model, path)
        self._psm_model = None  # Will store the React-specific components
        self._transform_pim_to_psm()
        self._templates_path = "pygen/generators/templates/frontend/react"
        self._test_generator = ReactTestGenerator(config, self._psm_model, os.path.join(path, "src/tests"))

    def _transform_pim_to_psm(self):
        """
        Transforms the PIM model into a PSM model for React components.

        Maps attributes and relationships to React-compatible inputs and components.
        """
        self._psm_model = PSMModel()
        for entity in self._pim_model.entities:
            component = self._psm_model.add_component(entity.name)

            # Add fields to the component
            for attr in entity.attributes:
                component.add_field(attr.name, self._map_type_to_react(attr.type))

            # Add relationships to the component
            for rel in entity.relationships:
                component.add_relationship(rel.target, self._map_relationship_to_react(rel.type))

            # Enable specific views
            component.list_component = True
            component.form_component = True
            component.detail_component = True

    def _map_type_to_react(self, pim_type):
        """
        Maps PIM field types to React-compatible input types.

        Args:
            pim_type (str): The PIM field type.

        Returns:
            str: React-compatible input type.
        """
        type_mapping = {
            "text": "text",
            "number": "number",
            "date": "date",
            "checkbox": "checkbox",
        }
        return type_mapping.get(pim_type, "text")


    def _map_relationship_to_react(self, relationship_type):
        """
        Maps PIM relationship types to React components.

        Args:
            relationship_type (str): The relationship type in PIM.

        Returns:
            str: React-compatible component type.
        """
        relationship_mapping = {
            "nested_table": "NestedTableComponent",
            "select_dropdown": "SelectDropdownComponent",
            "parent_reference": "ParentReferenceComponent",
            "related_item": "RelatedItemComponent",
        }
        return relationship_mapping.get(relationship_type, "DefaultRelationshipComponent")

    def generate(self):
        """
        Generates the React frontend application.

        This includes generating the app structure, components, views, and test files.
        """
        self._generate_app()
        self._generate_components()
        self._generate_views()
        self._test_generator.generate()

    def _generate_components(self):
        """
        Generates React components using Jinja2 templates.

        Creates component files for forms and tables based on the React PSM model.
        """
        # Ensure the src/components directory exists
        components_path = os.path.join(self._path, "src", "components")
        os.makedirs(components_path, exist_ok=True)

        # Initialize Jinja2 environment
        env = Environment(loader=FileSystemLoader(self._templates_path))

        if self._config.auth == "jwt":
            protected_route_template = env.get_template("protected_route_template.jinja2")
            with open(os.path.join(self._path, "src", "components", "ProtectedRoute.jsx"), "w") as file:
                file.write(protected_route_template.render())

        # Generate components for each entity
        for component in self._psm_model.components:
            for view in ["Table", "Form"]:
                try:
                    # Load the template for React components
                    template = env.get_template(f"{view.lower()}_template.jinja2")

                    # Render the template with the current component and view
                    output = template.render(component=component.to_dict(), view=view)

                    # Write the output to a JSX file
                    file_path = os.path.join(components_path, f"{component.name}{view}.jsx")
                    with open(file_path, "w") as file:
                        file.write(output)

                    print(f"Generated {view} component for {component.name} at {file_path}")
                except Exception as e:
                    print(f"Error generating {view} component for {component.name}: {e}")

        print(f"React components generated at {components_path}")

    def _generate_app(self):
        """
        Generates the main React application files.

        Includes the App.js, index.js, and related configuration files for the React application.
        """
        try:
            # Attempt to create the React app using react-scripts
            subprocess.run(["npx", "create-react-app", self._path], check=True)
        except FileNotFoundError:
            print("create-react-app not found. Creating the project structure manually.")
            self._create_project_structure()
        except subprocess.CalledProcessError:
            raise RuntimeError(
                "create-react-app failed to execute. Please ensure npm and create-react-app are installed.")

        # Initialize Jinja2 environment
        env = Environment(loader=FileSystemLoader(self._templates_path))

        # Generate .env file for API configuration
        env_file_path = os.path.join(self._path, ".env")
        with open(env_file_path, "w") as env_file:
            env_file.write("REACT_APP_API_HOST=http://127.0.0.1\n")
            env_file.write("REACT_APP_API_PORT=5000\n")

        print(f".env file created at {env_file_path}")

        # Generate api.js
        api_template = env.get_template("api_template.jinja2")
        with open(os.path.join(self._path, "src", "api.js"), "w") as file:
            file.write(api_template.render(config=self._config))
        print(f"Api.js file created at {os.path.join(self._path, "src", "Api.js")}")

        # Generate App.js file
        template = env.get_template("app_template.jinja2")
        output = template.render(components=self._psm_model.components, config=self._config)
        with open(os.path.join(self._path, "src", "App.js"), "w") as file:
            file.write(output)
        print(f"App.js file created at {os.path.join(self._path, "src", "App.js")}")

        # Generate index.css file
        css_template = env.get_template("app_css_template.jinja2")
        css_output = css_template.render()
        with open(os.path.join(self._path, "src", "app.css"), "w") as file:
            file.write(css_output)

        print(f"React frontend project created at {self._path}")

    def _create_project_structure(self):
        """
        Manually creates the folder structure for the React project.
        """
        folders = [
            "src",
            "src/components",
            "src/views",
            "public",
        ]

        for folder in folders:
            os.makedirs(os.path.join(self._path, folder), exist_ok=True)

        # Create package.json
        package_json_content = {
              "name": "react-frontend",
              "version": "0.1.0",
              "private": True,
              "dependencies": {
                "axios": "^1.5.0",
                "bootstrap": "^5.3.1",
                "react": "^18.2.0",
                "react-bootstrap": "^2.8.0",
                "react-dom": "^18.2.0",
                "react-router-dom": "^6.14.0",
                "react-scripts": "5.0.1"
              },
              "devDependencies": {
                "@babel/core": "^7.26.0",
                "@babel/preset-env": "^7.26.0",
                "@babel/preset-react": "^7.26.3",
                "@testing-library/jest-dom": "^6.0.0",
                "@testing-library/react": "^14.1.0",
                "@testing-library/user-event": "^14.5.0",
                "babel-jest": "^29.7.0",
                "eslint": "^8.57.1",
                "jest": "^29.7.0",
                "jest-environment-jsdom": "^29.7.0",
                "rimraf": "^4.0.0"
              },
              "scripts": {
                "start": "react-scripts start",
                "build": "react-scripts build",
                "test": "react-scripts test",
                "test:coverage": "react-scripts test -- --coverage",
                "eject": "react-scripts eject"
              },
              "browserslist": {
                "production": [
                  ">0.2%",
                  "not dead",
                  "not op_mini all"
                ],
                "development": [
                  "last 1 chrome version",
                  "last 1 firefox version",
                  "last 1 safari version"
                ]
              }
            }


        with open(os.path.join(self._path, "package.json"), "w") as file:
            import json
            file.write(json.dumps(package_json_content, indent=2))

        # Create jest.config.js
        jest_content = """
        module.exports = {
          testEnvironment: 'jsdom',
          moduleNameMapper: {
            '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
          },
          setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
        };
        """
        with open(os.path.join(self._path, "jest.config.js"), "w") as file:
            file.write(jest_content)

        # Create setupTests.js
        setup_content = """
        import '@testing-library/jest-dom';
        """
        with open(os.path.join(self._path, "src", "setupTests.js"), "w") as file:
            file.write(setup_content)

        # Create a basic index.html
        index_html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>React Frontend</title>
        </head>
        <body>
            <div id="root"></div>
        </body>
        </html>
        """
        with open(os.path.join(self._path, "public", "index.html"), "w") as file:
            file.write(index_html_content)



        # Create a basic index.js
        index_js_content = """
        import React from 'react';
        import { createRoot } from 'react-dom/client';
        import App from './App';
        import 'bootstrap/dist/css/bootstrap.min.css';
        import './app.css';

        
        // Create the root element
        const container = document.getElementById('root');
        const root = createRoot(container);
        
        // Render the application
        root.render(
            <React.StrictMode>
                <App />
            </React.StrictMode>
        );

        """
        with open(os.path.join(self._path, "src", "index.js"), "w") as file:
            file.write(index_js_content)

        print(f"Manual React project structure created at {self._path}")

    def _generate_views(self):
        """
        Generates views for the React application using Jinja2 templates.

        Each view corresponds to a component in the PSM model.
        """
        views_path = os.path.join(self._path, "src", "views")
        os.makedirs(views_path, exist_ok=True)

        # Initialize Jinja2 environment
        env = Environment(loader=FileSystemLoader(self._templates_path))

        # Generate login view if JWT authentication is enabled
        if self._config.auth == "jwt":
            login_template = env.get_template("login_template.jinja2")
            with open(os.path.join(self._path, "src", "views", "LoginView.jsx"), "w") as file:
                file.write(login_template.render(config=self._config))

        # Generate views for each entity
        for component in self._psm_model.components:
            try:
                # Load the template for React views
                template = env.get_template("view_template.jinja2")

                # Render the template with the current component
                output = template.render(component=component.to_dict())

                # Write the output to a JSX file
                file_path = os.path.join(views_path, f"{component.name}View.jsx")
                with open(file_path, "w") as file:
                    file.write(output)

                print(f"Generated view for {component.name} at {file_path}")
            except Exception as e:
                print(f"Error generating view for {component.name}: {e}")
