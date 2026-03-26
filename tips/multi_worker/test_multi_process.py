from typing import Dict, List
from time import sleep
from random import randint
from datetime import datetime
from pprint import pprint

from libs.multi_worker import MultiProcessWorker, Task


def worker_sleep(id:str, sec:int, **kwargs) -> str:
    """テスト用function"""

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
    return f"[{id}] {begin_at.strftime(dt_format)} - {end_at.strftime(dt_format)} / {(end_at-begin_at).seconds} sec"


if __name__ == '__main__':

    tasks:Dict[str, Task] = {
        f"{i:03}": Task(worker_sleep, f"{i:03}", sec=randint(1, 5))
        for i in range(0, 5)
    }
    ret = MultiProcessWorker.execute(tasks, max_workers=3)
    print("-----------------")
    pprint(ret)

    print("**********************************")
    tasks:List[Task] = [
        Task(worker_sleep, f"{i:03}", sec=randint(1, 5))
        for i in range(0, 5)
    ]
    ret = MultiProcessWorker.execute(tasks, max_workers=3)
    print("-----------------")
    pprint(ret)
