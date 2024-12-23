# Python Decorators - Example 1.1
# https://www.youtube.com/watch?v=r7Dtus7N4pI
# Python Decorators in 15 Minutes

def f1(func):
	def wrapper(*args, **kwargs):
		print("Started")
		val = func(*args, **kwargs)
		print("Ended")
		return val
		
	return wrapper
	

@f1
def f(a, b=9):
	print(a, b)
	

@f1
def add(x, y):
	return x + y
	
	
f("Hi!")
print(add(4,5))
