from typing import List, Dict
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback
from random import randint
from time import sleep
from datetime import datetime



def sleeper(id:int, sec:int):
    print(f"[id={id}, wait={sec}] start - {datetime.now().isoformat()}")
    sleep(sec)
    print(f"[id={id}, wait={sec}] end   - {datetime.now().isoformat()}")
    return (id, sec)

if __name__ == '__main__':
    inputs:List[int] = [
        randint(1, 10)
        for i in range(0, 5)
    ]


    results = {}
    with ThreadPoolExecutor(max_workers=3) as executer:
        tasks:dict = {}
        # 処理実行
        for idx in range(0, len(inputs)):
            tasks[idx] = executer.submit(sleeper, id=idx, sec=inputs[idx])


        # # 結果取得。上から順番に完了を待ちながら取得 -> それなら executer.map でも同じな気がする。
        # for id, process in processes.items():
        #     try:
        #         results[id] = process.result()
        #     except Exception as e:
        #         t = list(traceback.TracebackException.from_exception(e).format())
        #         results[id] = str(e)

        # 完了したタスクから順次結果を取得
        for future in as_completed(tasks.values()):
            result = future.result()  # 結果を取得
            print(result)


    print(results)

