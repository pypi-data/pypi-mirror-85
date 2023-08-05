# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_pagination', 'fastapi_pagination.ext']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.61.2,<0.62.0', 'pydantic>=1.7.2,<2.0.0']

extras_require = \
{'databases': ['databases>=0.4.0,<0.5.0'],
 'gino': ['gino>=1.0.1,<2.0.0',
          'SQLAlchemy>=1.3.20,<2.0.0',
          'sqlalchemy-stubs>=0.3,<0.4'],
 'orm': ['orm>=0.1.5,<0.2.0'],
 'sqlalchemy': ['SQLAlchemy>=1.3.20,<2.0.0', 'sqlalchemy-stubs>=0.3,<0.4']}

setup_kwargs = {
    'name': 'fastapi-pagination',
    'version': '0.3.1',
    'description': 'FastAPI pagination',
    'long_description': "# FastAPI Pagination\n\n## Installation\n\nBasic version\n```bash\npip install fastapi-pagination\n```\n\n`Gino` integration\n```bash\npip install fastapi-pagination[gino]\n```\n\n`SQLAlchemy` integration\n```bash\npip install fastapi-pagination[sqlalchemy]\n```\n\n## Example\n\n```python\nfrom fastapi import FastAPI, Depends\nfrom pydantic import BaseModel\n\nfrom fastapi_pagination import PaginationParams, Page\nfrom fastapi_pagination.paginator import paginate\n\napp = FastAPI()\n\nclass User(BaseModel):\n    name: str\n    surname: str\n\nusers = [\n    User(name='Yurii', surname='Karabas'),\n    # ...\n]\n\n@app.get('/users', response_model=Page[User])\nasync def get_users(params: PaginationParams = Depends()):\n    return paginate(users, params)\n```\n",
    'author': 'Yurii Karabas',
    'author_email': '1998uriyyo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/uriyyo/fastapi-pagination',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
