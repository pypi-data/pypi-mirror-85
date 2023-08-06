# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['instance',
 'statsservice',
 'statsservice.api.v1',
 'statsservice.commands',
 'statsservice.lib',
 'statsservice.models',
 'statsservice.views']

package_data = \
{'': ['*'],
 'statsservice': ['static/*', 'static/css/*', 'static/img/*', 'templates/*']}

install_requires = \
['Flask-SQLAlchemy>=2.4.3,<3.0.0',
 'Flask>=1.1.2,<2.0.0',
 'flask_login>=0.5.0,<0.6.0',
 'flask_principal>=0.4.0,<0.5.0',
 'flask_restx>=0.2.0,<0.3.0',
 'jsonschema>=3.2.0,<4.0.0',
 'pandas>=1.0.4,<2.0.0',
 'psycopg2-binary>=2.8.5,<3.0.0',
 'requests>=2.23.0,<3.0.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['monarc-stats-service = runserver:run']}

setup_kwargs = {
    'name': 'statsservice',
    'version': '0.2.0',
    'description': 'Stats Service for MONARC.',
    'long_description': '# Stats Service for MONARC\n\n[![Latest release](https://img.shields.io/github/release/monarc-project/stats-service.svg?style=flat-square)](https://github.com/monarc-project/stats-service/releases/latest)\n[![License](https://img.shields.io/github/license/monarc-project/stats-service.svg?style=flat-square)](https://www.gnu.org/licenses/agpl-3.0.html)\n[![Contributors](https://img.shields.io/github/contributors/monarc-project/stats-service.svg?style=flat-square)](https://github.com/monarc-project/stats-service/graphs/contributors)\n[![Workflow](https://github.com/monarc-project/stats-service/workflows/Python%20application/badge.svg?style=flat-square)](https://github.com/monarc-project/stats-service/actions?query=workflow%3A%22Python+application%22)\n[![CodeQL](https://github.com/monarc-project/stats-service/workflows/CodeQL/badge.svg?style=flat-square)](https://github.com/monarc-project/stats-service/actions?query=workflow%3A%22CodeQL%22)\n[![Documentation Status](https://readthedocs.org/projects/monarc-stats-service/badge/?version=latest&style=flat-square)](https://monarc-stats-service.readthedocs.io/en/latest/?badge=latest)\n[![PyPi version](https://img.shields.io/pypi/v/statsservice.svg?style=flat-square)](https://pypi.org/project/statsservice)\n\n## Presentation\n\n[This component](https://github.com/monarc-project/stats-service) provides an API\nin order to **collect** statistics from one or several\n[MONARC](https://github.com/monarc-project/MonarcAppFO) instances and to\n**return** these statistics with different filters and aggregation methods.\n\nIt can be deployed just next to a MONARC instance or on a dedicated server.\n\nThe collected statistics can be sent to an other stats instance.\n\n\n## Deployment\n\nThe following assumes you have already installed ``git``, ``poetry``,  and\n``Python >= 3.6.1``.\n\n```bash\n$ sudo apt install postgresql\n$ git clone https://github.com/monarc-project/stats-service\n$ cd stats-service/\n$ npm install\n$ cp instance/production.py.cfg instance/production.py\n$ poetry install\n$ poetry shell\n$ export FLASK_APP=runserver.py\n$ export FLASK_ENV=development\n$ export STATS_CONFIG=production.py\n$ flask db_create\n$ flask db_init\n\n$ flask client_create --name CASES\nName: CASES\nToken: SylsDTZTBk2zAkg016vW_aCuO1XQDXPsxrLuI1TG7z5sYvUfRlVf5R4g6kDnLI_o-c5iqrswrWzPANDKXmtV7Q\nCreated at: 2020-06-16 14:25:32.947745\n\n$ flask run\n * Serving Flask app "runserver.py" (lazy loading)\n * Environment: development\n * Debug mode: on\n * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n * Restarting with stat\n * Debugger is active!\n * Debugger PIN: 268-178-811\n```\n\n\n## Documentation\n\nA [documentation is available](https://monarc-stats-service.readthedocs.io).\n\n\n## License\n\n[Stats Service](https://github.com/monarc-project/stats-service) is under the\n[GNU Affero General Public License version 3](https://www.gnu.org/licenses/agpl-3.0.html).\n',
    'author': 'Cédric Bonhomme',
    'author_email': 'cedric@cedricbonhomme.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/monarc-project/stats-service',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
