# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aleksis',
 'aleksis.apps.csv_import',
 'aleksis.apps.csv_import.management.commands',
 'aleksis.apps.csv_import.migrations',
 'aleksis.apps.csv_import.tests.models',
 'aleksis.apps.csv_import.tests.util',
 'aleksis.apps.csv_import.util']

package_data = \
{'': ['*'],
 'aleksis.apps.csv_import': ['locale/ar/LC_MESSAGES/*',
                             'locale/de_DE/LC_MESSAGES/*',
                             'locale/fr/LC_MESSAGES/*',
                             'locale/la/LC_MESSAGES/*',
                             'locale/nb_NO/LC_MESSAGES/*',
                             'locale/tr_TR/LC_MESSAGES/*',
                             'templates/csv_import/*']}

install_requires = \
['aleksis-app-chronos>=2.0a3.dev0,<3.0',
 'aleksis-core>=2.0a3.dev0,<3.0',
 'dateparser>=0.7.6,<0.8.0',
 'pandas>=1.0.0,<2.0.0',
 'phonenumbers>=8.10,<9.0',
 'pycountry>=20.7.3,<21.0.0']

entry_points = \
{'aleksis.app': ['csv_import = aleksis.apps.csv_import.apps:CSVImportConfig']}

setup_kwargs = {
    'name': 'aleksis-app-csvimport',
    'version': '2.0a1',
    'description': 'AlekSIS (School Information System)\u200a—\u200aApp for SchILD-NRW interaction',
    'long_description': 'AlekSIS (School Information System)\u200a—\u200aApp for CSV imports\n====================================================================\n\nAlekSIS\n-------\n\nThis is an application for use with the `AlekSIS`_ platform.\n\nFeatures\n--------\n\nThis app provides general CSV imports functions to interact with school administration software.\n\nSupported systems:\n* SchILD-NRW (North Rhine-Westphalia, Germany)\n* Pedasos (Schleswig-Holstein, Germany\n\nLicence\n-------\n\n::\n\n  Copyright © 2019, 2020 Dominik George <dominik.george@teckids.org>\n  Copyright © 2020 Jonathan Weth <dev@jonathanweth.de>\n  Copyright © 2019 mirabilos <thorsten.glaser@teckids.org>\n  Copyright © 2019 Tom Teichler <tom.teichler@teckids.org>\n\n  Licenced under the EUPL, version 1.2 or later\n\nPlease see the LICENCE.rst file accompanying this distribution for the\nfull licence text or on the `European Union Public Licence`_ website\nhttps://joinup.ec.europa.eu/collection/eupl/guidelines-users-and-developers\n(including all other official language versions).\n\n.. _AlekSIS: https://edugit.org/AlekSIS/AlekSIS\n.. _European Union Public Licence: https://eupl.eu/\n',
    'author': 'Dominik George',
    'author_email': 'dominik.george@teckids.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://aleksis.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
