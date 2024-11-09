import sys
import os
import shutil
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../pygen')))

from click.testing import CliRunner
from pygen.__main__ import main


# Test to verify the CLI command correctly prints the content of the files
def test_cli_with_model_and_config_files(monkeypatch):
    runner = CliRunner()

    # Execute the command with the temporary files
    result = runner.invoke(main, ["tests/fixtures/valid_model.yaml", "-c", "tests/fixtures/valid_config.yaml"])

    # Check that the command executed successfully
    assert result.exit_code == 0

    shutil.rmtree("TestProject")


# Test to verify the version option
def test_cli_version():
    runner = CliRunner()
    result = runner.invoke(main, ["--version"])

    # Check that the command executed successfully
    assert result.exit_code == 0
    assert "PyGen, version 0.1.0" in result.output


# Test to verify the initialize command
def test_cli_initialize_project_with_form(monkeypatch):
    runner = CliRunner()
    # Execute the command with the temporary files

    # Mock user inputs
    inputs = iter(["TestProject", "1", "1", "1", "2", "1"])  # Mock inputs for project name and selections
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Run initialize command
    result = runner.invoke(main, ["tests/fixtures/valid_model.yaml"])

    # Check that the command executed successfully
    assert result.exit_code == 0
    assert "Project Configuration Complete:" in result.output
    assert "Project Name: TestProject" in result.output

    shutil.rmtree("TestProject")



# Test to verify the help message
def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])

    # Check that the command executed successfully
    assert result.exit_code == 0
    assert "Usage: main [OPTIONS] MODEL\n" in result.output  # Check for the presence of help text


# Test to verify handling of invalid command
def test_cli_invalid_command():
    runner = CliRunner()
    result = runner.invoke(main, ["invalid_command"])

    # Check that the command fails gracefully
    assert result.exit_code != 0
    assert "Usage: main [OPTIONS] MODEL\n" in result.output  # Adjust based on your error handling message