# flake8: noqa

from enum import Enum


class Descriptions(Enum):
    CONFIG_EXAMPLE = """# store here all  environment variables. Refer to example below: here is var USERNAME that
# could be loaded from
# .env file, or John will be used as a default one
# import os
# from os.path import join, dirname
# from dotenv import load_dotenv

# dotenv_path = join(dirname(__file__), ".env")
# load_dotenv(dotenv_path)

# USERNAME = os.environ.get("USERNAME", "John")

    """

    BASE_POPUP_EXAMPLE = """# Store here common locators and methods for popups of target APP to build Page Object
# structure.
# From this class, all other popups classes will be inherited. NOTE: in example below imports
# are ignored for simplicity

# class BasePopup:
#  POPUP_MODAL = (By.CSS_SELECTOR, "some.css.locator")

#  def __init__(self, driver):
#      self.driver = driver

#  def is_popup_displayed(self):
#     pass

            """

    BASE_PAGE_EXAMPLE = """# Store here common locators and methods for pages of target APP to build
# Page Object structure.
# From this class, all other page classes will be inherited. NOTE: in example below imports
# are ignored for simplicity

# class BasePage:
#   MENU_LIST = (By.CSS_SELECTOR, "some.css.locator.on.page")

#   def __init__(self, driver):
#       self.driver = driver

#  def is_main_menu_displayed(self):
#      pass

    """

    BASE_TEST = """# Create here base class for tests, from which every test will be inherited.
# Example:
# @pytest.mark.usefixtures('preconditions', 'postconditions', 'report_generation')
# class BaseTest:
#       pass

    """

    TOOLS_DESCRIPTION = """# Put here any scripts, emulators, stubs other useful staff, that required
# for test environment or test
# execution, but not directly related to target app

"""

    BASE_SERVICE_DESCRIPTION = """# Create here base class for the application API. Store payloads, routes and methods
#             Example of base service class:
# class BaseService:
#
#     def __init__(self):
#         self.route = ""
#         self.uri = ""
#         self.header = ""
#
#     def post(self, payload: dict, headers, *routes):
#         pass

    """

    REQUIREMENTS_FILE = """ # Put in this file all libs that required for environment
# Example:
# setuptools==50.3.2
# wheel==0.35.1
# twine==3.2.0

"""

    CONFTEST_FILE = """ # External plugin loading: conftest.py is used to import external plugins or modules.
# By defining the following global variable, pytest will load the module and make it available for its test.
# Plugins are generally files defined in your project or other modules which might be needed in your tests.

    """

    PYTEST_INI_FILE = """ # This file is for basic test configuration.
# Refer to https://docs.pytest.org/en/2.7.3/customize.html

    """

    DOCKER_FILE = """ # In case if the test project is supposed to be executed on other machines or via CI tools,
# (Jenkins for example), it would be handy to put code into a docker container. Dockerfile is required for image
# creation. Refer to docker documentation https://docs.docker.com/engine/reference/builder/

    """

    DOCKER_COMPOSE_FILE = """ # In case if more than one container is creating for the test project, compose could be
# used. Compose is a tool for defining and running multi-container Docker applications. With Compose, you use a YAML
# file to configure your application’s services. Then, with a single command, you create and start all the services
# from your configuration. To learn more about all the features of Compose, see the list of features.
# Refer to https://docs.docker.com/compose/

    """

    JENKINSFILE = """ # In case if project us supposed to be executed on CI (Jenkins), Jenkins Pipeline is handy to
# create and support jobs "as code". Purpose of Jenkinsfile - store Jenkins Pipeline script. Get more from the Jenkins
# documentation -  https://www.jenkins.io/doc/book/pipeline/getting-started/

    """

    README = """<Name of the project>.
<Project description>

## Table of Contents
* [Get Started](#get-started)
* [Test Run](#test-run)
* [Documentation](#documentation)

## Get Started <a name="get-started">

## Test Run <a name="test-run">

## Documentation <a name="documentation">
"""
