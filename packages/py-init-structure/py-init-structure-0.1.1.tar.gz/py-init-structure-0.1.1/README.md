# py-init-structure
This project to create sample structure for the tests project [py-init-structure](https://github.com/Sergii22/py-init-structure)

Available options for now:
- `general-tests-project` - creates folders for common test project without binding to any language or framework 
- `pytest-tests-project` -  creates folders for common test project with pytest, adds common files with package descriptions

### How to use
Start with `init_structure` command and follow interactive instruction to setup project file structure

### How to contribute
If you want to add sample structure of your project (doesn't matter language or purpose), it could be done in following way:
- install this lib 
- goto directory of your project
- execute `dir_tree_to_json` command (tree in required format will be printed )
- use output of command above to create new class for you project. Refer to `common_components/trees/test_project_sample.py` file