# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qmss_sl_practice',
 'qmss_sl_practice.docs',
 'qmss_sl_practice.qmss_sl_practice',
 'qmss_sl_practice.tests']

package_data = \
{'': ['*'], 'qmss_sl_practice.docs': ['source/*']}

install_requires = \
['pandas>=1.1.4,<2.0.0']

setup_kwargs = {
    'name': 'qmss-sl-practice',
    'version': '0.1.0',
    'description': 'This is a practice package.',
    'long_description': None,
    'author': 'Shiying Lai',
    'author_email': 'sl4849@columbia.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
