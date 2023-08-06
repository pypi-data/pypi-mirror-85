from common_components.src.test_project_files import \
    TestProjectFiles as TP
from common_components.src.base_files_dir import\
    BasePythonFileDir as BF
from common_components.src.descriptions import\
    Descriptions


class TestProjectSampleTree:

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
                    "name": TP.TOOLS_FOLDER.value,
                    "type": "directory",
                },
                {
                    "name": TP.TESTS_DIR.value,
                    "type": "directory",
                },
                {
                    "name": TP.PAGE_OBJECT_DIR.value,
                    "type": "directory",
                    "children": [
                        {
                            "name": TP.POPUPS_DIR.value,
                            "type": "directory",
                        },
                        {
                            "name": TP.PAGES_DIR.value,
                            "type": "directory",
                        }
                    ]
                },
                {
                    "name": TP.CONFIGS_DIR.value,
                    "type": "directory",
                },
                {
                    "name": TP.SERVICES_DIR.value,
                    "type": "directory",
                },
                {
                    "name": BF.README.value,
                    "type": "file",
                    "content": Descriptions.README.value
                }
            ]
        }
