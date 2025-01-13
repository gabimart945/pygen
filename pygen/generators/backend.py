from abc import ABC, abstractmethod
from pygen.generators.api import FlaskApiGenerator
from pygen.models.backend_pim import PimModel, Entity


class IBackendGenerator(ABC):
    """
    Abstract base class for backend code generators.

    Provides the interface for generating folders, transforming models,
    and creating APIs for the backend, with the flexibility to support different architectures.

    Attributes:
        _config (object): Configuration object containing backend framework and other settings.
        _path (str): The root directory where the backend files will be generated.
        _cim_model (object): The Computation Independent Model (CIM) representing the input model.
        _api_generator (FlaskApiGenerator): The API generator for the backend (e.g., Flask).
    """
    def __init__(self, config, model, path):
        """
        Initializes the backend generator with the given configuration, model, and output path.

        Args:
            config (object): Configuration object for backend generation.
            model (object): The input Computation Independent Model (CIM).
            path (str): The root directory where backend files will be generated.
        """
        self._config = config
        self._path = path
        self._cim_model = model
        if self._config.backend.framework == 'flask':
            self._api_generator = FlaskApiGenerator(self._config)

    def generate(self):
        """
        Orchestrates the backend generation process by transforming the model,
        creating folder structures, and generating the API.
        """
        self._transform_model()
        self._generate_folders()
        self._generate_api()

    @abstractmethod
    def _generate_folders(self):
        """
        Abstract method to create the folder structure for the backend.

        Must be implemented by subclasses.
        """
        raise NotImplementedError

    @abstractmethod
    def _transform_model(self):
        """
        Abstract method to transform the input CIM into a Platform Independent Model (PIM).

        Must be implemented by subclasses.
        """
        raise NotImplementedError

    def _generate_api(self):
        """
        Generates the API for the backend using the transformed PIM.

        Raises:
            NotImplementedError: If not implemented by subclasses.
        """
        raise NotImplementedError


class MonolithicBackendGenerator(IBackendGenerator):
    """
    Backend generator for monolithic architectures.

    Transforms the CIM into a single PIM and generates a monolithic backend.
    """
    def __init__(self, config, model, path):
        """
        Initializes the monolithic backend generator.

        Args:
            config (object): Configuration object for backend generation.
            model (object): The input CIM.
            path (str): The root directory for backend generation.
        """
        super().__init__(config, model, path)
        self._pim_model = None

    def _generate_folders(self):
        """
        Generates the folder structure for a monolithic backend.

        Note:
            This implementation is a placeholder and can be extended as needed.
        """
        pass

    def _transform_model(self):
        """
        Transforms the CIM into a single PIM for the monolithic backend.
        """
        self._cim_to_pim()

    def _generate_api(self):
        """
        Generates the API for the monolithic backend using the transformed PIM model.
        """
        self._api_generator.generate(self._pim_model, self._path)

    def _cim_to_pim(self):
        """
        Transforms the current CIM (Computation Independent Model) into a PIM (Platform Independent Model).

        This function processes:
        - Attributes from the CIM entities.
        - Relationships considering both `source` and `target` multiplicities (`0..1`, `1`, `0..*`, `1..*`).
        - Sets the `foreign_key` field for attributes that represent foreign keys in `many-to-one` or `one-to-one` relationships.

        Postcondition:
        - The PIM model (`self._pim_model`) is populated with transformed entities and relationships.
        """
        self._pim_model = PimModel()  # Initialize the PIM model

        # Transform each entity from CIM to PIM
        for cim_entity in self._cim_model.entities:
            # Create a new PIM entity corresponding to the current CIM entity
            pim_entity = Entity(cim_entity.name)

            # Add a primary key attribute (`id`) to the PIM entity
            pim_entity.add_attribute("id", "Integer", primary_key=True, nullable=False)

            # Add attributes from the CIM entity to the PIM entity
            for cim_attribute in cim_entity.attributes:
                pim_entity.add_attribute(
                    cim_attribute.name,
                    cim_attribute.type,
                    nullable=True  # Default: Attributes are nullable unless otherwise specified
                )

            # Process relationships involving the current entity
            for cim_relationship in self._cim_model.relationships:
                if cim_relationship.source == cim_entity.name:
                    # Determine the type of relationship, nullable, and whether a foreign key is needed
                    source_multiplicity = cim_relationship.source_multiplicity
                    target_multiplicity = cim_relationship.target_multiplicity
                    rel_type, nullable, add_foreign_key = determine_relationship_properties(
                        source_multiplicity, target_multiplicity, cim_relationship.type
                    )

                    # Add foreign key only if needed
                    if add_foreign_key:
                        foreign_key = f"{cim_relationship.target.lower()}s.id"
                        pim_entity.add_attribute(
                            f"{cim_relationship.target.lower()}_id",
                            "Integer",
                            nullable=nullable,
                            foreign_key=foreign_key
                        )

                    # Add the relationship to the source entity
                    pim_entity.add_relationship(
                        name=f"{cim_relationship.target.lower()}",
                        target=cim_relationship.target,
                        rel_type=rel_type
                    )

                elif cim_relationship.target == cim_entity.name:
                    # Determine the type of relationship, nullable, and whether a foreign key is needed
                    source_multiplicity = cim_relationship.source_multiplicity
                    target_multiplicity = cim_relationship.target_multiplicity
                    rel_type, nullable, add_foreign_key = determine_relationship_properties(
                        target_multiplicity, source_multiplicity, cim_relationship.type
                    )

                    # Add foreign key only if needed
                    if add_foreign_key:
                        foreign_key = f"{cim_relationship.source.lower()}s.id"
                        pim_entity.add_attribute(
                            f"{cim_relationship.source.lower()}_id",
                            "Integer",
                            nullable=nullable,
                            foreign_key=foreign_key
                        )

                    # Add the relationship to the target entity
                    pim_entity.add_relationship(
                        name=f"{cim_relationship.source.lower()}",
                        target=cim_relationship.source,
                        rel_type=rel_type
                    )

            # Add the transformed PIM entity to the PIM model
            self._pim_model.add_entity(pim_entity)


