# coding: utf-8
from typing import Any, Callable


def recursvie_map(data:Any, value_func:Callable=None, list_func:Callable=None, dict_func:Callable=None):
    """再帰的MAP処理
    dictやlistに対し、最下層まで変換処理を適用する。
    値の変換だけでなく、list_func や dict_func でデータ数やキー名なども変化させることが可能。

    Args:
        data        : 変換前データ。type = dict | list | scalar
        value_func  : スカラー値項目に適用する変換関数
        list_func   : list項目に適用する変換関数(ReturnType -> list)
        dict_func   : dict項目に適用する変換関数(ReturnType -> dict)

    Returns:
        arg1.data と同じ型: 各変換関数を適用したデータ

    Examples:
        result = recursive.recursvie_map(
            data=input_data,
            value_func=lambda x: __value_converter(
                value=x,
                [param1=value1],
                [...]
            ),
            list_func = lambda x: __list_converter(
                list_data=x,
                [param1=value1],
                [...]
            ),
            dict_func = lambda x: __dict_converter(
                dict_data=x,
                [param1=value1],
                [...]
            )
        )

    Note:
        value_func が最後に適用される。

    """
    

    # dict
    if isinstance(data, dict):
        # dict_func で変換処理してから再帰処理にかける。
        result:dict = data
        if callable(dict_func):
            result = dict_func(result)
        result = {
            k : recursvie_map(data=v, value_func=value_func, list_func=list_func, dict_func=dict_func)
            for k,v in result.items()
        }
        return result

    # list
    elif isinstance(data, list):
        # list_func で変換処理してから再帰処理にかける。
        result:list = data
        if callable(list_func):
            result = list_func(result)
        result = [
            recursvie_map(data=v, value_func=value_func, list_func=list_func, dict_func=dict_func)
            for v in result
        ]
        return result

    # scalar
    else:
        # value_func で変換処理
        if callable(value_func):
            return value_func(data)
        else:
            return data

