# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manabase', 'manabase.filter', 'manabase.filters', 'manabase.filters.lands']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'diskcache>=5.0.3,<6.0.0',
 'parsimonious>=0.8.1,<0.9.0',
 'pydantic>=1.7.2,<2.0.0',
 'requests>=2.24.0,<3.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['manabase = manabase:manabase']}

setup_kwargs = {
    'name': 'manabase',
    'version': '0.1.0',
    'description': 'Manabase generator for all your Magic: The Gathering needs.',
    'long_description': '# manabase\n\nGet suggestions for your MTG decks manabase.\n',
    'author': 'Aphosis',
    'author_email': 'aphosis.github@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Aphosis/manabase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
