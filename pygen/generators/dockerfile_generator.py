from abc import ABC, abstractmethod
import os


class DockerfileGenerator(ABC):
    """
    Abstract base class for Dockerfile generators.
    """

    def __init__(self, output_path):
        """
        Initializes the Dockerfile generator.

        Args:
            output_path (str): Path where the generated Dockerfile will be saved.
        """
        self.output_path = output_path

    @abstractmethod
    def generate(self):
        """
        Abstract method to generate the Dockerfile.
        """
        pass


class BackendDockerfileGenerator(DockerfileGenerator):
    """
    Dockerfile generator for backend projects.
    """

    def __init__(self, output_path, config):
        """
        Initializes the Dockerfile generator for backend projects.

        Args:
            output_path (str): Path where the generated Dockerfile will be saved.
            config (dict): Configuration specific to the Dockerfile.
        """
        super().__init__(output_path)
        self.config = config

    def generate(self):
        """
        Generates the Dockerfile for the backend.
        """
        base_image = self.config.get("base_image", "python:3.9-slim")
        port = self.config.get("port", 5000)

        dockerfile_content = f"""
# Dockerfile for Backend
FROM {base_image}

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY . /app

# Expose the application port
EXPOSE {port}

# Command to run the application
CMD ["python", "app.py"]
        """
        dockerfile_path = os.path.join(self.output_path, "Dockerfile")
        with open(dockerfile_path, "w") as file:
            file.write(dockerfile_content)
        print(f"Dockerfile for Backend generated at {dockerfile_path}")


class FrontendDockerfileGenerator(DockerfileGenerator):
    """
    Dockerfile generator for frontend projects.
    """

    def __init__(self, output_path, config):
        """
        Initializes the Dockerfile generator for frontend projects.

        Args:
            output_path (str): Path where the generated Dockerfile will be saved.
            config (dict): Configuration specific to the Dockerfile.
        """
        super().__init__(output_path)
        self.config = config

    def generate(self):
        """
        Generates the Dockerfile for the frontend.
        """
        base_image = self.config.get("base_image", "node:16-alpine")
        build_dir = self.config.get("build_dir", "build")

        dockerfile_content = f"""
# Dockerfile for Frontend
FROM {base_image}

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json files
COPY package*.json /app/

# Install dependencies
RUN npm install

# Copy the source code
COPY . /app

# Build the application
RUN npm run build

# Serve the application using a static file server
RUN npm install -g serve
WORKDIR /app/{build_dir}
CMD ["serve", "-s", "."]
        """
        dockerfile_path = os.path.join(self.output_path, "Dockerfile")
        with open(dockerfile_path, "w") as file:
            file.write(dockerfile_content)
        print(f"Dockerfile for Frontend generated at {dockerfile_path}")
