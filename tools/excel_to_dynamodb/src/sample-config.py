from typing import Dict,List,Any
import re

# カスタムファンクション：weekデータ生成
def custom_make_records_for_week(records:List[Dict[str, Any]], variables:Dict) -> List[Dict]:
    # week の曜日別にレコードを作成する

    results:List[Dict] = []
    for record in records:
        i:int = -1
        for day in record["monitoring.week"]:
            i = i + 1
            if day is None: continue
            results.append({
                "tenant_id" : record["tenant_id"],
                "day_of_week" : i,
                "start_time" : day[0],
                "end_time"   : day[1],
            })

    return results


# 読み込み設定
load_configs:dict = [
    {
        # "sheetname" : "縦並び複数件*",            # str もあり。ワイルドカード(*)可
        "sheetname" : re.compile("(.*)び(.*)"),     # re.Pattern も可
        "tables" : {
            "TBL_A": {
                "data_attr": {
                    "system-name" : {},
                    # "config1.category" : { "convert" : { "type":"ABC.Category" } },
                    # "config1.type" : { "convert": { "type":"ABC.Type" } },
                    # "config1.user" : { "convert": { "type":"ABC.User" } },
                    "config1.category" : { "convert" : { "name":"ABC.Category" } },
                    "config1.type" : { "convert": { "name":"ABC.Type" } },
                    "config1.user" : { "convert": { "name":"ABC.User" } },
                    "monitoring.use" : {},
                    "monitoring.week" : { "convert_type": None},
                },
                # *** 以下、開発中 ***
                "data_ranges" : [
                    {
                        "name"   : "test_values",
                        "direction" : "horizonal",
                        "header" : ["Required_2", "Caption_2", "VALUE"],
                        "min_row": 4,
                        "min_col": 4,
                        "max_row": 0,
                        "max_col": 0,
                    },
                    {
                        "name"   : "tests_attr",
                        "direction" : "horizonal",
                        "header" : None,
                        "min_row": 3,
                        "min_col": 2,
                        # "max_row": 0,
                        "max_col": 5,
                    },
                ]
            },
        },
    },
]


dynamodb_configs:List[Dict] = [
    {
        "table_name": "{var.prefix}-basic-config",
        "table_region": "{var.region}",
        "source" : "TBL_A",
        # 登録前削除設定。
        "pre-delete" : {
            "system_id": "{var.system_name}",
        },
        # 登録データテンプレート
        "template" : {
            "system_name" : "{var.system_name}",
            "tenant_id" : "{source.tenant_id}",
            "config1" : {
                "category" : "{source.config1.category}",
                "type" : "{source.config1.type}",
                "user" : "{source.config1.user}",
            },
            "retry" : {
                "count" : "{source.retry_count}",
            },
        },
    },
    {
        "table_name": "{var.prefix}-weekly",
        "source" : "TBL_A",
        # レコード処理のカスタム関数
        "function" : custom_make_records_for_week,
        # 事前削除
        "pre-delete" : {
            "index" : None,
            "keys" : {
                "tenant_id": "{source.system_name}",
            },
        },
        # 登録データテンプレート
        "template" : {
            "tenant_id"   : "{source.tenant_id}",
            "day_of_week" : "{source.day_of_week}",
            "time_from"   : "{source.start_time}",
            "time_to"     : "{source.end_time}",
        },
    },
]

