# coding: utf-8
from typing import Any, Callable

def recursive_map(data:Any, value_func:Callable=None, list_func:Callable=None, dict_func:Callable=None):
    """再帰的MAP処理
    dictやlistに対し、最下層まで変換処理を適用する。
    値の変換だけでなく、list_func や dict_func でデータ数やキー名なども変化させることが可能。

    Args:
        data        : 変換前データ。type = dict | list | scalar
        value_func  : スカラー値項目に適用する変換関数
        list_func   : list項目に適用する変換関数
        dict_func   : dict項目に適用する変換関数

    Returns:
        Any : 各変換関数を適用したデータ

    Examples:
        result = recursive.recursive_map(
            data=input_data,
            value_func=lambda k,v: __value_converter(
                key=k
                value=v,
                [param1=value1],
                [...]
            ),
            list_func = lambda k,v: __list_converter(
                key=k,
                list_data=v,
                [param1=value1],
                [...]
            ),
            dict_func = lambda k,v: __dict_converter(
                key=k,
                dict_data=v,
                [param1=value1],
                [...]
            )
        )

    Note:
        value_func が最後に適用される。

    """
    return __recursive_map(data=data, value_func=value_func, list_func=list_func, dict_func=dict_func, current_key=None)
    

def __recursive_map(data:Any, value_func:Callable=None, list_func:Callable=None, dict_func:Callable=None, current_key=None):

    # STEP1. list, dict の変換
    if isinstance(data, dict):
        # dict は dict_func で変換処理
        if callable(dict_func):
            data = dict_func(current_key, data)
    elif isinstance(data, list):
        # list は list_func で変換処理してから再帰処理にかける。
        if callable(list_func):
            data = list_func(current_key, data)

    # STEP2. data の変換
    if isinstance(data, dict):
        # dict の 再帰処理。
        return {
            k : __recursive_map(data=v, value_func=value_func, list_func=list_func, dict_func=dict_func, current_key=k)
            for k,v in data.items()
        }
    elif isinstance(data, list):
        # list の 再帰処理。
        return [
            __recursive_map(data=v, value_func=value_func, list_func=list_func, dict_func=dict_func, current_key=current_key)
            for v in data
        ]
    else:
        # scalar は value_func で変換処理
        if callable(value_func):
            return value_func(current_key, data)
        else:
            return data

