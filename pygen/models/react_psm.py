import yaml


class ReactPsmField:
    """
    Represents a field in the PSM model for React.
    """
    def __init__(self, name: str, field_type: str):
        """
        Initializes a field in the PSM model.

        Args:
            name (str): The name of the field.
            field_type (str): The React-compatible type of the field.
        """
        self.name = name
        self.type = field_type

    def to_dict(self):
        """
        Converts the field to a dictionary.

        Returns:
            dict: Dictionary representation of the field.
        """
        return {
            "name": self.name,
            "type": self.type
        }

    def __repr__(self):
        return f"PSMField(name={self.name!r}, type={self.type!r})"


class ReactPsmRelationship:
    """
    Represents a relationship in the PSM model for React.
    """
    def __init__(self, target: str, relationship_type: str):
        """
        Initializes a relationship in the PSM model.

        Args:
            target (str): The target entity of the relationship.
            relationship_type (str): The React-compatible component type for the relationship.
        """
        self.target = target
        self.type = relationship_type

    def to_dict(self):
        """
        Converts the relationship to a dictionary.

        Returns:
            dict: Dictionary representation of the relationship.
        """
        return {
            "target": self.target,
            "type": self.type
        }

    def __repr__(self):
        return f"PSMRelationship(target={self.target!r}, type={self.type!r})"


class ReactPsmComponent:
    """
    Represents a React component in the PSM model.
    """
    def __init__(self, name: str):
        """
        Initializes a React component in the PSM model.

        Args:
            name (str): The name of the component.
        """
        self.name = name
        self.fields = []
        self.relationships = []
        self.list_component = False
        self.form_component = False
        self.detail_component = False

    def add_field(self, name: str, field_type: str):
        """
        Adds a field to the component.

        Args:
            name (str): The name of the field.
            field_type (str): The React-compatible type of the field.
        """
        self.fields.append(ReactPsmField(name, field_type))

    def add_relationship(self, target: str, relationship_type: str):
        """
        Adds a relationship to the component.

        Args:
            target (str): The target entity of the relationship.
            relationship_type (str): The React-compatible component type for the relationship.
        """
        self.relationships.append(ReactPsmRelationship(target, relationship_type))

    def to_dict(self):
        """
        Converts the component to a dictionary.

        Returns:
            dict: Dictionary representation of the component.
        """
        return {
            "name": self.name,
            "fields": [field.to_dict() for field in self.fields],
            "relationships": [rel.to_dict() for rel in self.relationships],
            "listComponent": self.list_component,
            "formComponent": self.form_component,
            "detailComponent": self.detail_component
        }

    def __repr__(self):
        return (f"PSMComponent(name={self.name!r}, fields={self.fields!r}, "
                f"relationships={self.relationships!r}, list_component={self.list_component}, "
                f"form_component={self.form_component}, detail_component={self.detail_component})")


class ReactPsmModel:
    """
    Represents the complete PSM model for React.
    """
    def __init__(self):
        """
        Initializes an empty PSM model.
        """
        self.components = []

    def add_component(self, name: str) -> ReactPsmComponent:
        """
        Adds a React component to the PSM model.

        Args:
            name (str): The name of the component.

        Returns:
            PSMComponent: The created component.
        """
        component = ReactPsmComponent(name)
        self.components.append(component)
        return component

    def to_dict(self):
        """
        Converts the entire model to a dictionary.

        Returns:
            dict: Dictionary representation of the model.
        """
        return {
            "components": [component.to_dict() for component in self.components]
        }

    def export_to_yaml(self, file_path: str):
        """
        Exports the PSM model to a YAML file.

        Args:
            file_path (str): The path to the output YAML file.
        """
        with open(file_path, "w") as file:
            yaml.dump(self.to_dict(), file, default_flow_style=False)

    def __repr__(self):
        """Returns a string representation of the PIM model."""
        return f"PSMModel(components={self.components!r})"
