from abc import ABC, abstractmethod
import yaml
import os


class PipelineGenerator(ABC):
    """
    Abstract base class for CI pipelines.
    """

    @abstractmethod
    def generate_backend_pipeline(self, output_path):
        """
        Abstract method to generate a CI pipeline for the backend.

        Args:
            output_path (str): Path where the backend pipeline configuration will be saved.
        """
        pass

    @abstractmethod
    def generate_frontend_pipeline(self, output_path):
        """
        Abstract method to generate a CI pipeline for the frontend.

        Args:
            output_path (str): Path where the frontend pipeline configuration will be saved.
        """
        pass


class AzureDevOpsPipelineGenerator(PipelineGenerator):
    """
    CI pipeline generator for Azure DevOps.
    """

    def generate_backend_pipeline(self, output_path):
        """
        Generates the YAML configuration for the backend CI in Azure DevOps.

        Args:
            output_path (str): Path where the backend pipeline configuration will be saved.
        """
        pipeline = {
            "trigger": {"branches": {"include": ["main"]}},
            "pool": {"name": "pc"},
            "steps": [
                {
                    "task": "UsePythonVersion@0",
                    "inputs": {"versionSpec": "3.10", "addToPath": True},
                },
                {
                    "script": "python -m pip install --upgrade pip\n"
                              "pip install -r requirements.txt\n"
                              "pip install bandit pip-audit junit-xml\n"
                              "pip install git+https://gabrielmartinez945@dev.azure.com/gabrielmartinez945/pip_audit_to_junit/_git/pip_audit_to_junit",
                    "displayName": "Install dependencies and tools",
                },
                {
                    "script": "PYTHONPATH=$(System.DefaultWorkingDirectory) pytest tests/unit --junitxml=test-results.xml",
                    "displayName": "Run unit tests",
                },
                {
                    "task": "PublishTestResults@2",
                    "inputs": {
                        "testResultsFormat": "JUnit",
                        "testResultsFiles": "**/test-results.xml",
                        "failTaskOnFailedTests": True,
                        "testRunTitle": "Unit Test Results",
                    },
                    "displayName": "Publish unit test results",
                },
                {
                    "script": "PYTHONPATH=$(System.DefaultWorkingDirectory) pytest tests/security --junitxml=test-results.xml",
                    "displayName": "Run security tests",
                },
                {
                    "task": "PublishTestResults@2",
                    "inputs": {
                        "testResultsFormat": "JUnit",
                        "testResultsFiles": "**/test-results.xml",
                        "failTaskOnFailedTests": True,
                        "testRunTitle": "Security Test Results",
                    },
                    "displayName": "Publish security test results",
                },
                {
                    "script": "PYTHONPATH=$(System.DefaultWorkingDirectory) pytest tests/integration --junitxml=test-results.xml",
                    "displayName": "Run integration tests",
                },
                {
                    "task": "PublishTestResults@2",
                    "inputs": {
                        "testResultsFormat": "JUnit",
                        "testResultsFiles": "**/test-results.xml",
                        "failTaskOnFailedTests": True,
                        "testRunTitle": "Integration Test Results",
                    },
                    "displayName": "Publish integration test results",
                },
                {
                    "script": "bandit -r . -f xml -o bandit-report.xml || true",
                    "displayName": "Run Bandit security analysis",
                },
                {
                    "task": "PublishTestResults@2",
                    "inputs": {
                        "testResultsFormat": "JUnit",
                        "testResultsFiles": "**/bandit-report.xml",
                        "failTaskOnFailedTests": False,
                        "testRunTitle": "Bandit Security Analysis",
                    },
                    "displayName": "Publish Bandit results",
                },
                {
                    "script": "pip-audit -r requirements.txt -f json -o pip-audit-report.json || true",
                    "displayName": "Run pip-audit for dependency CVEs",
                },
                {
                    "script": "pip-audit-to-junit pip-audit-report.json pip-audit-report.xml",
                    "displayName": "Convert pip-audit JSON to JUnit XML",
                },
                {
                    "task": "PublishTestResults@2",
                    "inputs": {
                        "testResultsFormat": "JUnit",
                        "testResultsFiles": "**/pip-audit-report.xml",
                        "failTaskOnFailedTests": True,
                        "testRunTitle": "Dependency CVE Analysis",
                    },
                    "displayName": "Publish pip-audit results",
                },
            ],
        }

        with open(output_path, "w") as file:
            yaml.dump(pipeline, file, sort_keys=False, default_flow_style=False)

        print(f"Azure DevOps backend CI pipeline configuration generated at {output_path}")

    def generate_frontend_pipeline(self, output_path):
        """
        Generates the YAML configuration for the frontend CI in Azure DevOps.

        Args:
            output_path (str): Path where the frontend pipeline configuration will be saved.
        """
        pipeline = {
            "trigger": {"branches": {"include": ["main"]}},
            "pool": {"name": "pc"},
            "steps": [
                {"script": "npm install", "displayName": "Install Dependencies"},
                {"script": "npm run build", "displayName": "Build Frontend"},
                {
                    "script": "npm test -- --reporters jest-junit --outputFile=jest-test-results.xml",
                    "displayName": "Run Frontend Tests and Generate Report",
                },
                {
                    "task": "PublishTestResults@2",
                    "inputs": {
                        "testResultsFormat": "JUnit",
                        "testResultsFiles": "**/jest-test-results.xml",
                        "failTaskOnFailedTests": True,
                        "testRunTitle": "Frontend Test Results",
                    },
                    "displayName": "Publish Frontend Test Results",
                },
                {
                    "script": "npm audit --json > npm-audit-report.json || true",
                    "displayName": "Run Dependency Security Analysis (npm audit)",
                },
                {
                    "script": (
                        "npm install -g audit-ci\n"
                        "audit-ci --json > audit-ci-report.json || true"
                    ),
                    "displayName": "Run Dependency Security Analysis (audit-ci)",
                },
                {
                    "script": (
                        "zap-cli start\n"
                        "zap-cli quick-scan http://localhost:3000 > zap-scan-report.json || true\n"
                        "zap-cli shutdown"
                    ),
                    "displayName": "Run OWASP ZAP Security Scan",
                },
                {
                    "task": "PublishTestResults@2",
                    "inputs": {
                        "testResultsFormat": "JUnit",
                        "testResultsFiles": "**/zap-scan-report.json",
                        "failTaskOnFailedTests": False,
                        "testRunTitle": "OWASP ZAP Security Scan Results",
                    },
                    "displayName": "Publish OWASP ZAP Scan Results",
                },
            ],
        }

        with open(output_path, "w") as file:
            yaml.dump(pipeline, file, sort_keys=False, default_flow_style=False)

        print(f"Azure DevOps frontend CI pipeline configuration generated at {output_path}")


