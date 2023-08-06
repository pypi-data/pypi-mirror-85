from common_components.trees.project_trees import ProjectTree
from common_components.trees.env_and_deploy_files import\
    DockerTree, JenkinsTree
from common_components.trees.test_project_sample import\
    TestProjectSampleTree
from common_components.trees.test_project_tree import \
    TestProjectTree


class ProjectCollection:

    def __init__(self, directory, project_type):
        self.project_type = project_type
        self.directory = directory

    def get_project_structure(self):
        """
        This method to store objects of projects trees
        :return: object of tree for particular project
        """
        projects = {"general-tests-project":
                    TestProjectSampleTree(self.directory),
                    "pytest-tests-project":
                        TestProjectTree(self.directory),
                    "docker": DockerTree(self.directory),
                    "jenkins": JenkinsTree(self.directory)}
        return projects.get(self.project_type)

    def build_project(self):
        project = self.get_project_structure()
        return ProjectTree(project).create_project_tree(project.tree,
                                                        project.root_dir_name)
