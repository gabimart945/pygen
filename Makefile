# Variables
VENV_DIR := .venv
PYTHON := $(VENV_DIR)/Scripts/python
PIP := $(VENV_DIR)/Scripts/pip
PYTEST := $(VENV_DIR)/Scripts/pytest
PROJECT_DIR := .
TEST_DIR := tests
REQUIREMENTS := requirements.txt

# Commands
.PHONY: all install test clean

# Install dependencies
install:
	$(PIP) install -r $(REQUIREMENTS)

# Run tests with pytest
test:
	PYTHONPATH=$(PROJECT_DIR) $(PYTEST) $(TEST_DIR)

# Clean up cache files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +

# Run all commands in sequence
all: clean install test
