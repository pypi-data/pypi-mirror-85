# PyMathAlgoS

## 1. Установка

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

### Геометрия

Здесь вы можете увидеть готовые функции для геометрии


Просто константы:
```python
import pymathalgos
print(pymathalgos.PI)		# число пи
print(pymathalgos.E)		# число е
print(pymathalgos.FI)		# число фи
print(pymathalgos.NULL)		# 0
print(pymathalgos.TAU)		# число тау: число пи * 2
print(pymathalgos.SQRT2)	# корень из 2
print(pymathalgos.SQRT3)	# корень из 3
```

Здесь просто функции из тригонометрии:
```python
import pymathalgos
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

Если вы хотите узнать синус от градусов, а не от радиан
есть простая функция sin_d(degrees).

```python
import pymathalgos
# Эти две строки кода означают одно и тоже
print(pymathalgos.sin_r(pymathalgos.to_radians(90)))
print(pymathalgos.sin_d(90))
```

Можно получить расстояние от одной точки до другой
```python
import pymathalgos
pos1 = (50, 40)
pos2 = (30, 20)
print(pymathalgos.point_distance(pos1, pos2))
```
