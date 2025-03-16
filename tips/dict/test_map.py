import mylibs.dict_util as dict_util
import decimal
import datetime

# テスト用関数: 値変換
def __value_converter(key, value, dt_format, ignore_keys=[]):
    # ignore_keys に合致する場合は無編集
    if key in ignore_keys:
        return value

    # Decimal を int|float に変換
    if isinstance(value, decimal.Decimal):
        if float(value).is_integer():
            return int(value)
        else:
            return float(value)
    # 日付は指定フォーマットの文字列に変換
    if isinstance(value, datetime.datetime):
        return value.strftime(dt_format)

    # それ以外は無編集
    return value

# テスト用関数: dict構造変更
def __dict_converter(key, value):
    # dict 以外は何もしない
    if not isinstance(value, dict): return value

    # 以下条件どちらかを満たす場合はdict構造を変更する。
    #   1) キーに / が含まれていたら項目を２つに分割。
    #   2) 値が null であったら項目を削除
    temp = {}
    for k, v in value.items():
        if v is None: continue
        if len(keys := k.split('/')) == 2: 
            temp[keys[0]] = v
            temp[keys[1]] = v
            continue
        temp[k] = v
    return temp




def test_map_value_convert():
    original_data = {
        "str" : "STR",
        "int" : 123,
        "decimal_int" : decimal.Decimal(123),
        "decimal_float" : decimal.Decimal(123.45),
        "datetime" : datetime.datetime(year=2025, month=2, day=16, hour=9, minute=23, second=45),
        "list" : [
            "STR",
            123,
            decimal.Decimal(123),
            decimal.Decimal(123.45),
            datetime.datetime(year=2025, month=2, day=16, hour=9, minute=23, second=45),
            
        ]
    }


    ret = dict_util.map(
        data=original_data,
        func=(lambda k,v: __value_converter(
            key = k,
            value = v,
            dt_format="%Y-%m-%d %H.%M.%S"
        ))
    )

    assert isinstance(ret["decimal_int"], int)
    assert ret["decimal_int"] == int(123)

    assert isinstance(ret["decimal_float"], float)
    assert ret["decimal_float"] == float(123.45)

    assert ret["datetime"] == "2025-02-16 09.23.45"

    assert ret["list"] == [
        "STR",
        123,
        int(123),
        float(123.45),
        "2025-02-16 09.23.45",
    ]


def test_map_list_convert():
    original_data = [
        "STR",
        123,
        decimal.Decimal(123),
        decimal.Decimal(123.45),
        datetime.datetime(year=2025, month=2, day=16, hour=9, minute=23, second=45),
    ]

    ret = dict_util.map(
        data=original_data,
        func=(lambda k,v: __value_converter(
            key = k,
            value = v,
            dt_format="%Y-%m-%d %H.%M.%S"
        ))
    )

    assert ret == [
        "STR",
        123,
        int(123),
        float(123.45),
        "2025-02-16 09.23.45",
    ]


def test_map_recursive():
    original_data = {
        "datetime" : datetime.datetime(year=2025, month=2, day=16, hour=9, minute=23, second=45),
        "A" : {
            "datetime" : datetime.datetime(year=2025, month=2, day=16, hour=9, minute=23, second=45),
            "AA" : {
                "datetime" : datetime.datetime(year=2025, month=2, day=16, hour=9, minute=23, second=45),
                "AAA" : [
                    datetime.datetime(year=2025, month=2, day=16, hour=9, minute=23, second=45),
                    datetime.datetime(year=2025, month=2, day=16, hour=9, minute=23, second=45),
                ]
            }
        }
    }

    ret = dict_util.map(
        data=original_data,
        func=(lambda k,v: __value_converter(
            key = k,
            value = v,
            dt_format="%Y-%m-%d %H.%M.%S"
        ))
    )

    assert ret == {
        "datetime" : "2025-02-16 09.23.45",
        "A" : {
            "datetime" : "2025-02-16 09.23.45",
            "AA" : {
                "datetime" : "2025-02-16 09.23.45",
                "AAA" : [
                    "2025-02-16 09.23.45",
                    "2025-02-16 09.23.45",
                ]
            }
        }
    }


def test_map_use_key():
    original_data = {
        "aaa" : decimal.Decimal(123),
        "bbb" : decimal.Decimal(123),
        "ccc" : decimal.Decimal(123),
        "child" : {
            "aaa" : [
                decimal.Decimal(123),
                [
                    [
                       decimal.Decimal(123), 
                    ]
                ]
            ],
            "bbb" : [
                decimal.Decimal(123),
                [
                    [
                       decimal.Decimal(123), 
                    ]
                ]
            ],
        }
    }

    # 関数内で現在のキーを使用
    ret = dict_util.map(
        data=original_data,
        func=(lambda k,v: __value_converter(
            key = k,
            value = v,
            dt_format="%Y-%m-%d %H.%M.%S",
            ignore_keys=["aaa", "ccc"]
        ))
    )

    # 条件に合致するキーは変換処理しない。func:__value_converterでそういう処理
    assert isinstance(ret["aaa"], decimal.Decimal)                      
    assert isinstance(ret["ccc"], decimal.Decimal)
    assert isinstance(ret["child"]["aaa"][0], decimal.Decimal)          # listでも適用可能
    assert isinstance(ret["child"]["aaa"][1][0][0], decimal.Decimal)    # listでは最も近いキーが適用される。

    # 条件に合致しないキーは変換処理を実施する
    assert isinstance(ret["bbb"], int)
    assert isinstance(ret["child"]["bbb"][0], int)
    assert isinstance(ret["child"]["bbb"][1][0][0], int)


def test_map_use_key():
    original_data = {
        "aaa" : 123,
        "bb/cc" : "BC",
        "dd" : None,
        "child" : [
            {
                "aaa" : 123,
                "bb/cc" : "BC",
                "dd" : None,
            }
        ],
    }

    # 関数内で現在のキーを使用
    ret = dict_util.map(
        data=original_data,
        func=(lambda k,v: __dict_converter(
            key = k,
            value = v,
        ))
    )

    # 処理結果の確認
    assert ret["bb"] == "BC"        # 分割されている
    assert ret["cc"] == "BC"        # 分割されている
    assert not "dd" in ret.keys()   # None 項目は削除されている。

    # 深い階層でも同じく処理されている
    assert ret["child"][0]["bb"] == "BC"        # 分割されている
    assert ret["child"][0]["cc"] == "BC"        # 分割されている
    assert not "dd" in ret["child"][0].keys()   # None 項目は削除されている。
