import click

from pygen.project import Project
from pygen.exceptions import ConfigurationException, ModelValidationException
from pygen.yaml_interpreters import ModelYAMLInterpreter, ConfigurationYAMLInterpreter
from pygen.project_configuration import ProjectConfiguration


@click.command()
@click.version_option("0.1.0", prog_name="PyGen")
@click.option(
    "-c",
    "--config",
    nargs=1,
    type=click.File(mode="r"),
    help="Specify the path to the configuration YAML file."
)
@click.argument(
    "model",
    nargs=1,
    type=click.File(mode="r"),
    help="Specify the path to the model YAML file."
)
def main(model, config):
    """
    Entry point for the PyGen CLI tool.

    This function parses the provided model and configuration YAML files and
    initializes the project generation process. If the configuration file is
    not provided, it prompts the user for the required settings.

    Args:
        model (File): The model YAML file defining entities and relationships.
        config (File): The configuration YAML file (optional).
    """
    try:
        # Parse the model file using ModelYAMLInterpreter
        model = ModelYAMLInterpreter().parse(model)

        # Parse the configuration file if provided; otherwise, prompt user for configuration
        if config is not None:
            config = ConfigurationYAMLInterpreter().parse(config)
        else:
            config = ProjectConfiguration()
            config.init_form()  # Prompts user for configuration settings

        # Generate the project using the parsed model and configuration
        create_project(model, config)
    except ConfigurationException as ex:
        # Handle errors related to invalid configuration
        print(ex.message)
    except ModelValidationException as ex:
        # Handle errors related to invalid model definition
        print(ex.message)


def create_project(model, config):
    """
    Creates the project based on the provided model and configuration.

    This function initializes the Project class and triggers the generation
    of the application's file structure, backend, and frontend.

    Args:
        model (EntityModel): The parsed model representing entities and relationships.
        config (ProjectConfiguration): The configuration for the project settings.
    """
    # Display the project name to confirm project creation
    print(f"Creating application with name: {config.project_name}")

    # Initialize the Project with the parsed model and configuration
    project = Project(model, config)

    # Trigger the project generation process
    project.generate_project()


if __name__ == "__main__":
    main()
