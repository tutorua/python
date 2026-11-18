from datetime import datetime
from zoneinfo import ZoneInfo

now = '{:%Y-%m-%d %H:%M}'.format(datetime(2001, 2, 3, 4, 5))
print(now)

dt = datetime(2001, 2, 3, 4, 5)
new = '{:{dfmt} {tfmt}}'.format(dt, dfmt='%Y-%m-%d', tfmt='%H:%M')
print(new)

# strftime
now = datetime.now()
simple_date = now.strftime("%d.%m.%Y")
print(f"Today is: {simple_date}")

fancy_date = now.strftime("%A, %d %B")
print(f"Date is: {fancy_date}")

log_time = now.strftime("%H:%M:%S")
print(f"Event time is: {log_time}")


# correct way

# BAD
now = datetime.now()

print(now.isoformat())
# 2025-10-21T15:03:07.332217

# GOOD
now = datetime.now(tz=ZoneInfo("UTC"))
print(now.isoformat())
# 2025-10-21T12:04:22.573590+00:00

print(now.astimezone().isoformat())
# 2025-10-21T15:04:22.573590+03:00
