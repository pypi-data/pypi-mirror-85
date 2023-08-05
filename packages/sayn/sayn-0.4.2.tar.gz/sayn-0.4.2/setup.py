# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sayn',
 'sayn.core',
 'sayn.database',
 'sayn.logging',
 'sayn.scaffolding',
 'sayn.scaffolding.data.init_project.python',
 'sayn.tasks',
 'sayn.utils']

package_data = \
{'': ['*'],
 'sayn.scaffolding': ['data/init_project/*',
                      'data/init_project/dags/*',
                      'data/init_project/sql/*']}

install_requires = \
['Click>=7.0,<8.0',
 'colorama>=0.4.3,<0.5.0',
 'halo>=0.0.30,<0.0.31',
 'jinja2>=2.10.3,<3.0.0',
 'pydantic>=1.6.1,<2.0.0',
 'ruamel.yaml>=0.16.12,<0.17.0',
 'sqlalchemy>=1.3.12,<2.0.0']

extras_require = \
{'all': ['graphviz>=0.14,<0.15',
         'psycopg2>=2.8.5,<3.0.0',
         'snowflake-connector-python>=2.0.3,<3.0.0',
         'snowflake-sqlalchemy>=1.1.18,<2.0.0',
         'pymysql>=0.9.3,<0.10.0'],
 'graphviz': ['graphviz>=0.14,<0.15'],
 'mysql': ['pymysql>=0.9.3,<0.10.0'],
 'postgresql': ['psycopg2>=2.8.5,<3.0.0'],
 'snowflake': ['snowflake-connector-python>=2.0.3,<3.0.0',
               'snowflake-sqlalchemy>=1.1.18,<2.0.0']}

entry_points = \
{'console_scripts': ['sayn = sayn.cli:cli']}

setup_kwargs = {
    'name': 'sayn',
    'version': '0.4.2',
    'description': 'Data-modelling and processing framework for automating Python and SQL tasks',
    'long_description': '<img\n  src="https://173-static-files.s3.eu-west-2.amazonaws.com/sayn_docs/logos/sayn_logo.png"\n  alt="SAYN logo"\n  style="width: 50%; height: 50%;"\n/>\n\n#\n\nSAYN is a data-modelling and processing framework for automating Python and SQL tasks. It enables analytics teams to build robust data infrastructures in minutes.\n\n *Status: SAYN currently supports UNIX operating systems (macOS, Linux).*\n\n## Use Cases\n\nSAYN can be used for multiple purposes across the analytics workflow:\n\n* Data extraction: complement tools such as Fivetran or Stitch with customised extraction processes.\n* Data modelling: transform raw data in your data warehouse.\n* Data science: integrate and execute data science models.\n\n## Key Features\n\nSAYN has the following key features:\n\n* YAML based creation of [DAGs](https://173tech.github.io/sayn/dags/) (Direct Acyclic Graph). This means all analysts, including non Python proficient ones, can contribute to building ETL processes.\n* [SQL SELECT statements](https://173tech.github.io/sayn/tasks/autosql/): turn your queries into managed tables and views automatically.\n* [Jinja parameters](https://173tech.github.io/sayn/parameters/): switch easily between development and product environment and other tricks with Jinja templating.\n* [Python tasks](https://173tech.github.io/sayn/tasks/python/): use Python scripts to complement your extraction and loading layer and build data science models.\n* Multiple [databases](https://173tech.github.io/sayn/databases/overview/) supported.\n* and much more... See the [Documentation](https://173tech.github.io/sayn/).\n\n## Design Principles\n\nSAYN is designed around three core principles:\n\n* **Simplicity**: data models and processes should be easy to create, scale and maintain. So your team can focus on data transformation instead of writing processes. SAYN orchestrates all your tasks systematically and provides a lot of automation features.\n* **Flexibility**: the power of data is unlimited and so should your tooling. SAYN currently supports both SQL and Python so your analysts can choose the most optimal solution for each process.\n* **Centralisation**: all analytics code should live in one place, making your life easier and allowing dependencies throughout the whole analytics process.\n\n## Quick Start\n\n```bash\n$ pip install sayn\n$ sayn init test_sayn\n$ cd test_sayn\n$ sayn run\n```\n\nThis is it! You completed your first SAYN run on the example project. Continue with the [Tutorial: Part 1](https://173tech.github.io/sayn/tutorials/tutorial_part1/) which will give you a good overview of SAYN\'s true power!\n\n## Support\n\nIf you need any help with SAYN, or simply want to know more, please contact the team at <sayn@173tech.com>.\n\n## License\n\nSAYN is open source under the [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) license.\n\n---\n\nMade with :heart: by [173tech](https://www.173tech.com).\n',
    'author': 'Robin Watteaux',
    'author_email': 'robin@173tech.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://173tech.github.io/sayn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
