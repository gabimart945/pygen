import click


@click.command()
@click.version_option("0.1.0", prog_name="PyGen")
@click.option("-c", "--config", nargs=1, type=click.File(mode="r"))
@click.argument(
    "model",
    nargs=1,
    type=click.File(mode="r"),
)
def main(model, config):
    print(model.read().rstrip())
    print(config.read().rstrip())


if __name__ == "__main__":
    main()
