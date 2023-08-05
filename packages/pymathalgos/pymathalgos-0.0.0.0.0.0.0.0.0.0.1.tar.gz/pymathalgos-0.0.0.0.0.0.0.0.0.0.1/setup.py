# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymathalgos']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymathalgos',
    'version': '0.0.0.0.0.0.0.0.0.0.1',
    'description': '',
    'long_description': '# PyMathAlgoS\n\n## 1. Установка\n\n```bash\n$ pip install pymathalgos\n```\n\n## 2. Функционал\n\n### Simple arithmetic\n\nФункция вычисления факториала:\n\n```python\nimport pymathalgos\nprint(pymathalgos.factorial(2))\nprint(pymathalgos.factorial(-1))\n```\n\nРезультат:\n\n```\n1\nArithmeticError: argument value must be bigger then zero!\n```\n\n### Геометрия\n\nЗдесь вы можете увидеть готовые функции для геометрии\n\n\nЕсли вы хотите узнать синус от градусов, а не от радиан\nесть простая функция sin_d(degrees).\n```python\nimport pymathalgos\n# These 2 lines of code are means the same thinks\nprint(pymathalgos.sin_r(pymathalgos.to_radians(90)))\nprint(pymathalgos.sin_d(90))\n```',
    'author': 'Adi58816',
    'author_email': 'adisalimgereev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
