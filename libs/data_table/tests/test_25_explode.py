import pytest
from data_table import DataTable
from pprint import pprint



def test_explode():
    """データ展開"""

    # 入力データ
    columns = ("id", "name", "favorite")
    data = [
        [1, "Alice"     , "dog"                                            ],  # スカラー値
        [2, "Bob"       , None                                             ],  # None
        [3, "Charlie"   , { "id": 101, "name": "Swimming"}                 ],  # dict
        [4, "Denis"     , ["Heavy Metal", "Yoga", None, "Games"]           ],  # list. None も1つのデータとして扱う
        [5, "Eric"      , { "id": 102, "note": "not set", "name": None}    ],  # dict キー違い
        [6, "Frank"     , [ {"id": 901}, ["Money", "Power"] ]              ],  # 複合（1階層のみ展開する）
    ]

    # 想定結果
    expected_columns = ("id", "name", "favorite", "favorite__id", "favorite__name", "favorite__note")
    expected_data = {
        "favorite"          : [ "dog", None, None, "Heavy Metal", "Yoga", None, "Games", None, {"id": 901}, ["Money", "Power"] ],
        "favorite__id"      : [ None,  None, 101 , None, None, None, None, 102 , None, None],
        "favorite__name"    : [ None,  None, "Swimming" , None, None, None, None, None, None, None],
        "favorite__note"    : [ None,  None, None , None, None, None, None, "not set" , None, None],
    }


    # カラム、データの確認
    dt = DataTable(data=data, columns=columns)
    dt = dt.explode(key="favorite", sep='__')

    assert dt.row_count         == 10
    assert dt.columns           == expected_columns
    assert dt["favorite"]       == expected_data["favorite"]
    assert dt["favorite__id"]    == expected_data["favorite__id"]
    assert dt["favorite__name"]  == expected_data["favorite__name"]
    assert dt["favorite__note"]  == expected_data["favorite__note"]

