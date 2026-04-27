import pytest
from data_table import DataTable
from pprint import pprint
from datetime import datetime




def test_convert():
    """"変換処理（基本動作）"""

    data = {
        "id"  : [1       ,  2    , 3        , ],
        "name": ["Alice" , "Bob" , "Charlie", ],
        "sex" : ["F"     , None  , "M"      , ],
        "age" : [None    , "22"  ,            ],
    }
    dt1 = DataTable(data=data)

    # データ型が変更されている
    ret = dt1.convert(column="id", dtype="str")
    assert ret == ["1", "2", "3"]

    ret = dt1.convert(column="age", dtype="int")
    assert ret == [None, 22, None]

    # テーブルは変更されていない
    ret = dt1["age"]
    assert ret == [None, "22", None]



def test_isnull_nullif():
    """NULL処理"""

    data = {
        "id"  : [1       ,  2    , 3        , ],
        "name": ["Alice" , "Bob" , "Charlie", ],
        "sex" : ["F"     , None  , "M"      , ],
        "age" : [None    , "22"  ,            ],
    }
    dt1 = DataTable(data=data)

    # ISNULL変換（NULL -> 指定値）
    ret = dt1.convert(column="sex", dtype="str", is_null="F")
    assert ret == ["F", "F", "M"]

    # NULLIF変換（指定値 -> NULL）
    ret = dt1.convert(column="sex", dtype="str", null_if="M")
    assert ret == ["F", None, None]



def test_error_coerce():
    """変換エラー:coerce"""

    data = {
        "id"  : [1       ,  2    , 3        , ],
        "name": ["Alice" , "Bob" , "Charlie", ],
        "sex" : ["F"     , None  , "M"      , ],
        "age" : [None    , "XXX" , "40"     , ],
    }
    dt1 = DataTable(data=data)

    # 'coerce:強制(NULL)'
    error_data = []
    ret = dt1.convert(column="age", dtype="int", errors='coerce', error_data=error_data)

    # 変換結果: エラーデータは None に変換される
    assert ret == [None, None, 40]

    # エラーデータ
    assert len(ret) == len(error_data)
    assert error_data[0] == None                # 正常データはNone
    assert isinstance(error_data[1], Exception) # エラー該当行は Exception
    assert error_data[2] == None                # 正常データはNone



def test_error_ignore():
    """変換エラー:ignore"""

    data = {
        "id"  : [1       ,  2    , 3        , ],
        "name": ["Alice" , "Bob" , "Charlie", ],
        "sex" : ["F"     , None  , "M"      , ],
        "age" : [None    , "XXX" , "40"     , ],
    }
    dt1 = DataTable(data=data)

    # 'coerce:無視'
    error_data = []
    ret = dt1.convert(column="age", dtype="int", errors='ignore', error_data=error_data)

    # 変換結果: エラーデータは無変換
    assert ret == [None, "XXX", 40]

    # エラーデータ
    assert len(ret) == len(error_data)
    assert error_data[0] == None                # 正常データはNone
    assert isinstance(error_data[1], Exception) # エラー該当行は Exception
    assert error_data[2] == None                # 正常データはNone





def test_error_raise():
    """変換エラー:raise"""

    data = {
        "id"  : [1       ,  2    , 3        , ],
        "name": ["Alice" , "Bob" , "Charlie", ],
        "sex" : ["F"     , None  , "M"      , ],
        "age" : [None    , "XXX" , "40"     , ],
    }
    dt1 = DataTable(data=data)

    # 'raise:例外発生'
    with pytest.raises(Exception) as e:
        ret = dt1.convert(column="age", dtype="int", errors='raise')
    assert "InvalidOperation" in str(e)


