# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mimosa']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.3.0,<20.0.0',
 'cerberus>=1.3.2,<2.0.0',
 'click>=7.0,<8.0',
 'cutie>=0.2.2,<0.3.0',
 'firebase-admin>=3.2.1,<4.0.0',
 'halo>=0.0.28,<0.0.29',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['mimosa = mimosa.main:main']}

setup_kwargs = {
    'name': 'mimosa-monomer',
    'version': '0.1.0',
    'description': 'CLI for Stilt 2 database.',
    'long_description': "# mimosa \nDatabase management CLI for **Stilt 2**.\n\n## Installation\nRun `pip install mimosa_monomer-0.0.1-py3-none-any.whl` to install the package\ninto your chosen python environment.\n\nBe sure to update to the current wheel filename.\n\n## Usage\nRun `mimosa` in the terminal. Select the service account key file for the\ndesired Firebase project to connect to. Follow the prompts.\n\n# Development\nRun all tests with `tox` command.\n\nRun tests and recreate virtual environments with `tox --recreate`.\n\n## Docker Development Environment\nYou'll need Docker installed on your machine, obviously 😁.\n\n### Clone This Repository\n```\ngit clone https://github.com/hhelmric/mimosa.git\ncd mimosa\n```\n\n### Build The Image\n\nFrom cloned directory (where Dockerfile is located):\n```\ndocker build . -t mimosa:latest\n```\n\n**If you have updated `pyproject.toml`, and are experiencing odd behavior, \nyou may need to rebuild the image to get the correct dependencies.**\n\n### Run The Container\nFrom cloned directory.\n```\ndocker-compose run app\n```\n\nThis will run the container and begin a Bash terminal within. **The local source code directory will be synced with the container's `/code` directory.** Changes you make to source code in your IDE should be reflected in the container.\n\nFrom here you can execute commands:\n\n*  `tox` or `tox -e py38` to run tests against the installed version of the package.\n*  `poetry add some_package` or `poetry add --dev some_package` to add dependencies to pyproject.toml.\n*  `python -m mimosa.main` from within `src` folder to run the program against the non-installed source file.\n*  `poetry build` builds the package for distribution.\n*  `poetry publish` publishes package on pypi. You'll need a pypi account and to be added to the project as a collaborator.\n",
    'author': 'Daniel Hampton',
    'author_email': 'dhampton084@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
