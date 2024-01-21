import json
import os
import datetime
import decimal 

JSON_IN  = os.path.join(os.path.dirname(__file__), "sample-input.json")
JSON_OUT = os.path.join(os.path.dirname(__file__), "sample-output.json")


# json.dump未対応データ型の変換関数
def json_serialize(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, decimal.Decimal):
        return float(obj)
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
            "decimal": decimal.Decimal(123456.78),
        },
        "null": None,
        "list" : [
            "a1",
            "a2",
            "a3"
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

