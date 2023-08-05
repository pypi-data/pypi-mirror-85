# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flake8_django_migrations', 'flake8_django_migrations.checkers']

package_data = \
{'': ['*']}

install_requires = \
['astor>=0.1', 'flake8>=3.7']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=0.9']}

entry_points = \
{'flake8.extension': ['DM = flake8_django_migrations:Plugin']}

setup_kwargs = {
    'name': 'flake8-django-migrations',
    'version': '0.1.0',
    'description': 'Flake8 plugin to lint for backwards incompatible database migrations',
    'long_description': '# flake8-django-migrations\n\nFlake8 plugin to lint for backwards incompatible database migrations.\n\n## Installation\n\nInstall using `pip` (or your favourite package manager):\n\n```sh\npip install flake8-django-migrations\n```\n\n## Usage\n\nThis plugin should be used automatically when running flake8:\n\n```sh\nflake8\n```\n\n\n## Checks\n\nThis is the list of checks currently implemented by this plugin.\n\n### DM001\n\n`RemoveField` operation should be wrapped in `SeparateDatabaseAndState`. \n\nSuch an operation should be run in two separate steps, using `SeparateDatabaseAndState`, otherwise it is not backwards compatible.\n\n* Step 1: remove the field from the model and code. For foreign key fields, the foreign key constraint should also be dropped.\n* Step 2: remove the column from the database.\n\n#### Bad\n\n```python\nclass Migration(migrations.Migration):\n    operations = [\n        migrations.RemoveField(\n            model_name="order",\n            name="total",\n        ),\n    ]\n```\n\n#### Good\n\n```python\nclass Migration(migrations.Migration):\n    operations = [\n        migrations.SeparateDatabaseAndState(\n            state_operations=[\n                migrations.RemoveField(\n                    model_name="order",\n                    name="total",\n                ),\n            ],\n        ),\n    ]\n```\n\n',
    'author': 'Bruno Alla',
    'author_email': 'bruno.alla@festicket.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/browniebroke/flake8-django-migrations',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
