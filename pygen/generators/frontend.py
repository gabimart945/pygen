from abc import ABC, abstractmethod
import os
from jinja2 import Environment, FileSystemLoader

from pygen.models.cim import CimModel
from pygen.models.frontend_pim import PIMModel
from pygen.models.react_psm import PSMModel


class FrontendGenerator(ABC):
    """
    Abstract base class for generating frontend applications from a CIM model.
    """
    def __init__(self, cim_model, config, path):
        """
        Initializes the frontend generator with a CIM model.

        Args:
            cim_model (CimModel): The conceptual independent model.
        """
        self._config = config
        self._cim_model = cim_model
        self._pim_model = None  # Will be populated after the CIM to PIM transformation
        self._transform_cim_to_pim()
        self._path = path

    def _transform_cim_to_pim(self):
        """
        Transforms the CIM model into a PIM model structured for frontend generation.
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

            # Add relationships to configure nested tables, dropdowns, or many-to-many components
            for relationship in self._cim_model.relationships:
                if relationship.source == cim_entity.name:
                    if relationship.type == "composition":
                        # Handle one-to-many relationships as nested tables
                        pim_entity.add_relationship(relationship.target, "table")
                    elif relationship.type == "aggregation":
                        # Handle many-to-one relationships as dropdowns
                        pim_entity.add_relationship(relationship.target, "dropdown")

    @abstractmethod
    def transform_pim_to_psm(self):
        """
        Abstract method to transform the PIM model into a PSM model specific to a frontend framework.
        """
        raise NotImplementedError

    @abstractmethod
    def generate_frontend(self):
        """
        Abstract method to generate the frontend application using Jinja2 templates.

        Args:
            output_path (str): The directory path where the frontend files will be generated.
        """
        raise NotImplementedError


class ReactFrontendGenerator(FrontendGenerator):
    """
    Concrete implementation of FrontendGenerator for generating React applications.
    """
    def __init__(self,  cim_model, config, path):
        """
        Initializes the React frontend generator.

        Args:
            cim_model (CimModel): The conceptual independent model.
        """
        super().__init__( cim_model, config, path)
        self._psm_model = None  # Will store the React-specific components
        self._transform_pim_to_psm()

    def _transform_pim_to_psm(self):
        """
        Transforms the PIM model into a PSM model specific to React.
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

    def _map_type_to_react(self, pim_type: str) -> str:
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

    def _map_relationship_to_react(self, relationship_type: str) -> str:
        """
        Maps PIM relationship types to React components.

        Args:
            relationship_type (str): The relationship type in PIM.

        Returns:
            str: React-compatible component type.
        """
        relationship_mapping = {
            "table": "nestedTable",
            "dropdown": "selectDropdown",
            "multi-select": "multiSelect"
        }
        return relationship_mapping.get(relationship_type, "nestedTable")

    def generate_frontend(self):
        self._generate_app()
        self._generate_components()
        self._generate_views()
        self._generate_routes()

    def _generate_components(self):
        """
        Generates the React frontend application using Jinja2 templates.

        Args:
            output_path (str): The directory path where the frontend files will be generated.
        """


        # Ensure output directory exists
        os.makedirs(self._path, exist_ok=True)

        # Initialize Jinja2 environment
        env = Environment(loader=FileSystemLoader("path_to_templates"))

        # Generate components for each entity
        for component in self._psm_model.components:
            template = env.get_template("react_component_template.jinja2")
            output = template.render(component=component.to_dict())
            with open(os.path.join(self._path, f"{component.name}Component.jsx"), "w") as file:
                file.write(output)

        print(f"React frontend generated at {self._path}")
