def function(value, *args, **kwargs):
   print(value)
   print(args)
   print(kwargs)

function(42, 'text', 12345, [1, 2, 3], pi=3.14, name='Adrian')

# 42
# ('text', 12345, [1, 2, 3])
# {'pi': 3.14, 'name': 'Adrian}
