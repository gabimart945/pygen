from setuptools import setup, find_packages


def parse_requirements(filename):
    """Load dependencies from a requirements file."""
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name="pygen",
    version="0.1.0",
    description="A tool for generating web applications automatically",
    author="Gabriel Martinez Pieper",
    author_email="gabriel.martinez945@comunidadunir.net",
    url="https://github.com/yourusername/pygen",  # Update this with your repository URL
    packages=find_packages(exclude=["tests", "tests.*", "example_files"]),
    include_package_data=True,
    install_requires=parse_requirements("requirements.txt"),
    entry_points={
        "console_scripts": [
            "pygen = pygen.__main__:main",  # Register the `pygen` command to call the `main` function
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
