# Реализовать параметризованный декоратор, который будет повторять выполнение фунции
# указанное количество раз при возникновении ошибки. При возникновении ошибки 
# необходимо выводить на печатьназвание класса возникшей ошибки. При удачном выполнении 
# вывести на печать "ок". Если повторов не осталось нужно напечатать название 
# класса ошибки с префиксом "final"
# 
from functools import wraps
from typing import Callable

error_counter_success = 0

def retry_on_exception(retries: int):
    def wrapper(func: Callable):
        @wraps(func)
        def inner(*args, **kwargs):
            func()
            nonlocal retries
            while retries > 0:
                try:
                    result = func(*args, **kwargs)
                    print("ok")
                    return result
                except Exception as e:
                    if retries != 1:
                        print(type(e).__name__)
                        retries -= 1
                    else:
                        print(f"final {type(e).__name__}")
                        return None
        return inner
    return wrapper


@retry_on_exception(retries=3)
def test_success_after_one_fail():
    global error_counter_success
    if error_counter_success < 2:
        error_counter_success += 1
        raise ValueError
    return "Success after fail!"

@retry_on_exception(retries=3)
def test_fail_all_attempts():
    raise AttributeError

@retry_on_exception(retries=3)
def test_success_immediately():
    return "Success Immediately!"
