# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spacytextblob']

package_data = \
{'': ['*']}

install_requires = \
['spacy>=2.3.2,<3.0.0', 'textblob>=0.15.3,<0.16.0']

setup_kwargs = {
    'name': 'spacytextblob',
    'version': '0.1.3',
    'description': 'A TextBlob sentiment analysis pipeline compponent for spaCy',
    'long_description': None,
    'author': 'SamEdwardes',
    'author_email': 'edwardes.s@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
