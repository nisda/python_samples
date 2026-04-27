import pytest
from data_table import DataTable
from pprint import pprint
from datetime import datetime




def test_column_rename():
    """"リネーム"""

    data = {
        "id"  : [1       ,  2    , 3        , ],
        "name": ["Alice" , "Bob" , "Charlie", ],
        "sex" : ["F"     , None  , "M"      , ],
        "age" : [None    , "22"  ,            ],
    }
    dt1 = DataTable(data=data)
    assert dt1.columns == ["id", "name", "sex", "age"]

    # 列名変更
    dt1.rename(columns={"sex": "gender", "id": "person_id"})
    assert dt1.columns == ["person_id", "name", "gender", "age"]

    # データを取ってみる
    assert dt1["gender"] == ["F"     , None  , "M"      , ]
    assert dt1["sex"] == None




