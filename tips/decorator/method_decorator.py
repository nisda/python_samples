from typing import List, Dict, Tuple, Any, Callable
from enum import Enum
import inspect
import functools
from  datetime import datetime, timedelta


#--------------------------------------
#   Methodデコレータ
#--------------------------------------
def deco_method(deco_arg1, *deco_args, **deco_kwargs):
    def __wrapper(func:Callable) -> Callable:
        @functools.wraps(func)
        def __inner(self, *args, **kwargs) -> Any:

            # クラスのメンバ変数を取得
            deco_arg1_value = getattr(self, deco_arg1)

            # 実行
            my_name = "deco_func" 
            print(f"[{my_name}] -- {func}")
            print(f"[{my_name}]   deco_arg1   = {deco_arg1_value}")
            print(f"[{my_name}]   deco_args   = {deco_args}")
            print(f"[{my_name}]   deco_kwargs = {deco_kwargs}")
            ret:Any = func(self, *args, **kwargs)
            print(f"[{my_name}]   --> {ret}")

            # 返却
            return ret

        return __inner
    return __wrapper



#--------------------------------------
#   テスト用クラス
#--------------------------------------
class TestClass:
    _config_a:Any

    def __init__(self, config_a):
        self._config_a = config_a

    # メンバ変数を decorator に渡すには、変数名を渡して中で getattr するしか手段がなさそう。
    @deco_method("_config_a", 1, add_a="ADD_A")
    def squared(self, value=10):
        return value ** 2


#--------------------------------------
#   サンプル
#--------------------------------------
if __name__ == '__main__':

    print("**************")
    test_obj = TestClass(config_a="CONF_A1")
    ret = test_obj.squared(value=3)
    print(f"[main] ret = {ret}")

    print("**************")
    test_obj = TestClass(config_a="CONF_A2")
    ret = test_obj.squared(value=4)
    print(f"[main] ret = {ret}")



