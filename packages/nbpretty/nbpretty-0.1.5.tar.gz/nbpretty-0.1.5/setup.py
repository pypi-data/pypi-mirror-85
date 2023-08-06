# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nbpretty']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1,<6.0',
 'click>=7.0,<8.0',
 'ipython>=7.18.1,<8.0.0',
 'livereload>=2.6.3,<3.0.0',
 'nbconvert>=5.6,<6.0',
 'rich>=9.0.0,<10.0.0']

entry_points = \
{'console_scripts': ['nbpretty = nbpretty:main']}

setup_kwargs = {
    'name': 'nbpretty',
    'version': '0.1.5',
    'description': 'A tool to convert sets of Jupyter notebook files into a single, cohesive set of linked pages',
    'long_description': 'nbpretty\n========\n\nnbpretty is a tool to convert sets of notebook files into a single, cohesive set of linked pages.\n\nDocumentation at https://nbpretty.readthedocs.io\n',
    'author': 'Matt Williams',
    'author_email': 'matt@milliams.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/milliams/nbpretty',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
