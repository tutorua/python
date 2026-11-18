from typing import Any


def print_pro(*args: Any, **kwargs: Any) -> None:
    print(*args, **kwargs)


people: list[Any] = ['Bob', 'Alice', 'Charlie']
print(people)
print(*people)
print(*people, sep=', ')
print(*people, sep='-')
print(*people, sep=' -> ', end='.\n')
print(*people, sep=' = ')