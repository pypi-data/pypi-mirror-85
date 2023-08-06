from setuptools import find_packages, setup

with open("README.md", "r") as rf:
    long_description = rf.read()

requirements = [
    "click==7.1.2",
    "questionary==1.8.0"
]

setup(
    name="py-init-structure",
    packages=find_packages(),
    version="0.1.3",
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Creates structure of autotest project",
    author="Sergii Golovach",
    license="MIT",
    classifiers=["Programming Language :: Python :: 3"],
    install_requires=requirements,
    entry_points='''
            [console_scripts]
            init_structure=common_components.src.controller:create_structure
            dir_tree_to_json=common_components.src.controller:print_current_dir_tree
        ''',
    python_requires='>=3.7.5',
)
