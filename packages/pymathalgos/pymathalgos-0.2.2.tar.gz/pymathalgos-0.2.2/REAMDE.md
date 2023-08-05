# PyMathAlgoS

## 1. Установка

Настоятельно рекомендуется перед установкой данного пакета установить модуль numba (отдельно), так как его декортаторы очень часто используются для того, чтобы ускорить процесс вычисления и нахождения результата

```bash
$ pip install numba
```
А потом уже установить этот модуль
```bash
$ pip install pymathalgos
```

## 2. Функционал

### Простая арифметика

Функция вычисления факториала:

```python
import pymathalgos
print(pymathalgos.factorial(2))	 # 1
print(pymathalgos.factorial(-1)) # ArithmeticError: argument value must be bigger then zero!
```

Функции для вычисления большего, меньшего числа из аргументов, а также суммы аргументов:

```python
import pymathalgos

print(pymathalgos._min(2, 8, 1)) # 1
print(pymathalgos._max(2, 8, 9)) # 9
print(pymathalgos._sum(1, 2, 3)) # 6
```

Функции округления
```python
import pymathalgos

print(pymathalgos.ceil(10.4))   # округление до ближайшего большего числа
print(pymathalgos.floor(18.7))  # округление вниз
```

Можно получить знак числа
```python
import pymathalgos
print(pymathalgos.get_sing(90))     # "+"
print(pymathalgos.get_sing(-90))    # "-"
print(pymathalgos.get_sing(0))      # None
```

Можно найти сумму цифр в какой-либо системе счиления
```python
import pymathalgos
print(pymathalgos.digits_sum(123)) # здесь сумма вычисляется в десятичной системе счисления
print(pymathalgos.digits_sum(100, 2)) # здесь вычисляется в двоичной системе счисления
```

Можно найти значение логарифма:
```python
import pymathalgos
print(pymathalgos.log(10))      # здесь вычисляется десятичный логарифм
print(pymathalgos.loge(10))     # здесь вычисляется натуральный логарифм
print(pymathalgos.log(30, 2))   # здесь вычисляется логарифм по основанию 2
```

### Константы


Просто константы:
```python
import pymathalgos.
print(pymathalgos.PI)		# число пи
print(pymathalgos.E)		# число е
print(pymathalgos.FI)		# число фи
print(pymathalgos.NULL)		# 0
print(pymathalgos.TAU)		# число тау: число пи * 2
print(pymathalgos.SQRT2)	# корень из 2
print(pymathalgos.SQRT3)	# корень из 3
```

### Геометрия

Здесь вы можете увидеть готовые функции для геометрии

Здесь просто функции из тригонометрии:
```python
import pymathalgos.geometry as geometry

n = 90

#					Можно вычислять градусы или радианы
#						|
print(geometry.sin("degrees", n))
print(geometry.cos("degrees", n))

# Функции tan() и tg(), а также подобные функции означают одно и тоже 
print(geometry.tan("degrees", n))
print(geometry.tg("degrees", n))

print(geometry.asin("degrees", n))
print(geometry.acos("radians", 1))
print(geometry.atan("degrees", n))

print(geometry.sinh("degrees", n))
print(geometry.cosh("degrees", n))
print(geometry.tanh("radians", pymathalgos.PI))

print(geometry.asinh("degrees", n))
print(geometry.acosh("degrees", n))
print(geometry.atanh("degrees", n))
```

Можно получить расстояние от одной точки до другой
```python
import pymathalgos.geometry as geometry
pos1 = (50, 40)
pos2 = (30, 20)
print(geometry.point_distance(pos1, pos2))
```

Можно найти гипотенузу в прямоугольном треугольнике
```python
import pymathalgos.geometry as geometry
a, b = 2, 3
print(geometry.hypot(a, b))
```

