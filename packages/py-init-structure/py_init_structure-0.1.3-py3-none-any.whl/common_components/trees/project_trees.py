import os


class ProjectTree:
    def __init__(self, project_tree, root_dir=None):
        self.project_tree = project_tree
        self.root_dir = root_dir

    def create_project_tree(self, tree: dict, root_name=None):
        if not root_name:
            root_name = os.getcwd()

        os.makedirs(f"{root_name}", exist_ok=True)
        if tree.get("children"):
            for i in tree.get("children"):
                if i.get("type") == "directory":
                    self.create_project_tree(i, root_name + "/" +
                                             i.get("name"))
                else:
                    with open(os.path.join(root_name,
                                           i.get("name")), 'a') as temp_file:
                        if i.get("content"):
                            temp_file.write(i.get("content"))
                        else:
                            temp_file.write("")


def print_dir_tree(dirname, path=os.path.pathsep):
    data = []
    for name in os.listdir(dirname):
        dct = {'name': name}

        full_path = os.path.join(dirname, name)
        if os.path.isfile(full_path):
            dct['type'] = 'file'
        elif os.path.isdir(full_path):
            dct['type'] = 'folder'
            dct['children'] = print_dir_tree(
                full_path, path=path + name + os.path.pathsep)
        data.append(dct)
    return data
