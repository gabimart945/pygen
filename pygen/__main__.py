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
    type=click.File(mode="r")
)
@click.argument(
    "model",
    nargs=1,
    type=click.File(mode="r")
)
def main(model, config):

    try:
        # Parse the model file using ModelYAMLInterpreter
        model = ModelYAMLInterpreter().parse(model)
        # Parse the configuration file if provided; otherwise, prompt user for configuration
        if config is not None:
            config = ConfigurationYAMLInterpreter().parse(config)
        else:
            config = ProjectConfiguration()
            config.init_form()  # Prompts user for configuration settings
        create_project(model, config)
    except ConfigurationException as ex:
        print(ex.message)
    except ModelValidationException as ex:
        print(ex.message)


def create_project(model, config):
    # Display the project name to confirm project creation
    print(f"Creating application with name: {config.project_name}")
    # Initialize the Project with parsed model and configuration
    project = Project(model, config)
    # Trigger the project generation process
    project.generate_project()


if __name__ == "__main__":
    main()
