from enum import Enum


class BasePythonFileDir(Enum):
    INIT = "__init__.py"
    README = "README.md"
    REQUIREMENTS_FILE = "requirements.txt"
    DOCKER_FILE = "Dockerfile"
    DOCKER_COMPOSE_FILE = "docker-compose.yml"
    JENKINSFILE = "Jenkinsfile"
