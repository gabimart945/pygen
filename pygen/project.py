import os
from generators import *
from pygen.generators.backend import MonolithicBackendGenerator


class Project(object):
    """
    Represents a project with a specified model and configuration.

    This class provides the main functionality to generate a project by creating
    the necessary file structure based on the provided model
    and configuration.

    Attributes:
        _model (EntityModel): The model defining entities and relationships.
        _config (ProjectConfiguration): The configuration for the project,
                                        including settings like backend and database.
    """

    def __init__(self, model, config):
        """
        Initializes the Project with a model and configuration.

        Args:
            model (EntityModel): The model representing the entities and their relationships.
            config (ProjectConfiguration): The configuration object for project settings.
        """
        self._model = model
        self._config = config
        self._paths = {}
        if self._config.project_name in os.listdir('.'):
            items = list(filter(lambda f: self._config.project_name in f, os.listdir('.')))
            self._root_folder = self._config.project_name + '_' + str(len(items))
        else:
            self._root_folder = self._config.project_name

        self._paths["backend"] = self._root_folder + '/backend'
        self._paths["frontend"] = self._root_folder + '/frontend'
        if self._config.backend.architecture == "monolithic":
            self._backend_generator = MonolithicBackendGenerator(self._config, self._model, self._paths["backend"])
        self._frontend_generator = None


    @property
    def root_folder(self):
        return self._root_folder

    def generate_project(self):
        """
        Generates the entire project by creating the file structure and backend setup.

        Calls helper methods to generate the required file structure and backend
        based on the project's model and configuration.

        Raises:
            NotImplementedError: If any helper methods are not implemented.
        """
        # Generate project directories and files according to configuration and model
        self._generate_file_structure()

        # Generate backend components (e.g., APIs) based on configuration and model
        self._generate_backend()

    def _generate_file_structure(self):
        os.mkdir(self._root_folder)
        os.mkdir(self._paths["backend"])
        os.mkdir(self._paths["frontend"])

    def _generate_backend(self):
        self._backend_generator.generate()



