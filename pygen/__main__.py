import click

from pygen.project import Project
from yaml_interpreters import ModelYAMLInterpreter, ConfigurationYAMLInterpreter
from project_configuration import ProjectConfiguration


@click.command()
@click.version_option("0.1.0", prog_name="PyGen")
@click.option(
    "-c",
    "--config",
    nargs=1,
    type=click.File(mode="r"),
    help="Path to the configuration YAML file."
)
@click.argument(
    "model",
    nargs=1,
    type=click.File(mode="r"),
    help="Path to the model YAML file."
)
def main(model, config):
    """
    Main entry point for the PyGen CLI application.

    This function parses the provided model and configuration files, initializes
    a Project instance, and triggers the project generation process.

    Args:
        model (File): The YAML file containing the entity model definition.
        config (File, optional): The YAML file containing the project configuration. 
                                 If not provided, a configuration form will prompt the user.

    Example:
        pygen <model_file.yaml> -c <config_file.yaml>

    Raises:
        ConfigurationException: If the configuration file is invalid.
        ModelValidationException: If the model file is invalid.
    """
    # Parse the model file using ModelYAMLInterpreter
    model = ModelYAMLInterpreter().parse(model)

    # Parse the configuration file if provided; otherwise, prompt user for configuration
    if config is not None:
        config = ConfigurationYAMLInterpreter().parse(config)
    else:
        config = ProjectConfiguration()
        config.init_form()  # Prompts user for configuration settings

    # Display the project name to confirm project creation
    print(f"Creating application with name: {config.project_name}")

    # Initialize the Project with parsed model and configuration
    project = Project(model, config)

    # Trigger the project generation process
    project.generate_project()


if __name__ == "__main__":
    main()
