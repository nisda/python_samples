from typing import Callable
from time import sleep
import random
from datetime import datetime, timedelta

def retry_wrapper(
        func:Callable,
        count:int=0,
        interval:int = 0,
        jitter:int=0,
        backoff:int=0
        ):

    for i in range(0, count+1):
        try:
            print(f"[{i}] {datetime.now()}")
            ret = func()
            return ret
        except Exception as e:
            if i < count:
                sleep(interval)
                sleep(jitter * random.random())
                sleep(backoff * 2 ** i)
            else:
                raise e






def time_compare(target_time:datetime) -> bool:
    if datetime.now() <= target_time:
        raise ValueError("not reach!")
    else:
        return True


if __name__ == '__main__':

    patterns = [
        {"count": 3, "interval": 1, "jitter": 5},
        {"count": 3, "interval": 0, "jitter": 0, "backoff": 2},
    ]

    func:Callable = lambda: time_compare(target_time)
    for p in patterns:
        try:
            target_time:datetime = datetime.now() + timedelta(seconds=10)
            print(f"-- {p}")
            ret = retry_wrapper(func=func, **p)
            print(ret)
        except Exception as e:
            print(str(e))


