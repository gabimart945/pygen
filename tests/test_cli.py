import pytest
from click.testing import CliRunner
from pygen.__main__ import main  # Import the cli function from your module


# Test to verify the cli command correctly prints the content of the files
def test_cli(monkeypatch):
    runner = CliRunner()

    # Create temporary files with test content
    model_content = "model content"
    config_content = "config content"

    with runner.isolated_filesystem():
        # Create temporary files
        with open("test_model.txt", "w") as model_file:
            model_file.write(model_content)
        with open("test_config.txt", "w") as config_file:
            config_file.write(config_content)

        # Execute the command with the temporary files
        result = runner.invoke(main, ["test_model.txt", "-c", "test_config.txt"])

        # Check that the command executed successfully
        assert result.exit_code == 0

        # Check the output
        assert model_content in result.output
        assert config_content in result.output


# Test to verify the version option
def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])

    # Check that the command executed successfully
    assert result.exit_code == 0
    assert "PyGen, version 0.1.0" in result.output
