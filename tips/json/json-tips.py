import json
import os
import datetime
import decimal
import uuid
import sys

JSON_IN  = os.path.join(os.path.dirname(__file__), "sample-input.json")
JSON_OUT = os.path.join(os.path.dirname(__file__), "sample-output.json")


# json.dump未対応データ型の変換関数
# usage:
#   json.dumps(variable, default=common_funcs.json_serialize)
def json_serialize(obj):
    # datetime
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    # defimal
    if isinstance(obj, decimal.Decimal):
        if '.' in str(obj):
            return float(obj)
        else:
            return int(obj)
    # bytes
    if isinstance(obj, bytes):
        return obj.decode()
    # uuid
    if isinstance(obj, uuid.UUID):
        return str(obj)
    # 上記以外はサポート対象外.
    raise TypeError ("Type %s not serializable" % type(obj))



if __name__ == '__main__':

    # データ生成
    output_data = {
        "str": "JSONテスト",
        "int": 123,
        "float": 1234.56,
        "dict" : {
            "dt" : datetime.datetime.now(),
            "decimal_1": decimal.Decimal(-123456),
            "decimal_2": decimal.Decimal(-123456.78),
            "decimal_3": decimal.Decimal(-123456.000),
        },
        "null": None,
        "uuid": uuid.uuid4(),
        "bytes": b'binary!',
        "list" : [
            "d1-a",
            "d1-b",
            [
                "d2-a",
                "d2-b",
            ],
        ],
        "tuple" : ("t1", "t2"),
    }

    # 表示
    print("--- 表示：json.dumps")
    json_str = json.dumps(
        output_data,
        indent=2,
        default=json_serialize,
        ensure_ascii=False,
        sort_keys=True,
    )
    print(json_str)

    sys.exit(0)


    # ファイル出力
    print("--- ファイル出力：json.dump")
    with open(JSON_OUT, 'w', encoding="utf-8") as f:
        json.dump(
            output_data,
            f,
            indent=2,
            default=json_serialize,
            ensure_ascii=False,
            sort_keys=True,
        )


    # json文字列をdictに変換
    print("--- json_str -> dict：json.loads")
    loads_data = json.loads(json_str)
    print(loads_data)

    # ファイル読込
    print("--- ファイル読込：json.load")
    with open(JSON_OUT, 'r', encoding="utf-8") as f:
        input_data: dict = json.load(f)
    print(input_data)