class GitHubActionsPipelineGenerator(PipelineGenerator):
    """
    CI pipeline generator for GitHub Actions.
    """

    def generate_backend_pipeline(self, output_path):
        """
        Generates the YAML workflow configuration for the backend CI in GitHub Actions.

        Args:
            output_path (str): Path where the backend pipeline configuration will be saved.
        """
        workflow = {
            "name": "Backend CI",
            "on": {
                "push": {"branches": ["main"]},
                "pull_request": {"branches": ["main"]},
            },
            "jobs": {
                "build_backend": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v2"},
                        {
                            "uses": "actions/setup-python@v2",
                            "with": {"python-version": "3.10"},
                        },
                        {
                            "run": (
                                "python -m pip install --upgrade pip\n"
                                "pip install -r requirements.txt\n"
                                "pip install bandit pip-audit junit-xml\n"
                                "pip install git+https://gabrielmartinez945@dev.azure.com/gabrielmartinez945/pip_audit_to_junit/_git/pip_audit_to_junit"
                            ),
                            "name": "Install dependencies and tools",
                        },
                        {
                            "run": "PYTHONPATH=$(pwd) pytest tests/unit --junitxml=unit-test-results.xml",
                            "name": "Run unit tests",
                        },
                        {
                            "uses": "actions/upload-artifact@v2",
                            "with": {
                                "name": "Unit Test Results",
                                "path": "unit-test-results.xml",
                            },
                            "name": "Upload unit test results",
                        },
                        {
                            "run": "PYTHONPATH=$(pwd) pytest tests/security --junitxml=security-test-results.xml",
                            "name": "Run security tests",
                        },
                        {
                            "uses": "actions/upload-artifact@v2",
                            "with": {
                                "name": "Security Test Results",
                                "path": "security-test-results.xml",
                            },
                            "name": "Upload security test results",
                        },
                        {
                            "run": "PYTHONPATH=$(pwd) pytest tests/integration --junitxml=integration-test-results.xml",
                            "name": "Run integration tests",
                        },
                        {
                            "uses": "actions/upload-artifact@v2",
                            "with": {
                                "name": "Integration Test Results",
                                "path": "integration-test-results.xml",
                            },
                            "name": "Upload integration test results",
                        },
                        {
                            "run": "bandit -r . -f xml -o bandit-report.xml || true",
                            "name": "Run Bandit security analysis",
                        },
                        {
                            "uses": "actions/upload-artifact@v2",
                            "with": {
                                "name": "Bandit Security Analysis",
                                "path": "bandit-report.xml",
                            },
                            "name": "Upload Bandit security analysis results",
                        },
                        {
                            "run": "pip-audit -r requirements.txt -f json -o pip-audit-report.json || true",
                            "name": "Run pip-audit for dependency CVEs",
                        },
                        {
                            "run": "pip-audit-to-junit pip-audit-report.json pip-audit-report.xml",
                            "name": "Convert pip-audit JSON to JUnit XML",
                        },
                        {
                            "uses": "actions/upload-artifact@v2",
                            "with": {
                                "name": "Dependency CVE Analysis",
                                "path": "pip-audit-report.xml",
                            },
                            "name": "Upload pip-audit results",
                        },
                    ],
                }
            },
        }

        with open(output_path, "w") as file:
            yaml.dump(workflow, file, sort_keys=False, default_flow_style=False)

        print(f"GitHub Actions backend CI workflow configuration generated at {output_path}")

    def generate_frontend_pipeline(self, output_path):
        """
        Generates the YAML workflow configuration for the frontend CI in GitHub Actions.

        Args:
            output_path (str): Path where the frontend pipeline configuration will be saved.
        """
        workflow = {
            "name": "Frontend CI",
            "on": {
                "push": {"branches": ["main"]},
                "pull_request": {"branches": ["main"]},
            },
            "jobs": {
                "build_frontend": {
                    "runs-on": "ubuntu-latest",
                    "steps": [
                        {"uses": "actions/checkout@v2"},
                        {"run": "npm install", "name": "Install Dependencies"},
                        {"run": "npm run build", "name": "Build Frontend"},
                        {
                            "run": "npm test -- --reporters jest-junit --outputFile=jest-test-results.xml",
                            "name": "Run Frontend Tests and Generate Report",
                        },
                        {
                            "uses": "actions/upload-artifact@v2",
                            "with": {
                                "name": "Frontend Test Results",
                                "path": "jest-test-results.xml",
                            },
                            "name": "Upload Frontend Test Results",
                        },
                        {
                            "run": "npm audit --json > npm-audit-report.json || true",
                            "name": "Run Dependency Security Analysis (npm audit)",
                        },
                        {
                            "uses": "actions/upload-artifact@v2",
                            "with": {
                                "name": "npm Audit Report",
                                "path": "npm-audit-report.json",
                            },
                            "name": "Upload npm Audit Report",
                        },
                        {
                            "run": "zap-cli start\nzap-cli quick-scan http://localhost:3000 > zap-scan-report.json || true\nzap-cli shutdown",
                            "name": "Run OWASP ZAP Security Scan",
                        },
                        {
                            "uses": "actions/upload-artifact@v2",
                            "with": {
                                "name": "OWASP ZAP Security Scan Report",
                                "path": "zap-scan-report.json",
                            },
                            "name": "Upload OWASP ZAP Scan Report",
                        },
                    ],
                }
            },
        }

        with open(output_path, "w") as file:
            yaml.dump(workflow, file, sort_keys=False, default_flow_style=False)

        print(f"GitHub Actions frontend CI workflow configuration generated at {output_path}")

