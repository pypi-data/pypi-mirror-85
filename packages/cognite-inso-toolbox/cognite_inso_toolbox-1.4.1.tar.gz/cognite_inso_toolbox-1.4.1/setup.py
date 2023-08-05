# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['inso_toolbox',
 'inso_toolbox.drift_detector',
 'inso_toolbox.filter',
 'inso_toolbox.geometry',
 'inso_toolbox.impute',
 'inso_toolbox.physics',
 'inso_toolbox.physics.dimensionless',
 'inso_toolbox.physics.single_phase',
 'inso_toolbox.smoother',
 'inso_toolbox.ts_utils',
 'inso_toolbox.units',
 'inso_toolbox.units.utils',
 'inso_toolbox.utils']

package_data = \
{'': ['*']}

install_requires = \
['cognite-sdk>=2.6.2,<3.0.0', 'matplotlib>=3.3.0,<4.0.0', 'scipy>=1.4.1,<2.0.0']

setup_kwargs = {
    'name': 'cognite-inso-toolbox',
    'version': '1.4.1',
    'description': 'Inso Toolbox',
    'long_description': None,
    'author': 'cognite',
    'author_email': 'gustavo.zarruk@cognite.com, johannes.kolberg@cognite.com, nicolas.agnes@cognite.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
