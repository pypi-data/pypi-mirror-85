# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandasnotebooks']

package_data = \
{'': ['*']}

install_requires = \
['dbispipeline>=0.8.0,<0.9.0',
 'ipywidgets>=7.5.1,<8.0.0',
 'pandas>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'pandasnotebooks',
    'version': '0.3.7',
    'description': 'Widgets to analyze, manipulate dataframes from dbispipelines.',
    'long_description': None,
    'author': 'Benjamin Murauer',
    'author_email': 'b.murauer@posteo.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
