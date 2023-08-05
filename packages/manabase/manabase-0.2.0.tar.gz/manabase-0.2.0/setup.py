# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manabase',
 'manabase.filler',
 'manabase.filter',
 'manabase.filters',
 'manabase.filters.lands']

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
    'version': '0.2.0',
    'description': 'Manabase generator for all your Magic: The Gathering needs.',
    'long_description': '# manabase\n\nLanding rock solid mana bases for your decks.\n\nManabase is a command-line tool that helps you generate a mana base for your\nMagic: The Gathering decks.\n\nIt uses [scryfall](https://scryfall.com/) as its source of truth.\n\n## Installation\n\nManabase is available on [PyPI](https://pypi.org/project/manabase/)\nInstall manabase using `pip`:\n\n```bash\npip install --user manabase\n```\n\n## Usage\n\nManabase offers a primary command, `manabase`, that generates a list of lands\nfor a set of colors.\n\n### Filters\n\nManabase includes a set of powerful filters, defining which type of lands are\nallowed in the output list.\n\nThese type of lands are called land cycles, and are defined by\n[MTG Gamepedia](https://mtg.gamepedia.com/Dual_land).\n\nFollowing is a list of supported cycles, and the name of the corresponding\nfilter:\n\n- [`battle`](https://mtg.gamepedia.com/Battle_land): Battle for Zendikar dual lands.\n- [`bond`](https://mtg.gamepedia.com/Bond_land): Battlebond and Commander Legends crowd lands.\n- [`bounce`](https://mtg.gamepedia.com/Bounce_land): Ravnica bounce lands.\n- [`check`](https://mtg.gamepedia.com/Check_land): Ixalan and Innistrad check lands.\n- [`cycling`](https://mtg.gamepedia.com/Cycling_land#Dual-colored_Cycling_Lands):\n  Amonkhet cycling lands.\n- [`fast`](https://mtg.gamepedia.com/Fast_land): Mirrodin and Kaladesh fast lands.\n- [`fetch`](https://mtg.gamepedia.com/Fetch_land): Onslaught and Zendikar fetch lands.\n- [`filter`](https://mtg.gamepedia.com/Filter_land): Odyssey and Future Sight filter lands.\n- [`horizon`](https://mtg.gamepedia.com/Horizon_land): Future Sight and Modern Horizons horizon lands.\n- [`original`](https://mtg.gamepedia.com/Dual_land#Original_dual_lands):\n  The original dual lands.\n- [`pain`](https://mtg.gamepedia.com/Pain_land): Ice Age and Apocalypse pain lands.\n- [`reveal`](https://mtg.gamepedia.com/Reveal_land): Innistrad reveal lands.\n- [`scry`](https://mtg.gamepedia.com/Scry_land): Theros and M21 scry lands.\n- [`shock`](https://mtg.gamepedia.com/Shock_land): Ravnica shock lands.\n\nAdditionally, two color-related filters are provided:\n\nThese are:\n\n- `producer`: This filter checks if the land produces mana of the given colors.\n- `reference`: This filter checks if a reference to a land type of the given\n  colors is contained in the card text.\n\nWithout these filters, all colors could be matched.\n\nExamples:\n\n`fetch` will accept all fetch lands.\n`producer` will accept all lands that can produce your colors.\n\n### Operators\n\nFilters can be combined using four operators:\n\n- `&`: Accepts only cards matching both filters.\n- `|`: Accepts cards matching either filter.\n- `^`: Accepts cards matching one filter or the other, but not both.\n- `~`: Inverts the following filter results.\n\nMoreover, you can group operators and filters using parenthesis to\ncontrol operator precedence.\n\nExamples:\n\n- `reference & fetch` would match only fetch lands respecting your colors.\n- `(producer & original) | (reference & fetch)` would match either original\n  lands producing your colors, or fetch lands of your colors.\n\n### Filter arguments\n\nFinally, some filters can take arguments to control their behavior.\n\n`producer` and `reference` each take `exclusive` and `minimum_count` arguments.\n\n`exclusive`, which is true by default, prevents cards matching colors other than\nyours. For example, if you asked for white and blue, a white and red land would\nbe excluded, because it contains red.\n\n`minimum_count` sets the number of colors a land should match, among your colors,\nbefore being accepted. By default this is 2, which means lands have to produce\nor reference at least two of your colors to be accepted.\n\nThis filters can help you define a better behavior, for example for fetch lands\nit makes sense to disable the `exclusive` argument and set the `minimum_count`\nto 1, so that all fetch lands matching at least one of your colors are included.\n\nTo override arguments, specify your argument values in the right order, between\ncurly braces, separated by commas.\n\nExamples:\n\n- `producer { 0, 3 }` would match all lands producing at least three of your\n  colors, without excluding other colors.\n- `reference { 0, 1 } & fetch` would match fetch lands producing at least one\n  of your colors, without excluding other colors.\n\n### Commands\n\nIn the following examples, we are using the `manabase` command to generate\na set of lands for a white, blue and black deck.\n\nGenerate a set of lands using default settings:\n\n```bash\nmanabase WUB\n```\n\nGenerate a set of 37 maximum lands, with 1 occurrence of each land:\n\n```bash\nmanabase WUB --lands=37 --occurrences\n```\n\nGenerate a list of only fetch lands and original dual lands.\n\n```bash\nmanabase WUB --filters="(producer & original) | (reference & fetch)"\n```\n\n## Contributing\n\nThis package uses [`poetry`](https://python-poetry.org/) to manage its\ndependencies.\n\n### Installing\n\n[Install poetry](https://python-poetry.org/docs/#installation).\n\nClone this repository:\n\n```bash\ngit clone https://github.com/Aphosis/manabase\ncd manabase\n```\n\nInstall manabase for development:\n\n```bash\npoetry install\n```\n\n### Tests\n\nTests are written using [pytest](https://docs.pytest.org/en/stable/).\n\nOnce `manabase` has been installed, you can run tests to check if your\nchanges did not introduce regressions.\n\nTo run the test suite, `cd` into the `manabase` folder, then run:\n\n```bash\npytest\n```\n\nPytest is configured in `pyproject.toml`, you do not need to specify any\nextra arguments.\n\n## License\n\nThis tool is licensed under MIT.\n\n## Non affiliation disclaimer\n\nManabase is not affiliated, associated, authorized, endorsed by, or in any way\nofficially connected with Wizards of the Coast, or any of its subsidiaries or\nits affiliates.\n',
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
