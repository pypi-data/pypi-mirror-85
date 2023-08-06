from setuptools import find_packages, setup

requirements = [
    "click==7.1.2",
    "questionary==1.8.0",
    "prompt-toolkit==3.0.8",
    "wcwidth==0.2.5"
]

setup(
    name="py-init-structure",
    packages=find_packages(),
    version="0.1.0",
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
