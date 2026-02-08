from typing import List, Dict, Tuple, Any, Callable
from enum import Enum
import inspect
import functools
from  datetime import datetime, timedelta


#--------------------------------------
#   Functionデコレータ
#--------------------------------------
def deco_func(deco_arg1, *deco_args, **deco_kwargs):
    def __wrapper(func:Callable) -> Callable:
        @functools.wraps(func)
        def __inner(*args, **kwargs) -> Any:
            # 実行
            my_name = "deco_func" 
            print(f"[{my_name}] -- {func}")
            print(f"[{my_name}]   deco_arg1   = {deco_arg1}")
            print(f"[{my_name}]   deco_args   = {deco_args}")
            print(f"[{my_name}]   deco_kwargs = {deco_kwargs}")
            ret:Any = func(*args, **kwargs)
            print(f"[{my_name}]   --> {ret}")

            # 返却
            return ret

        return __inner
    return __wrapper


#--------------------------------------
#   サンプル
#--------------------------------------
CONST_KW2 = "KW2"

@deco_func("a", "b", "c", kw1="KW1", kw2=CONST_KW2)
def test_func_1(*args, **kwargs):
    my_name = "test_func_1" 
    print(f"[{my_name}] -- {my_name}")
    print(f"[{my_name}]   args   = {args}")
    print(f"[{my_name}]   kwargs = {kwargs}")
    return len(args) + len(kwargs)



if __name__ == '__main__':

    print("**************")
    ret = test_func_1()

    print("**************")
    ret = test_func_1(1, 2, 3, a="A", b="B")



