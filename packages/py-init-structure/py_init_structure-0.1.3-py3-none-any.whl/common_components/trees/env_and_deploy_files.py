from common_components.src.base_files_dir import \
    BasePythonFileDir as Base

from common_components.src.descriptions import \
    Descriptions as DC


class DockerTree:

    @property
    def dir_name(self):
        return self.root_dir_name

    def __init__(self, root_dir_name=None):
        self.root_dir_name = root_dir_name

    @property
    def tree(self):
        return self.tree_dict()

    def tree_dict(self):
        return {
            "name": self.root_dir_name,
            "type": "directory",
            "children": [
                {
                    "name": Base.DOCKER_COMPOSE_FILE.value,
                    "type": "file",
                    "content": DC.DOCKER_COMPOSE_FILE.value
                },
                {
                    "name": Base.DOCKER_FILE.value,
                    "type": "file",
                    "content": DC.DOCKER_FILE.value
                },
                {
                    "name": Base.JENKINSFILE.value,
                    "type": "file",
                    "content": DC.JENKINSFILE.value
                }
            ]
        }


class JenkinsTree:

    @property
    def dir_name(self):
        return self.root_dir_name

    def __init__(self, root_dir_name=None):
        self.root_dir_name = root_dir_name

    @property
    def tree(self):
        return self.tree_dict()

    def tree_dict(self):
        return {
            "name": self.root_dir_name,
            "type": "directory",
            "children": [
                {
                    "name": Base.JENKINSFILE.value,
                    "type": "file",
                    "content": DC.JENKINSFILE.value
                }
            ]
        }

