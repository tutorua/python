from datetime import datetime

now = '{:%Y-%m-%d %H:%M}'.format(datetime(2001, 2, 3, 4, 5))
print(now)

dt = datetime(2001, 2, 3, 4, 5)
new = '{:{dfmt} {tfmt}}'.format(dt, dfmt='%Y-%m-%d', tfmt='%H:%M')
print(new)
