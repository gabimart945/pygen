import click
from YamlInterpreters import ModelYAMLInterpreter, ConfigurationYAMLInterpreter
from ProjectConfiguration import ProjectConfiguration


@click.command()
@click.version_option("0.1.0", prog_name="PyGen")
@click.option("-c", "--config", nargs=1, type=click.File(mode="r"))
@click.argument(
    "model",
    nargs=1,
    type=click.File(mode="r"),
)
def main(model, config):
    model = ModelYAMLInterpreter().parse(model)
    if config is not None:
        config = ConfigurationYAMLInterpreter().parse(config)
    else:
        config = ProjectConfiguration()
        config.init_form()
    # TODO: Create Application
    print(f"Creating application with name: {config.project_name}")


if __name__ == "__main__":
    main()
