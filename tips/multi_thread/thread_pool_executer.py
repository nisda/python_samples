from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor
import traceback
from random import randint
from time import sleep
from datetime import datetime

def sleeper(id:int, sec:int):
    print(f"[id={id}, wait={sec}] start - {datetime.now().isoformat()}")
    sleep(sec)
    print(f"[id={id}, wait={sec}] end   - {datetime.now().isoformat()}")
    return sec

if __name__ == '__main__':
    inputs:List[int] = [
        randint(1, 5)
        for i in range(0, 5)
    ]


    results = {}
    with ThreadPoolExecutor() as executer:
        processes:dict = {}
        # 処理実行
        for idx in range(0, len(inputs)):
            processes[idx] = executer.submit(sleeper, id=idx, sec=inputs[idx]).result()
        # 結果取得
        for id, process in processes.items():
            try:
                results[id] = process.result()
            except Exception as e:
                t = list(traceback.TracebackException.from_exception(e).format())
                results[id] = str(e)

    print(results)

