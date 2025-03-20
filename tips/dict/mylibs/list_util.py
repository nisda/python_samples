from typing import List, Any
from . import value_util


def compare(list_left:List[Any], list_right:List[Any]) -> int:
    """
    複数のデータ型に対応した list 比較処理
    """

    # 要素の長さを取得
    len_left = len(list_left)
    len_right = len(list_right)
    len_min = min(len_left, len_right)

    # 両方に値がある範囲での比較
    for i in range(0, len_min):
        v1 = list_left[i]
        v2 = list_right[i]
        if 0 != (ret := value_util.compare(value_left=v1, value_right=v2)):
            # 差異があればその時点で返却
            return ret

    # ここまで一致していた場合は、長さで比較
    if len_left < len_right: return -1
    if len_left > len_right: return 1
    return 0


def list_sort(data:List[Any]) -> List[Any]:

    def __quick_sort(data):
        # 最後の要素は何もせず返却
        if len(data) <= 1:
            return data

        # 真ん中の要素をピボットとする。
        pivot = data.pop(len(data) // 2)

        # ピボットを基準に大小に振り分け
        small  = [ x for x in data if value_util.compare(x, pivot) <= 0]
        large = [ x for x in data if 0 < value_util.compare(x, pivot)]

        # 再帰処理
        small = __quick_sort(small)
        large = __quick_sort(large)

        return small + [pivot] + large

    return __quick_sort(data=data)


def list_list_sort(data:List[List[Any]]) -> List[List[Any]]:

    def __quick_sort(data):
        # 最後の要素は何もせず返却
        if len(data) <= 1:
            return data

        # 真ん中の要素をピボットとする。
        pivot = data.pop(len(data) // 2)

        # ピボットを基準に大小に振り分け
        small = [ x for x in data if compare(x, pivot) <= 0]
        large = [ x for x in data if 0 < compare(x, pivot)]

        # 再帰処理
        small = __quick_sort(small)
        large = __quick_sort(large)

        return small + [pivot] + large

    return __quick_sort(data=data)

