# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymathalgos']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymathalgos',
    'version': '0.0.2.0',
    'description': '',
    'long_description': '# PyMathAlgoS\n\n## 1. Установка\n\n```bash\n$ pip install pymathalgos\n```\n\n## 2. Функционал\n\n### Простая арифметика\n\nФункция вычисления факториала:\n\n```python\nimport pymathalgos\nprint(pymathalgos.factorial(2))\t # 1\nprint(pymathalgos.factorial(-1)) # ArithmeticError: argument value must be bigger then zero!\n```\n\nФункции для вычисления большего, меньшего числа из аргументов, а также суммы аргументов:\n\n```python\nimport pymathalgos\n\nprint(pymathalgos._min(2, 8, 1)) # 1\nprint(pymathalgos._max(2, 8, 9)) # 9\nprint(pymathalgos._sum(1, 2, 3)) # 6\n\n```\n\n### Геометрия\n\nЗдесь вы можете увидеть готовые функции для геометрии\n\n\nЗдесь просто функции из тригонометрии:\n```python\nimport pymathalgos\nimport pymathalgos.geometry as geometry\n\nprint(geometry.sin())\nprint(geometry.cos())\n\n# Функции tan() и tg(), а также подобные функции означают одно и тоже \nprint(geometry.tan())\nprint(geometry.tg())\n\nprint(geometry.asin())\nprint(geometry.acos())\nprint(geometry.atan())\n\nprint(geometry.sinh())\nprint(geometry.cosh())\nprint(geometry.tanh())\n\nprint(geometry.asinh())\nprint(geometry.acosh())\nprint(geometry.atanh())\n```\n\nЕсли вы хотите узнать синус от градусов, а не от радиан\nесть простая функция sin_d(degrees).\n\n```python\nimport pymathalgos\n# Эти две строки кода означают одно и тоже\nprint(pymathalgos.sin_r(pymathalgos.to_radians(90)))\nprint(pymathalgos.sin_d(90))\n```',
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
