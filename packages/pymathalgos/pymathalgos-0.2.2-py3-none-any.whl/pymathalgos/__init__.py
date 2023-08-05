import math



def factorial(n: int) -> int:
	if (n < 0):
		raise ArithmeticError("argument value must be bigger then zero!")
	if (n < 2):
		return 1
	total = 1
	for i in range(1, n + 1):
		total *= i
	return total


def _sum(*args):	return sum(args)
def _max(*args):	return max(args)
def _min(*args):	return min(args)
