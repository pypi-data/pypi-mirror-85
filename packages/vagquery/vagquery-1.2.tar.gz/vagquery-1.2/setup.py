# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vagquery']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2018.07,<2019.0', 'requests>=2.18.4,<3.0.0']

setup_kwargs = {
    'name': 'vagquery',
    'version': '1.2',
    'description': 'Queries for VAG public transportation time schedules',
    'long_description': '# vagquery\n\n[![Build Status](https://travis-ci.org/derphilipp/vagquery.svg?branch=master)](https://travis-ci.org/derphilipp/vagquery)\n[![Coverage Status](https://coveralls.io/repos/derphilipp/vagquery/badge.png?branch=master)](https://coveralls.io/r/derphilipp/vagquery?branch=master)\n\n\nA python library for generating and executing queries for the VAG public transport system\n[start.vag.de](https://start.vag.de)\n\nThis enables users with disabilities, hackers and you to receive information from the start.vag website.\n\n# General usage\n\nTwo classes are usually used:\n\n```\n    import vagquery\n    # Query for stations beginning with \'Schwe\'\n    stations = vagquery.StationQuery("Schwe").query()\n    for station in stations:\n        print(station)\n\n\n    # Query for next departures of the main railway station (id: 510)\n    departures = vagquery.DepartureQuery(510).query()\n    for departure in departures:\n        print(departure)\n```\n\nSpecialized usage\n============================\n\nFor repeated queries, the query object can be created and run again and again:\n\n```\n    dquery = vagquery.DepartureQuery(510)\n    departures = dquery.query()\n    # ...\n    # much later\n    # ...\n    departures = dquery.query()\n```\n\nFor a custom formating of the departures, the properties of a departure object can be used:\n\n```\n    departures = vagquery.DepartureQuery(510).query()\n    for departure in departures:\n        print(departure.product + " " + str(departure.latitude) + str(departure.longitude))\n```\n\n# License\n\n*vagquery* is licensed under the MIT license.\n\n',
    'author': 'Philipp Weißmann',
    'author_email': 'mail@philipp-weissmann.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/derphilipp/vagquery',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
