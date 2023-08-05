# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymathalgos']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymathalgos',
    'version': '0.2.2',
    'description': '',
    'long_description': '# PyMathAlgoS\n\n## 1. Установка\n\nНастоятельно рекомендуется перед установкой данного пакета установить модуль numba (отдельно), так как его декортаторы очень часто используются для того, чтобы ускорить процесс вычисления и нахождения результата\n\n```bash\n$ pip install numba\n```\nА потом уже установить этот модуль\n```bash\n$ pip install pymathalgos\n```\n\n## 2. Функционал\n\n### Простая арифметика\n\nФункция вычисления факториала:\n\n```python\nimport pymathalgos\nprint(pymathalgos.factorial(2))\t # 1\nprint(pymathalgos.factorial(-1)) # ArithmeticError: argument value must be bigger then zero!\n```\n\nФункции для вычисления большего, меньшего числа из аргументов, а также суммы аргументов:\n\n```python\nimport pymathalgos\n\nprint(pymathalgos._min(2, 8, 1)) # 1\nprint(pymathalgos._max(2, 8, 9)) # 9\nprint(pymathalgos._sum(1, 2, 3)) # 6\n```\n\nФункции округления\n```python\nimport pymathalgos\n\nprint(pymathalgos.ceil(10.4))   # округление до ближайшего большего числа\nprint(pymathalgos.floor(18.7))  # округление вниз\n```\n\nМожно получить знак числа\n```python\nimport pymathalgos\nprint(pymathalgos.get_sing(90))     # "+"\nprint(pymathalgos.get_sing(-90))    # "-"\nprint(pymathalgos.get_sing(0))      # None\n```\n\nМожно найти сумму цифр в какой-либо системе счиления\n```python\nimport pymathalgos\nprint(pymathalgos.digits_sum(123)) # здесь сумма вычисляется в десятичной системе счисления\nprint(pymathalgos.digits_sum(100, 2)) # здесь вычисляется в двоичной системе счисления\n```\n\nМожно найти значение логарифма:\n```python\nimport pymathalgos\nprint(pymathalgos.log(10))      # здесь вычисляется десятичный логарифм\nprint(pymathalgos.loge(10))     # здесь вычисляется натуральный логарифм\nprint(pymathalgos.log(30, 2))   # здесь вычисляется логарифм по основанию 2\n```\n\n### Константы\n\n\nПросто константы:\n```python\nimport pymathalgos.\nprint(pymathalgos.PI)\t\t# число пи\nprint(pymathalgos.E)\t\t# число е\nprint(pymathalgos.FI)\t\t# число фи\nprint(pymathalgos.NULL)\t\t# 0\nprint(pymathalgos.TAU)\t\t# число тау: число пи * 2\nprint(pymathalgos.SQRT2)\t# корень из 2\nprint(pymathalgos.SQRT3)\t# корень из 3\n```\n\n### Геометрия\n\nЗдесь вы можете увидеть готовые функции для геометрии\n\nЗдесь просто функции из тригонометрии:\n```python\nimport pymathalgos.geometry as geometry\n\nn = 90\n\n#\t\t\t\t\tМожно вычислять градусы или радианы\n#\t\t\t\t\t\t|\nprint(geometry.sin("degrees", n))\nprint(geometry.cos("degrees", n))\n\n# Функции tan() и tg(), а также подобные функции означают одно и тоже \nprint(geometry.tan("degrees", n))\nprint(geometry.tg("degrees", n))\n\nprint(geometry.asin("degrees", n))\nprint(geometry.acos("radians", 1))\nprint(geometry.atan("degrees", n))\n\nprint(geometry.sinh("degrees", n))\nprint(geometry.cosh("degrees", n))\nprint(geometry.tanh("radians", pymathalgos.PI))\n\nprint(geometry.asinh("degrees", n))\nprint(geometry.acosh("degrees", n))\nprint(geometry.atanh("degrees", n))\n```\n\nМожно получить расстояние от одной точки до другой\n```python\nimport pymathalgos.geometry as geometry\npos1 = (50, 40)\npos2 = (30, 20)\nprint(geometry.point_distance(pos1, pos2))\n```\n\nМожно найти гипотенузу в прямоугольном треугольнике\n```python\nimport pymathalgos.geometry as geometry\na, b = 2, 3\nprint(geometry.hypot(a, b))\n```\n\n',
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
