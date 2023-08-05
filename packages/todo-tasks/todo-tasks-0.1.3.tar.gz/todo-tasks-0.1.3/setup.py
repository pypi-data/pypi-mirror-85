# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src', 'src.controllers', 'src.repositories', 'src.view']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'inseminator>=0.2,<0.3',
 'pydantic>=1.7.2,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'rich>=9.1.0,<10.0.0']

entry_points = \
{'console_scripts': ['tasks = src.entrypoint:run']}

setup_kwargs = {
    'name': 'todo-tasks',
    'version': '0.1.3',
    'description': '',
    'long_description': None,
    'author': 'Milan Suk',
    'author_email': 'Milansuk@email.cz',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
