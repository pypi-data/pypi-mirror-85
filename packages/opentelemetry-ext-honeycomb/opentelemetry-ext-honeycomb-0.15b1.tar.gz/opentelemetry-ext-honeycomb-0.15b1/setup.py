# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opentelemetry', 'opentelemetry.ext', 'opentelemetry.ext.honeycomb']

package_data = \
{'': ['*']}

install_requires = \
['libhoney>=1.10.0', 'opentelemetry-api>=0.15b0', 'opentelemetry-sdk>=0.15b0']

setup_kwargs = {
    'name': 'opentelemetry-ext-honeycomb',
    'version': '0.15b1',
    'description': 'OpenTelemetry plugins for Honeycomb',
    'long_description': None,
    'author': 'Honeycomb Authors',
    'author_email': 'solutions@honeycomb.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
