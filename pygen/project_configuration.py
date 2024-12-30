from pygen.sanitizers import sanitize_filename


class DbConfiguration(object):
    """
    Manages the database configuration for production and development environments.
    Provides accessors and mutators for both production and development databases.
    """

    def __init__(self, yaml_db=None):
        """
        Initializes DbConfiguration with YAML data, if provided.

        Args:
            yaml_db (dict, optional): YAML dictionary containing 'production'
                                      and optional 'development' database configurations.
        """
        if yaml_db is not None:
            self._production = yaml_db['production']
            self._development = yaml_db.get('development', None)
        else:
            self._production = None
            self._development = None

    @property
    def production(self):
        """
        Gets the production database configuration.

        Returns:
            str: Production database configuration.
        """
        return self._production

    @property
    def development(self):
        """
        Gets the development database configuration.

        Returns:
            str: Development database configuration.
        """
        return self._development

    def set_production(self, database):
        """
        Sets the production database configuration.

        Args:
            database (str): Production database name.
        """
        self._production = database

    def set_development(self, database):
        """
        Sets the development database configuration.

        Args:
            database (str): Development database name.
        """
        self._development = database


class BackendConfiguration(object):
    """
    Manages backend configuration, including framework and database configuration.
    Provides methods to validate and set backend framework and database.
    """

    def __init__(self, yaml_backend=None):
        """
        Initializes BackendConfiguration with YAML data, if provided.

        Args:
            yaml_backend (dict, optional): YAML dictionary containing 'framework'
                                           and 'database' configuration.
        """
        if yaml_backend is not None:
            self._architecture = yaml_backend["architecture"]
            self._framework = yaml_backend["framework"]
            self._database = DbConfiguration(yaml_backend["database"])
        else:
            self._framework = None
            self._database = DbConfiguration()

    @property
    def architecture(self):
        """
        Gets the backend architecture.

        Returns:
            str: Backend architecture type.
        """
        return self._architecture

    @property
    def framework(self):
        """
        Gets the backend framework.

        Returns:
            str: Backend framework name.
        """
        return self._framework

    @property
    def database(self):
        """
        Gets the database configuration.

        Returns:
            DbConfiguration: Database configuration object.
        """
        return self._database

    def set_architecture(self, architecture):
        """
        Sets the backend framework if supported.

        Args:
            framework (str): Backend framework name.

        Raises:
            ValueError: If the framework is unsupported.
        """
        if architecture in ["monolithic"]:
            self._architecture = architecture
        else:
            raise ValueError(f"Unsupported backend architecture: {architecture}")

    def set_framework(self, framework):
        """
        Sets the backend framework if supported.

        Args:
            framework (str): Backend framework name.

        Raises:
            ValueError: If the framework is unsupported.
        """
        if framework in ["flask"]:
            self._framework = framework
        else:
            raise ValueError(f"Unsupported backend framework: {framework}")

    def set_database(self, environment, database):
        """
        Sets the database configuration for the specified environment.

        Args:
            environment (str): Either 'production' or 'development'.
            database (str): Database name.

        Raises:
            ValueError: If the database or environment is unsupported.
        """
        if database in ["postgresql", "sqlite"]:
            if environment == "production":
                self._database.set_production(database)
            elif environment == "development":
                self._database.set_development(database)
            else:
                raise ValueError(f"Unsupported environment: {environment}")
        else:
            raise ValueError(f"Unsupported database: {database}")


class FrontendConfiguration(object):
    """
    Manages frontend configuration, including framework.
    Provides methods to validate and set frontend framework.
    """

    def __init__(self, yaml_frontend=None):
        """
        Initializes FrontendConfiguration with YAML data, if provided.

        Args:
            yaml_frontend (dict, optional): YAML dictionary containing 'framework'
        """
        if yaml_frontend is not None:
            self._framework = yaml_frontend["framework"]
        else:
            self._framework = None

    @property
    def framework(self):
        """
        Gets the frontend framework.

        Returns:
            str: Frontend framework name.
        """
        return self._framework

    def set_framework(self, framework):
        """
        Sets the frontend framework if supported.

        Args:
            framework (str): Backend framework name.

        Raises:
            ValueError: If the framework is unsupported.
        """
        if framework in ["react"]:
            self._framework = framework
        else:
            raise ValueError(f"Unsupported frontend framework: {framework}")


