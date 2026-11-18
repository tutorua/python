from random import randint
from typing import TextIO

log_file: TextIO = open('app.log', 'a')
print(f'Roll: {randint(1, 10)}', file=log_file)
