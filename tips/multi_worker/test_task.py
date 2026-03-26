from typing import Dict, Callable
from time import sleep
from random import randint
from datetime import datetime
from pprint import pprint

from libs.multi_worker import Task
import types

def worker_sleep(id:str, sec:int) -> str:
    dt_format = "%H:%M:%S"

    # 開始時刻を表示
    begin_at:datetime = datetime.now()
    print(f"[{id}] begin: {begin_at.strftime(dt_format)}")

    # Sleep
    sleep(sec)

    # 終了時刻を表示
    end_at:datetime = datetime.now()
    print(f"[{id}] end  : {end_at.strftime(dt_format)}")

    # 戻り値（開始 - 終了 / 経過時間）
    return f"{begin_at.strftime(dt_format)} - {end_at.strftime(dt_format)} / {(end_at-begin_at).seconds} sec"


if __name__ == '__main__':

    func = worker_sleep
    print(type(func))
    print(func.__name__)
    print(isinstance(func, types.LambdaType))
    print(isinstance(func, Callable))

    func = lambda: worker_sleep(ud="A", sec=2)
    print(type(func))
    print(func.__name__)
    print(isinstance(func, types.LambdaType))
    print(isinstance(func, Callable))

    # task = Task(worker_sleep, "ID-001", sec=5)
    # ret = task()
    # print(ret)


