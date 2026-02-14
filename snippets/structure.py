def is_an_adult(age: int, has_id: bool) -> bool:
    return age >= 21 and has_id


def is_bob(name: str) -> bool:
    return name.lower() == 'bob'


def enter_club(name: str, age: int, has_id:bool) -> None:
    if is_bob(name):
        print('Get out of here Bob')
        return
    
    if is_an_adult(age, has_id):
        print('You may enter the club.')
    else:
        print('You may NOT enter the club.')


def bye() -> None:
    print('Bye, World!')


def greet() -> None:
    print('Hello, World!')


def main() -> None:
    greet()
    age_ok_1: int = 29
    age_ok_2: int = 21
    age_ok_3: int = 31
    age_notok: int = 19.1 #  mypy .\structure.py  # to get incompatible type assignmet notification
    enter_club('Bob', age_ok_1, has_id=True)
    enter_club('James', age_ok_2, has_id=True)
    enter_club('Sandra', age_ok_3, has_id=False)
    enter_club('Mario', age_notok, has_id=True)
    bye()


if __name__ == '__main__':
    main()
