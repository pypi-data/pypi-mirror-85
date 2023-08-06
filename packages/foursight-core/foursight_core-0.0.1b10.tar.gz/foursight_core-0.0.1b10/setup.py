# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['foursight_core',
 'foursight_core.chalicelib',
 'foursight_core.chalicelib.checks',
 'foursight_core.chalicelib.checks.helpers',
 'foursight_core.scripts']

package_data = \
{'': ['*'], 'foursight_core.chalicelib': ['templates/*']}

install_requires = \
['Jinja2==2.10.1',
 'MarkupSafe==1.1.1',
 'PyJWT==1.5.3',
 'click==6.7',
 'dcicutils==1.1.0b1',
 'elasticsearch-dsl==6.4.0',
 'elasticsearch==6.4.0',
 'fuzzywuzzy==0.17.0',
 'geocoder==1.38.1',
 'gitpython>=3.1.2,<4.0.0',
 'google-api-python-client==1.7.4',
 'python-Levenshtein==0.12.0',
 'pytz>=2020.1,<2021.0']

setup_kwargs = {
    'name': 'foursight-core',
    'version': '0.0.1b10',
    'description': 'Serverless Chalice Application for Monitoring',
    'long_description': None,
    'author': '4DN-DCIC Team',
    'author_email': 'support@4dnucleome.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.7',
}


setup(**setup_kwargs)
