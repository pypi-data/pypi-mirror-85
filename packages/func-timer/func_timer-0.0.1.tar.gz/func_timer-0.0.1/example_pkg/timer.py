import time
from functools import wraps


def func_timer(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        time_start = time.time()
        res = func(*args, **kwargs)
        run_time = time.time() - time_start
        print('运行', run_time * 1000, '毫秒')
        return res
    return wrap