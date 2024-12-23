# Python Decorators - Example 1
# https://www.youtube.com/watch?v=r7Dtus7N4pI
# Python Decorators in 15 Minutes

def f1(func):
	def wrapper(*args, **kwargs):
		print("Started")
		func(*args, **kwargs)
		print("Ended")
		
	return wrapper
	

@f1
def f(a, b=9):
	print(a, b)
	
	
f("Hi!")