# 参考: https://qiita.com/murakamixi/items/5203832663e47f4c3990

from typing import overload

@overload
def add(a: int, b: int) -> int:...

@overload
def add(a: float, b: float) -> float:...

def add(a, b):
    return a + b
