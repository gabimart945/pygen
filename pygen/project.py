import os
import subprocess
import sys
from pygen.generators.backend import MonolithicBackendGenerator
from pygen.generators.frontend import ReactFrontendGenerator


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
        if self._config.frontend.framework == "react":
            self._frontend_generator = ReactFrontendGenerator(self._config, self._model, self._paths["frontend"])


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

        # Generate frontend app
        self._generate_frontend()

        # Install dependencies
        self._install_dependencies()

    def _generate_file_structure(self):
        os.mkdir(self._root_folder)
        os.mkdir(self._paths["backend"])
        os.mkdir(self._paths["frontend"])

    def _generate_backend(self):
        self._backend_generator.generate()

    def _generate_frontend(self):
        self._frontend_generator.generate()

    def _install_dependencies(self):
        """
           Navigates to different directories and installs dependencies with pip and npm.

           Args:
               path_python (str): Path where Python dependencies will be installed
               path_node (str): Path where Node.js dependencies will be installed

           Returns:
               bool: True if the entire process was successful, False otherwise
           """
        # Save the current working directory
        original_directory = os.getcwd()
        # Generate full paths using class variables

        print(f"Original working directory: {original_directory}")

        try:
            # Step 1: Navigate to Python path
            print(f"\n1. Navigating to: {self._paths["backend"]}")
            os.chdir(self._paths["backend"])
            print(f"Current directory: {os.getcwd()}")

            # Step 2: Install dependencies with pip
            print("\n2. Installing dependencies with pip...")
            if os.path.exists('requirements.txt'):
                pip_result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                                            capture_output=True, text=True)
                print(pip_result.stdout)
                if pip_result.returncode != 0:
                    print(f"Error installing dependencies with pip: {pip_result.stderr}")
                    return False
            else:
                print("requirements.txt file not found")

            # Step 3: Navigate back to the original directory
            print(f"\n3. Returning to original directory: {original_directory}")
            os.chdir(original_directory)
            print(f"Current directory: {os.getcwd()}")

            # Step 4: Navigate to Node.js path
            print(f"\n4. Navigating to: {self._paths["frontend"]}")
            os.chdir(self._paths["frontend"])
            print(f"Current directory: {os.getcwd()}")

            # Step 5: Install dependencies with npm
            print("\n5. Installing dependencies with npm...")
            if os.path.exists('package.json'):
                # Try multiple ways to run npm to handle path issues
                try:
                    # Try with full path on Windows
                    if os.name == 'nt':  # Windows
                        npm_paths = [
                            r'C:\Program Files\nodejs\npm.cmd',
                            r'C:\Program Files (x86)\nodejs\npm.cmd',
                            os.path.join(os.environ.get('APPDATA', ''), 'npm', 'npm.cmd'),
                            os.path.join(os.environ.get('ProgramFiles', ''), 'nodejs', 'npm.cmd')
                        ]

                        for npm_path in npm_paths:
                            if os.path.exists(npm_path):
                                print(f"Found npm at: {npm_path}")
                                npm_result = subprocess.run([npm_path, 'install'],
                                                            capture_output=True, text=True)
                                break
                        else:
                            # If no specific path works, try with shell=True
                            print("Using shell=True to find npm")
                            npm_result = subprocess.run('npm install',
                                                        shell=True, capture_output=True, text=True)
                    else:  # Non-Windows systems
                        npm_result = subprocess.run(['npm', 'install'],
                                                    capture_output=True, text=True)
                except Exception as e:
                    print(f"Error attempting to run npm: {str(e)}")
                    return False
                print(npm_result.stdout)
                if npm_result.returncode != 0:
                    print(f"Error installing dependencies with npm: {npm_result.stderr}")
                    return False
            else:
                print("package.json file not found")

            print("\nProcess completed successfully!")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return False

        finally:
            # Make sure to return to the original directory when finished
            os.chdir(original_directory)
            print(f"Finished. Current directory: {os.getcwd()}")
