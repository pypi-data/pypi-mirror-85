import click
import os
import json
import questionary

from common_components.src.projects_collection import ProjectCollection
from common_components.trees.project_trees import print_dir_tree


class QuestionaryOption(click.Option):

    def __init__(self, param_decls=None, **attrs):
        click.Option.__init__(self, param_decls, **attrs)
        if not isinstance(self.type, click.Choice):
            raise Exception('ChoiceOption type arg must be click.Choice')

    def prompt_for_value(self, ctx):
        val = questionary.select(self.prompt,
                                 choices=self.type.choices).unsafe_ask()
        return val


@click.command()
@click.option("--directory",
              prompt="Name of project root folder. \n"
                     "Skip this step by pressing Enter"
                     " btn if you want to add structure to current directory",
              default="",
              help="Name of directory where project will be created")
@click.option("--project-type", prompt="Select type of project",
              type=click.Choice(["general-tests-project",
                                 "pytest-tests-project"]),
              cls=QuestionaryOption)
@click.option('--docker', prompt="Will you use Docker in your project?",
              type=click.Choice(["yes",
                                 "no"]),
              cls=QuestionaryOption)
@click.option('--jenkins', prompt="Will you use Jenkins in your project?",
              type=click.Choice(["yes",
                                 "no"]),
              cls=QuestionaryOption)
def create_structure(directory, project_type, docker, jenkins):
    """
    Method to create structure of test project
    :param jenkins: to add files for Jenkins
    :param docker: to add files for Docker
    :param directory: directory where folders and files will be added
    :param project_type: specification for the project
    """
    ProjectCollection(directory=directory if directory else None,
                      project_type=project_type).build_project()
    if docker == "yes":
        ProjectCollection(directory=directory if directory else None,
                          project_type="docker").build_project()
    if jenkins == "yes":
        ProjectCollection(directory=directory if directory else None,
                          project_type="jenkins").build_project()


@click.command()
def print_current_dir_tree():
    print("Print structure")
    print(json.dumps(print_dir_tree(os.path.curdir), indent=4))
