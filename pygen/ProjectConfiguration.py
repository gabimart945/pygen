from Sanitizers import sanitize_filename


class DbConfiguration(object):
    def __init__(self, yaml_db=None):
        if yaml_db is not None:
            self._production = yaml_db['production']
            if yaml_db['development'] is not None:
                self._development = yaml_db['development']
            else:
                self._development = None
        else:
            self._production = None
            self._development = None

    @property
    def production(self):
        return self._production

    @property
    def development(self):
        return self._development

    def set_production(self, database):
        self._production = database

    def set_development(self, database):
        self._development = database


class BackendConfiguration(object):
    def __init__(self, yaml_backend=None):
        if yaml_backend is not None:
            self._framework = yaml_backend["framework"]
            self._database = DbConfiguration(yaml_backend["database"])
        else:
            self._framework = None
            self._database = DbConfiguration()

    @property
    def framework(self):
        return self._framework

    @property
    def database(self):
        return self._database

    def set_framework(self, framework):
        if framework == "flask":
            self._framework = framework
        else:
            print(f"Unsupported backend framework: {framework}")
            # TODO: Raise exception

    def set_database(self, environment, database):
        if database == "postgresql" or database == "sqlite":
            if environment == "production":
                self._database.set_production(database)
            elif environment == "development":
                self._database.set_development(database)
            else:
                print(f"Unsupported enviroment: {environment}")
                # TODO: Raise exception
        else:
            print(f"Unsupported database: {database}")
            # TODO: Raise exception


class ProjectConfiguration(object):
    def __init__(self, yaml_configuration=None):
        if yaml_configuration is not None:
            self._project_name = yaml_configuration["project_name"]
            self._backend = BackendConfiguration(yaml_configuration["backend"])
        else:
            self._project_name = None
            self._backend = BackendConfiguration()

    @property
    def project_name(self):
        return self._project_name

    @property
    def backend(self):
        return self._backend

    def set_project_name(self, project_name):
        self._project_name = sanitize_filename(project_name)

    def init_form(self):
        self._project_name = sanitize_filename(input("Enter project name: "))
