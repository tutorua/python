import os
from pathlib import Path
from datetime import datetime

now = '{:%Y-%m-%d %H:%M}'.format(datetime(2001, 2, 3, 4, 5))
print(now)

dt = datetime(2001, 2, 3, 4, 5)
new = '{:{dfmt} {tfmt}}'.format(dt, dfmt='%Y-%m-%d', tfmt='%H:%M')
print(new)

timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
PROJECT_ROOT = Path(__file__).parent.parent
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots" / timestamp
print(SCREENSHOTS_DIR)
if not SCREENSHOTS_DIR.exists():
    print("SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)")