def get_user_by_id(user_id):
   assert type(user_id) is int, 'user_id must be integer'
   print('Searching...')

get_user_by_id(4267)
# Searching...

get_user_by_id('foo')
# AssertionError: user_id must be integer
