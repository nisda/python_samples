from typing import Any
import decimal
import datetime
import recursive as recursive
import re
import pytest

#-----------------------------------------------
# テスト用内部関数
#-----------------------------------------------

# スカラー値 変換用関数
def __value_converter(key:Any, value, base_dt:datetime, dt_format:str) -> Any:
    # 項目名の１文字目が '*' であったら何もしない
    if isinstance(key, str) and key.startswith("*"):
        return value

    # Decimal を int | float に変換
    if isinstance(value, decimal.Decimal):
        if float(value).is_integer():
            return int(value)
        else:
            return float(value)

    # 日付は文字列に変換
    if isinstance(value, datetime.datetime):
        return value.strftime(dt_format)

    # 文字列 '@{day(x)}' を、パラメータのbase_dt を基準とした日付文字列に変換
    if isinstance(value, str) and ( m := re.fullmatch(r'@{day\((.+)\)}', value) ):
        days = m.group(1)
        dt = ( base_dt + datetime.timedelta(days=int(days)))
        return dt.strftime(dt_format)

    return value

# list 変換用関数
def __list_converter(key:Any, list_data:list, target_value:Any, amplification_count:int) -> list:
    # 項目名の１文字目が '*' であったらdictに変換する。
    if isinstance(key, str) and key.startswith("*"):
        result = {}
        for i in range(0, len(list_data)):
            result[i] = list_data[i]
        return result

    # 特定の値を増幅する。
    result = []
    for v in list_data:
        if v == target_value:
            result.extend([v] * amplification_count)    # 増幅処理。
        else:
            result.append(v)
    return result

# dict 変換用関数
def __dict_converter(key:Any, dict_data:dict) -> dict:
    # @{day(x,y)} 形式のときに、項目を２つに分ける。以下の形に変換
    # ["keyNameSince"] = "@{day(x)}"
    # ["keyNameUntil"] = "@{day(y)}"
    # x, y それぞれブランク可。ブランク時は該当項目を作らない。
    result = {}
    for k,v in dict_data.items():
        if isinstance(v, str) and ( m := re.fullmatch(r'@{day\((.*),(.*)\)}', v) ):
            if len(m.group(1).strip()) > 0:
                result[f"{k}Since"] = "@{day(" + m.group(1).strip() + ")}"
            if len(m.group(2).strip()) > 0:
                result[f"{k}Until"] = "@{day(" + m.group(2).strip() + ")}"
        else:
            result[k] = v
    return result 



#-----------------------------------------------
# pytest
#-----------------------------------------------

def test_value_func_1():
    now_dt = datetime.datetime.now()
    input_data = {
        "str" : "AAA",
        "int" : 123,
        "decimal_int" : decimal.Decimal(123),
        "decimal_float" : decimal.Decimal(12.345),
        "datetime_str" : now_dt,
        "*str" : "AAA",
        "*int" : 123,
        "*decimal_int" : decimal.Decimal(123),
        "*decimal_float" : decimal.Decimal(12.345),
        "*datetime_str" : now_dt,
    }

    # テスト対象
    result = recursive.recursive_map(
        data=input_data,
        value_func=lambda k,v: __value_converter(
            key=k,
            value=v,
            base_dt=datetime.datetime.fromisoformat("2025-01-09 12:00:00"),
            dt_format="%Y-%m-%d"
        )
    )
    # 結果確認
    assert result["str"] == "AAA"
    assert result["int"] == int(123)
    assert result["decimal_int"] == int(123)
    assert result["decimal_float"] == float(12.345)
    assert result["datetime_str"] == now_dt.strftime("%Y-%m-%d")
    assert result["*str"] == "AAA"
    assert result["*int"] == int(123)
    assert result["*decimal_int"] == decimal.Decimal(123)
    assert result["*decimal_float"] == decimal.Decimal(12.345)
    assert result["*datetime_str"] == now_dt




