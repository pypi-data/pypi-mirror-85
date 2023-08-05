# PyMathAlgoS

## 1. Installation

```bash
$ pip install pymathalgos
```

## 2. Functions

If you want to get the factorial value there is a factorial function:

```python
import pymathalgos
print(pymathalgos.factorial(-1))
```

The result is:

```
ArithmeticError: argument value must be bigger then zero!
```

```python
import pymathalgos
# These 2 lines of code are means the same thinks
print(pymathalgos.sin_r(pymathalgos.to_radians(90)))
print(pymathalgos.sin_d(90))
```