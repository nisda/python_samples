# coding: utf-8
from typing import Any
import decimal
import re
import datetime

# 再帰的MAP
def __recursvie_map(func:callable, data:Any):
    if isinstance(data, dict):
        return { k:__recursvie_map(func=func, data=v) for k,v in data.items() }
    elif isinstance(data, list):
        return [ __recursvie_map(func=func, data=v) for v in data ]
    else:
        return func(data)


# MAPで反映する関数
def convert_func(value:Any):
    if isinstance(value, decimal.Decimal):
        return float(value)
    if isinstance(value, str) and ( m := re.fullmatch(r'@day\((.+)\)', value) ):
        days = m.group(1)
        dt = ( datetime.datetime.now() + datetime.timedelta(days=int(days)))
        return dt.strftime("%Y-%m-%d")
    return value

# テストINPUTデータ
input_data = {
    "aaa" : "AAA",
    "bbb" : 1234,
    "ccc" : decimal.Decimal(12345.67),
    "ddd" : decimal.Decimal(23456),
    "eee" : [
        "xxx",
        "yyy",
        decimal.Decimal(123),
    ],
    "fff" : {
        "FA" : 123,
        "FB" : "@day(-1)",
        "FC" : {
            "FCA" : 123,
            "FCB" : "asd",
            "FCC" : [decimal.Decimal(123), 234, 456],
        }
    }
}

# テスト実行
print("-- input_data")
print(input_data)

ret = __recursvie_map(func=convert_func, data=input_data)
print("-- ret")
print(ret)
