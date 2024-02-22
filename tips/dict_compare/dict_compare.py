# coding: utf-8

import re
from typing import Any, Callable


def is_contains(data:Any, condition:Any) -> bool:

    if isinstance(condition, dict):
        # dict の場合は子要素を比較

        if not isinstance(data, dict):
            # 両方dictでなかったらNG
            return False

        if ( (data.keys() & condition.keys()) ^ condition.keys() ):
            # conditionで指定されたkeyがすべて含まれていなかったらNG
            return False

        # 再帰呼び出しで下層を比較
        for k in condition.keys():
            if not is_contains(data[k], condition[k]):
                return False

        # すべて通ったらTrue
        return True

    elif isinstance(condition, list):
        # list の場合は、data の値が list に含まれていたらOK
        for c in condition:
            if is_contains(data, c):
                return True
        return False

    elif isinstance(condition, re.Pattern):
        # condition が正規表現の場合、それにマッチしたらOK
        return bool(condition.match(data))

    elif isinstance(condition, Callable):
        # condition が Callable のときはデータをパラメータにしてコール
        return condition(data)

    else:
        # それ以外のパターンは値として単純比較
        return bool(data == condition)

