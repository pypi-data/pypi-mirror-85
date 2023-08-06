# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyaccelerator', 'pyaccelerator.elements']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.0,<4.0.0', 'numpy>=1.19.0,<2.0.0', 'scipy>=1.5.2,<2.0.0']

extras_require = \
{'docs': ['sphinx<3.3.0',
          'sphinx-autoapi>=1.5.0,<2.0.0',
          'sphinx-rtd-theme>=0.5.0,<0.6.0',
          'm2r2>=0.2.5,<0.3.0']}

setup_kwargs = {
    'name': 'pyaccelerator',
    'version': '0.1.0',
    'description': 'Accelerator building blocks.',
    'long_description': None,
    'author': 'Loic Coyle',
    'author_email': 'loic.coyle <loic.coyle@hotmail.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