class MicroservicesBackendGenerator(IBackendGenerator):
    """
    Backend generator for microservices architectures.

    Creates a separate PIM for each entity in the CIM and generates individual services.
    """
    def __init__(self, config, model, path):
        """
        Initializes the microservices backend generator.

        Args:
            config (object): Configuration object for backend generation.
            model (object): The input CIM.
            path (str): The root directory for backend generation.
        """
        super().__init__(config, model, path)
        self._microservice_pim_models = []
        self._microservice_paths = {}

    def _generate_folders(self):
        """
        Creates a folder for each microservice based on its entity name.
        """
        for model in self._config.models:
            print(f"Generate folder for {model.entity.name}")
            self._microservice_paths[model.entity.name] = self._path + "/" + model.entity.name
        pass

    def _transform_model(self):
        """
        Transforms the CIM into individual PIMs, one for each microservice.
        """
        self._cim_to_pims()

    def _generate_api(self):
        """
        Generates the API for each microservice using its corresponding PIM model.
        """
        port = 5000
        for model in self._config.models:
            self._api_generator.generate(model, self._microservice_paths[model.entity.name], port)
            port = port + 1

    def _cim_to_pims(self):
        """
        Transforms the current CIM (Computation Independent Model) into a list of PIM models for microservices.

        This method creates a separate PIM model for each entity in the CIM. Each PIM model:
        - Represents a single entity as a microservice.
        - Includes the entity's attributes.
        - Adds relationships as foreign keys for related entities based on multiplicity and type.
        - Includes explicit relationships for documentation and design.

        Steps:
        1. Iterate over each entity in the CIM model.
        2. Create a new PIM model for the entity.
        3. Add the entity's attributes, including a primary key (`id`).
        4. Add relationships:
            - Foreign keys for related entities with `nullable` determined by multiplicity.
            - Explicit relationships indicating relationship types (e.g., `one-to-many`, `many-to-one`).

        Postcondition:
        - Returns a list of PIM models, one for each entity in the CIM model.

        """
        self._microservice_pim_models = []  # List to store individual PIM models for microservices

        # Transform each entity from CIM to PIM
        for cim_entity in self._cim_model.entities:
            pim_model = PimModel()
            # Create a new PIM entity corresponding to the current CIM entity
            pim_entity = Entity(cim_entity.name)

            # Add a primary key attribute (`id`) to the PIM entity
            pim_entity.add_attribute("id", "Integer", primary_key=True, nullable=False)

            # Add attributes from the CIM entity to the PIM entity
            for cim_attribute in cim_entity.attributes:
                pim_entity.add_attribute(
                    cim_attribute.name,
                    cim_attribute.type,
                    nullable=True  # Default: Attributes are nullable unless otherwise specified
                )

            # Process relationships involving the current entity
            for cim_relationship in self._cim_model.relationships:
                if cim_relationship.source == cim_entity.name:
                    # Determine the type of relationship, nullable, and whether a foreign key is needed
                    source_multiplicity = cim_relationship.source_multiplicity
                    target_multiplicity = cim_relationship.target_multiplicity
                    rel_type, nullable, add_foreign_key = determine_relationship_properties(
                        source_multiplicity, target_multiplicity, cim_relationship.type
                    )

                    # Add foreign key only if needed
                    if add_foreign_key:
                        foreign_key = f"{cim_relationship.target.lower()}s.id"
                        pim_entity.add_attribute(
                            f"{cim_relationship.target.lower()}_id",
                            "Integer",
                            nullable=nullable,
                            foreign_key=foreign_key
                        )

                    # Add the relationship to the source entity
                    pim_entity.add_relationship(
                        name=f"{cim_relationship.target.lower()}",
                        target=cim_relationship.target,
                        rel_type=rel_type
                    )

                elif cim_relationship.target == cim_entity.name:
                    # Determine the type of relationship, nullable, and whether a foreign key is needed
                    source_multiplicity = cim_relationship.source_multiplicity
                    target_multiplicity = cim_relationship.target_multiplicity
                    rel_type, nullable, add_foreign_key = determine_relationship_properties(
                        target_multiplicity, source_multiplicity, cim_relationship.type
                    )

                    # Add foreign key only if needed
                    if add_foreign_key:
                        foreign_key = f"{cim_relationship.source.lower()}s.id"
                        pim_entity.add_attribute(
                            f"{cim_relationship.source.lower()}_id",
                            "Integer",
                            nullable=nullable,
                            foreign_key=foreign_key
                        )

                    # Add the relationship to the target entity
                    pim_entity.add_relationship(
                        name=f"{cim_relationship.source.lower()}",
                        target=cim_relationship.source,
                        rel_type=rel_type
                    )

            # Add the entity to the microservice PIM model
            pim_model.add_entity(pim_entity)
            self._microservice_pim_models.append(pim_model)


