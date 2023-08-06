# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['preql', 'preql.jup_kernel']

package_data = \
{'': ['*'], 'preql': ['modules/*']}

install_requires = \
['dsnparse',
 'lark-parser>=0.11.1,<0.12.0',
 'prompt-toolkit',
 'pygments',
 'rich',
 'runtype>=0.1.6,<0.2.0',
 'tqdm']

extras_require = \
{'mysql': ['mysqlclient'], 'pgsql': ['psycopg2'], 'server': ['starlette']}

entry_points = \
{'console_scripts': ['preql = preql.__main__:main']}

setup_kwargs = {
    'name': 'prql',
    'version': '0.1.12',
    'description': 'An interpreted relational query language that compiles to SQL',
    'long_description': '![alt text](logo_small.png "Logo")\n\nPreql (*pronounced: Prequel*) is an interpreted relational query language.\n\nIt is designed for use by data engineers, analysts and data scientists.\n\n* Compiles to SQL at runtime. It has the performance and abilities of SQL, and much more.\n\n    * Support for Postgres, MySQL and Sqlite. (more planned!)\n\n    * Escape hatch to SQL, for all those database-specific features we didn\'t think to include\n\n* Programmer-friendly syntax and semantics, with gradual type-checking, inspired by Typescript and Python\n\n* Interface through Python, HTTP or a terminal environment with autocompletion\n\n\n**Note: Preql is still work in progress, and isn\'t ready for production use, or any serious use yet**\n\n# Documentation\n\n[Read here](https://preql.readthedocs.io/en/latest/)\n\n# Get started\n\nSimply install via pip:\n\n```sh\n    pip install -U prql\n```\n\nThen just run the interpreter:\n\n```sh\n    preql\n```\n\nRequires Python 3.8+\n\n[Read more](https://preql.readthedocs.io/en/latest/getting-started.html)\n\n# Quick Example\n\n```javascript\n// Sum up all the squares of an aggregated list of numbers\n// Grouped by whether they are odd or even\nfunc sqrsum(x) = sum(x * x)\nfunc is_even(x) = x % 2 == 0\n\nprint [1..100]{\n        is_even(item) => sqrsum(item)\n      }\n// Result is:\n┏━━━━━━━━━┳━━━━━━━━┓\n┃ is_even ┃ sqrsum ┃\n┡━━━━━━━━━╇━━━━━━━━┩\n│       0 │ 166650 │\n│       1 │ 161700 │\n└─────────┴────────┘\n```\n\nIn the background, this was run by executing the following SQL code (reformatted):\n\n```sql\n  WITH range1 AS (SELECT 1 AS item UNION ALL SELECT item+1 FROM range1 WHERE item+1<100)\n     , subq_3(is_even, sqrsum) AS (SELECT ((item % 2) = 0) AS is_even, SUM(item * item) AS sqrsum FROM range1 GROUP BY 1)\n  SELECT * FROM subq_3\n```\n\n# License\n\nPreql uses an “Interface-Protection Clause” on top of the MIT license.\n\nSee: [LICENSE](LICENSE)\n\nIn simple words, it can be used for any commercial or non-commercial purpose, as long as your product doesn\'t base its value on exposing the Preql language itself to your users.\n\nIf you want to add the Preql language interface as a user-facing part of your commercial product, contact us for a commercial license.\n',
    'author': 'Erez Shin',
    'author_email': 'erezshin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/erezsh/Preql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
