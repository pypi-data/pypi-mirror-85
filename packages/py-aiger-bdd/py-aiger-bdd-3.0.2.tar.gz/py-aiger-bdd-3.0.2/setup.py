# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiger_bdd']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=20.0.0,<21.0.0',
 'bidict>=0.21.0,<0.22.0',
 'dd>=0.5.4,<0.6.0',
 'funcy>=1.12,<2.0',
 'py-aiger>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'py-aiger-bdd',
    'version': '3.0.2',
    'description': 'Aiger to BDD bridge.',
    'long_description': "# py-aiger-bdd\n[![Build Status](https://cloud.drone.io/api/badges/mvcisback/py-aiger-bdd/status.svg)](https://cloud.drone.io/mvcisback/py-aiger-bdd)\n[![codecov](https://codecov.io/gh/mvcisback/py-aiger-bdd/branch/master/graph/badge.svg)](https://codecov.io/gh/mvcisback/py-aiger-bdd)\n\n[![PyPI version](https://badge.fury.io/py/py-aiger-bdd.svg)](https://badge.fury.io/py/py-aiger-bdd)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n# Installation\n\n`$ pip install py-aiger-bdd`\n\nFor developers, note that this project uses the\n[poetry](https://poetry.eustace.io/) python package/dependency\nmanagement tool. Please familarize yourself with it and then\nrun:\n\n`$ poetry install`\n\n# Usage\n\nThis tutorial assumes familiarity with [py-aiger](https://github.com/mvcisback/py-aiger) and [py-aiger-bv](https://github.com/mvcisback/py-aiger-bv).\n\n```python\nimport aiger_bv as BV\nfrom aiger_bdd import to_bdd, from_bdd, count\n\nx = BV.atom(3, 'x', signed=False) \n\nexpr = x < 5  # Could be an AIG or AIGBV or BoolExpr.\nbdd, manager, input2var = to_bdd(expr)  # Convert circuit encoded by expr into a BDD.\nexpr2 = from_bdd(bdd)  # Creates an Aiger Expression from a BDD.\n\nassert count(expr, fraction=True) == 5/8\nassert count(expr, fraction=False) == 5\n```\n",
    'author': 'Marcell Vazquez-Chanlatte',
    'author_email': 'mvc@linux.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mvcisback/py-aiger-bdd',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
