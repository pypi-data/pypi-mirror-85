# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycurd',
 'pycurd.crud',
 'pycurd.crud.ext',
 'pycurd.pydantic_ext',
 'pycurd.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyPika>=0.42.1',
 'multidict>=4.5,<6.0',
 'pydantic>=1.6.1',
 'typing_extensions>=3.6.5']

setup_kwargs = {
    'name': 'pycurd',
    'version': '0.1.18',
    'description': 'A common crud framework for web.',
    'long_description': '# pycrud\n\n[![codecov](https://codecov.io/gh/fy0/pycrud/branch/master/graph/badge.svg)](https://codecov.io/gh/fy0/pycrud)\n\nA common crud framework for web.\n\nFeatures:\n\n* Generate query by json\n\n* Role based permission system\n\n* Easy to bind\n\n* Tested\n\n\n### Examples:\n\n#### Define\n\n```python\nfrom typing import Optional\n\nfrom playhouse.db_url import connect\nfrom pycurd.crud.ext.peewee_crud import PeeweeCrud\nfrom pycurd.types import RecordMapping\n\nclass User(RecordMapping):\n    id: Optional[int]\n    nickname: str\n    username: str\n    password: str = \'password\'\n\n\ndb = connect("sqlite:///:memory:")\n\nc = PeeweeCrud(None, {\n    User: \'users\'\n}, db)\n\n```\n\n#### Create\n\n```python\nfrom pycurd.values import ValuesToWrite\n\nv = ValuesToWrite({\'nickname\': \'wwww\', \'username\': \'u2\'})\nlst = await c.insert_many(User, [v])\n\nprint(lst)\n```\n\n#### Read\n\n```python\nfrom pycurd.query import QueryInfo\n\nlst = await c.get_list(QueryInfo.from_json(User, {\n    \'id.eq\': 1\n}))\n\nprint([x.to_dict() for x in lst])\n```\n\n#### Update\n\n```python\nfrom pycurd.query import QueryInfo\nfrom pycurd.values import ValuesToWrite\n\nv = ValuesToWrite({\'nickname\': \'bbb\', \'username\': \'u2\'})\nlst = await c.update(QueryInfo.from_json(User, {\n    \'id.in\': [1,2,3]\n}), v)\n\nprint(lst)\n```\n\n#### Delete\n\n```python\nfrom pycurd.query import QueryInfo\n\nlst = await c.delete(QueryInfo.from_json(User, {\n    \'id.in\': [1,2,3]\n}))\n\nprint(lst)\n```\n\n\n### Operators\n\n| type | operator | text |\n| ---- | -------- | ---- |\n| compare | EQ | (\'eq\', \'==\') |\n| compare | NE | (\'ne\', \'!=\') |\n| compare | LT | (\'lt\', \'<\') |\n| compare | LE | (\'le\', \'<=\') |\n| compare | GE | (\'ge\', \'>=\') |\n| compare | GT | (\'gt\', \'>\') |\n| relation | IN | (\'in\',) |\n| relation | NOT_IN | (\'notin\', \'not in\') |\n| relation | IS | (\'is\',) |\n| relation | IS_NOT | (\'isnot\', \'is not\') |\n| relation | PREFIX | (\'prefix\',) |\n| relation | CONTAINS | (\'contains\',) |\n| logic | AND | (\'and\',) |\n| logic | OR | (\'or\',) |\n\n\n```json5\n// usage:\n{\n  \'time.ge\': 1,\n  \'$or\': {\n    \'id.in\': [1, 2, 3],\n    \'$and\': {\n      \'time.ge\': 100,\n      \'time.le\': 500,\n    }\n  }\n}\n```\n',
    'author': 'fy',
    'author_email': 'fy0748@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fy0/pycrud',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.9',
}


setup(**setup_kwargs)