class ProjectConfiguration(object):
    """
    Manages the overall project configuration, including project name, backend and frontend configuration.
    Provides methods to initialize project settings.
    """

    def __init__(self, yaml_configuration=None):
        """
        Initializes ProjectConfiguration with YAML data, if provided.

        Args:
            yaml_configuration (dict, optional): YAML dictionary containing 'project_name'
                                                 ,'backend' and 'frontend' configuration.
        """
        if yaml_configuration is not None:
            self._project_name = yaml_configuration["project_name"]
            self._auth = yaml_configuration.get("auth", None)
            self._backend = BackendConfiguration(yaml_configuration["backend"])
            self._frontend = FrontendConfiguration(yaml_configuration["frontend"])
            self._cicd = yaml_configuration.get("cicd", None)

        else:
            self._project_name = None
            self._auth = None
            self._backend = BackendConfiguration()
            self._frontend = FrontendConfiguration()
            self._cicd = None

    @property
    def project_name(self):
        """
        Gets the project name.

        Returns:
            str: Project name.
        """
        return self._project_name

    @property
    def auth(self):
        """
        Gets the authentication method.

        Returns:
            str: Authentication method.
        """
        return self._auth

    @property
    def backend(self):
        """
        Gets the backend configuration.

        Returns:
            BackendConfiguration: Backend configuration object.
        """
        return self._backend

    @property
    def frontend(self):
        """
        Gets the frontend configuration.

        Returns:
            BackendConfiguration: Backend configuration object.
        """
        return self._frontend

    @property
    def cicd(self):
        """
        Gets the ci/cd platform.

        Returns:
            str: The ci/cd platform.
        """
        return self._cicd

    def set_cicd(self, cicd):
        """
        Sets the ci/cd platform after sanitizing it.

        Args:
            cicd (str): The ci/cd platform.

        Raises:
            ValueError: If the ci/cd platform is unsupported.
        """
        if cicd in ["azure", "github"]:
            self._cicd = cicd
        else:
            raise ValueError(f"Unsupported ci/cd platform: {cicd}")

    def set_project_name(self, project_name):
        """
        Sets the project name after sanitizing it.

        Args:
            project_name (str): The name of the project.
        """
        self._project_name = sanitize_filename(project_name)

    def set_auth(self, auth):
        """
        Sets the project name after sanitizing it.

        Args:
            auth (str or None): The authentication method.

        Raises:
            ValueError: If the authentication method is unsupported.
        """
        if auth is None or auth in ["basic"]:
            self._auth = auth
        else:
            raise ValueError(f"Unsupported authentication method: {auth}")

    @staticmethod
    def _get_option(options):
        """
        Displays a numbered list of options and prompts the user to select one.

        Args:
            options (list of str): A list of options to display to the user.

        Returns:
            str: The selected option from the list.

        Raises:
            ValueError: If the input is not a valid integer or is outside the valid range.

        Example:
            options = ["option1", "option2", "option3"]
            selected_option = _get_option(options)
        """
        while True:
            # Display each option with a corresponding number.
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")

            # Prompt the user to enter their choice as a number.
            try:
                choice = int(input("Enter the number of your choice: "))

                # Check if the choice is within the valid range.
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                print("Invalid option. Please try again.")

            except ValueError:
                # Handle cases where input is not an integer.
                print("Invalid input. Please enter a number corresponding to the options.")

    def init_form(self):
        """
        Initializes the project configuration through a user input form.
        Prompts the user for project name, backend framework, and production/development databases.
        """

        # Set project name
        project_name = input("Enter project name: ")
        self.set_project_name(project_name)

        # Select authentication method
        print("\nSelect authentication method:")
        auth = self._get_option(["none", "basic"])
        if auth == "none":
            self.set_auth(None)
        else:
            self.set_auth(auth)

        # Select backend architecture
        print("\nSelect backend architecture:")
        self._backend.set_architecture(self._get_option(["monolithic"]))

        # Select backend framework
        print("\nSelect backend framework:")
        self._backend.set_framework(self._get_option(["flask"]))

        # Select production database
        print("\nSelect production database:")
        self._backend.database.set_production(self._get_option(["postgresql", "sqlite"]))

        # Select development database
        print("\nSelect development database:")
        self._backend.database.set_development(self._get_option(["postgresql", "sqlite"]))

        # Select backend framework
        print("\nSelect frontend framework:")
        self._frontend.set_framework(self._get_option(["react"]))

        # Select ci/cd platform
        print("\nSelect ci/cd platform:")
        self.set_cicd(self._get_option(["azure", "github"]))

        # Summary of configuration
        print("\nProject Configuration Complete:")
        print(f"Project Name: {self.project_name}")
        print(f"Authentication method: {self.auth}")
        print(f"Backend Framework: {self.backend.framework}")
        print(f"Production Database: {self.backend.database.production}")
        print(f"Development Database: {self.backend.database.development}")
        print(f"Frontend Framework: {self.frontend.framework}")