# listコンバータ
def test_recursive_map_list_func_1():
    input_data = [1, 2, 3, "1", "2", "3", 1, 2, 3, "1", "2", "3"]

    result = recursive.recursive_map(
        data=input_data,
        list_func = lambda k,v: __list_converter(
            key=k,
            list_data=v,
            target_value="3",
            amplification_count=2,
        )
    )
    print(result)
    assert result == [1, 2, 3, "1", "2", "3", "3", 1, 2, 3, "1", "2", "3", "3"]


# dictコンバータ
def test_recursive_map_map_func_1():
    input_data = {
        "between" : "@{day(-1, 2)}",
        "from" : "@{day(-1,)}",
        "to" : "@{day(,2)}",
    }
    result = recursive.recursive_map(
        data=input_data,
        dict_func = lambda k,v: __dict_converter(
            key=k,
            dict_data=v,
        )
    )
    print(result)
    assert result.get("between", None) is None
    assert result.get("from", None) is None
    assert result.get("to", None) is None
    assert result.get("betweenSince", None) == "@{day(-1)}"
    assert result.get("betweenUntil", None) == "@{day(2)}"
    assert result.get("fromSince", None) == "@{day(-1)}"
    assert result.get("toUntil", None) == "@{day(2)}"


# 複合パターン
def test_recursive_map_1():
    # 入力データ
    input_data = {
        "a" : "AAA",
        "b" : 1,
        "c" : decimal.Decimal(123),
        "d" : decimal.Decimal(12.345),
        "e" : "@{day(0)}",
        "f" : {
            "fa" : "F_FA",
            "fb" : 2,
            "fc" : decimal.Decimal(234),
            "fd" : decimal.Decimal(23.456),
            "fe" : {
                "str" : "str",
                "yesterday" : "@{day(-1)}",
                "today" : "@{day(0)}",
                "tomorrow" : "@{day(1)}",
                "between" : "@{day(-2, 3)}",
                "from" : "@{day(-2, )}",
                "to" : "@{day(,3)}",
                "list" : [1, 2, 3],
                "dict" : {"fe1": 1, "fe2": 2},
                "*yesterday" : "@{day(-1)}",
            },
            "ff" : [
                "F_FF",
                1,
                "@{day(1)}",
                "3"
            ],
            "*fg" : [
                "FGA",
                "FGB",
            ],
        }
    }

    result = recursive.recursive_map(
        data=input_data,
        value_func=lambda k,v: __value_converter(
            key=k,
            value=v,
            base_dt=datetime.datetime.fromisoformat("2025-01-09 12:00:00"),
            dt_format="%Y-%m-%d"
        ),
        list_func = lambda k,v: __list_converter(
            key=k,
            list_data=v,
            target_value="3",
            amplification_count=2,
        ),
        dict_func = lambda k,v: __dict_converter(
            key=k,
            dict_data=v,
        )
    )
    print(result)

    assert result.get("c", None) == int(123)
    assert result.get("d", None) == float(12.345)
    assert result.get("e", None) == "2025-01-09"
    assert result.get("f", {}).get("fc") == int(234)
    assert result.get("f", {}).get("fd") == float(23.456)
    assert result.get("f", {}).get("fe", {}).get("yesterday") == "2025-01-08"
    assert result.get("f", {}).get("fe", {}).get("today") == "2025-01-09"
    assert result.get("f", {}).get("fe", {}).get("tomorrow") == "2025-01-10"
    assert result.get("f", {}).get("fe", {}).get("betweenSince") == "2025-01-07"
    assert result.get("f", {}).get("fe", {}).get("betweenUntil") == "2025-01-12"
    assert result.get("f", {}).get("fe", {}).get("fromSince") == "2025-01-07"
    assert result.get("f", {}).get("fe", {}).get("toUntil") == "2025-01-12"
    assert result.get("f", {}).get("fe", {}).get("*yesterday") == "@{day(-1)}"
    assert len(result.get("f", {}).get("ff", [])) == len(input_data.get("f", {}).get("ff", [])) + 1
    assert type(result.get("f", {}).get("*fg", {})).__name__ == 'dict'
    assert result.get("f", {}).get("*fg", {}).get(0) == 'FGA'
    assert result.get("f", {}).get("*fg", {}).get(1) == 'FGB'


