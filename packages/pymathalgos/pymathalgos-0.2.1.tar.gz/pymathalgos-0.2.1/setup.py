# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymathalgos']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymathalgos',
    'version': '0.2.1',
    'description': '',
    'long_description': '# PyMathAlgoS\n\n## 1. Установка\n\n```bash\n$ pip install pymathalgos\n```\n\n## 2. Функционал\n\n### Простая арифметика\n\nФункция вычисления факториала:\n\n```python\nimport pymathalgos\nprint(pymathalgos.factorial(2))\t # 1\nprint(pymathalgos.factorial(-1)) # ArithmeticError: argument value must be bigger then zero!\n```\n\nФункции для вычисления большего, меньшего числа из аргументов, а также суммы аргументов:\n\n```python\nimport pymathalgos\n\nprint(pymathalgos._min(2, 8, 1)) # 1\nprint(pymathalgos._max(2, 8, 9)) # 9\nprint(pymathalgos._sum(1, 2, 3)) # 6\n\n```\n\n### Геометрия\n\nЗдесь вы можете увидеть готовые функции для геометрии\n\n\nПросто константы:\n```python\nimport pymathalgos\nprint(pymathalgos.PI)\t\t# число пи\nprint(pymathalgos.E)\t\t# число е\nprint(pymathalgos.FI)\t\t# число фи\nprint(pymathalgos.NULL)\t\t# 0\nprint(pymathalgos.TAU)\t\t# число тау: число пи * 2\nprint(pymathalgos.SQRT2)\t# корень из 2\nprint(pymathalgos.SQRT3)\t# корень из 3\n```\n\nЗдесь просто функции из тригонометрии:\n```python\nimport pymathalgos\nimport pymathalgos.geometry as geometry\n\nn = 90\n\n#\t\t\t\t\tМожно вычислять градусы или радианы\n#\t\t\t\t\t\t|\nprint(geometry.sin("degrees", n))\nprint(geometry.cos("degrees", n))\n\n# Функции tan() и tg(), а также подобные функции означают одно и тоже \nprint(geometry.tan("degrees", n))\nprint(geometry.tg("degrees", n))\n\nprint(geometry.asin("degrees", n))\nprint(geometry.acos("radians", 1))\nprint(geometry.atan("degrees", n))\n\nprint(geometry.sinh("degrees", n))\nprint(geometry.cosh("degrees", n))\nprint(geometry.tanh("radians", pymathalgos.PI))\n\nprint(geometry.asinh("degrees", n))\nprint(geometry.acosh("degrees", n))\nprint(geometry.atanh("degrees", n))\n```\n\nЕсли вы хотите узнать синус от градусов, а не от радиан\nесть простая функция sin_d(degrees).\n\n```python\nimport pymathalgos\n# Эти две строки кода означают одно и тоже\nprint(pymathalgos.sin_r(pymathalgos.to_radians(90)))\nprint(pymathalgos.sin_d(90))\n```\n\nМожно получить расстояние от одной точки до другой\n```python\nimport pymathalgos\npos1 = (50, 40)\npos2 = (30, 20)\nprint(pymathalgos.point_distance(pos1, pos2))\n```\n',
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
