# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crudapi',
 'crudapi.core',
 'crudapi.models',
 'crudapi.routers',
 'crudapi.services']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.20,<2.0.0',
 'fastapi>=0.61.1,<0.62.0',
 'pydantic-sqlalchemy>=0.0.7,<0.0.8']

setup_kwargs = {
    'name': 'crudapi',
    'version': '0.1.1',
    'description': 'The easiest way to create your Restful CRUD APIs',
    'long_description': '# CrudAPI: The easiest way to create your CRUD APIs\n\n[![codecov](https://codecov.io/gh/unmateo/crudapi/branch/develop/graph/badge.svg?token=RAKVPGHZU5)](https://codecov.io/gh/unmateo/crudapi)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI version](https://badge.fury.io/py/crudapi.svg)](https://badge.fury.io/py/crudapi)\n\nCombining the power of FastAPI, Pydantic and SQLAlchemy, you\'ll only have to care about modeling your data and we\'ll take care of building up a RESTful API for it.\n\n```python\nfrom crudapi import CrudAPI\nfrom crudapi.models.api import BaseAPI\nfrom crudapi.models.orm import BaseORM\n\nfrom sqlalchemy import Column\nfrom sqlalchemy import String\n\n\nclass BookORM(BaseORM):\n\n    __tablename__ = "books"\n    title = Column(String, nullable=False)\n\n\ncrud = CrudAPI(orm_model=BookORM)\n\n```\n\nyou\'ll get, out of the box, a working _crudapi_ with all these working REST endpoints:\n\n- GET: /books\n- POST: /books\n- GET: /books/\\<id>\n- PUT: /books/\\<id>\n- PATCH: /books/\\<id>\n- DELETE: /books/\\<id>\n\nand because CrudAPI subclasses FastAPI you\'ll also get all the incredible features of this wonderful library.\n\n---\n\n## Development\n\nWe use Poetry for packaging and dependency management:\n\n`poetry install`\n\n`poetry shell`\n\nWe use Pytest for testing:\n\n`pytest`\n\nYou can start a testing server running:\n\n`uvicorn tests.server:app --reload `\n',
    'author': 'Mateo Harfuch',
    'author_email': 'mharfuch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/unmateo/crudapi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