def determine_relationship_properties(source_multiplicity, target_multiplicity, relation_type):
    """
    Determines the relationship properties (type, nullable, and foreign key requirement) based on multiplicities.

    Args:
        source_multiplicity (str): Multiplicity of the source (`0..1`, `1`, `0..*`, `1..*`).
        target_multiplicity (str): Multiplicity of the target (`0..1`, `1`, `0..*`, `1..*`).
        rel_type (str): Type of relationship (`composition`, `aggregation`, `association`).

    Returns:
        tuple: A tuple containing:
            - rel_type (str): The type of relationship in the PIM model (`one-to-one`, `one-to-many`, etc.).
            - nullable (bool): Whether the attribute is nullable.
            - add_foreign_key (bool): Whether to add a foreign key for this relationship.
    """
    # Determine nullability
    nullable = "0" in source_multiplicity or "0" in target_multiplicity

    # Determine relationship type based on multiplicities
    if source_multiplicity == "1" and target_multiplicity == "1":
        rel_type = "one-to-one"
        add_foreign_key = True
    elif source_multiplicity in ["1", "1..*"] and target_multiplicity in ["0..*", "1..*"]:
        rel_type = "one-to-many"
        add_foreign_key = False
    elif source_multiplicity in ["0..*", "1..*"] and target_multiplicity in ["1", "1..*"]:
        rel_type = "many-to-one"
        add_foreign_key = True
    elif source_multiplicity in ["0..*", "1..*"] and target_multiplicity in ["0..*", "1..*"]:
        rel_type = "many-to-many"
        add_foreign_key = False
    else:
        raise ValueError(f"Unsupported multiplicities: {source_multiplicity}, {target_multiplicity}")

    # Adjust nullability for compositions
    if relation_type == "composition":
        nullable = False

    return rel_type, nullable, add_foreign_key