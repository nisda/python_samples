import pytest
from datetime import datetime
from decimal import Decimal
from format_ex.format2 import format


INPUT_DATA = {
    "a" : { "aa" : { "aaa" : "AAA"} },
    "b" : [
        {
            "b0a": (
                { "b0a0a" : "B0A0A" },
            )
        }
    ],
    "c" : {
        "decimal" : Decimal("123.45"),
        "datetime": datetime(2026, 4, 30, 20, 47, 13, 123456),
    },
    "d" : {
        "date_format" : "%Y%m%d",
        "datetime_format" : "%Y%m%d%H%M%S.%f",
        "digit_len" : 6,
    }
}


"""基本動作（階層アクセス）"""
@pytest.mark.parametrize(
    [
        "expr", "expect",
    ],
    [
        pytest.param("a.aa.aaa"  , "a.aa.aaa"),         # 対象外（プレースホルダーなし）
        pytest.param("{a.aa.aaa}", "AAA"),              # 変換
        pytest.param("//{a.aa.aaa}//", "//AAA//"),      # 混在
        pytest.param("{b.0.b0a.0.b0a0a}", "B0A0A"),     # 変換, list, tuple 含み
        pytest.param("{b[0][b0a].0.b0a0a}", "B0A0A"),   # 表記パターン
        pytest.param("{b[0][b0a]}"      , str(({"b0a0a":"B0A0A"},))),               # 階層（ノード）
        pytest.param("{b[0][b0a].0}"    , str({"b0a0a":"B0A0A"})),                  # 階層（ノード）
        pytest.param("{b[0]}"           , str({"b0a": ({"b0a0a":"B0A0A"},)})),      # 階層（ノード）
        pytest.param("{b}"              , str([{"b0a": ({"b0a0a":"B0A0A"},)}])),    # 階層（ノード）
   ]
)
def test_format(expr, expect):
    """基本動作（階層アクセス）"""

    ret = format(expr, data=INPUT_DATA)
    assert ret == expect
    assert type(ret) == type(expect)


"""フォーマット指定"""
@pytest.mark.parametrize(
    [
        "expr", "expect",
    ],
    [
        pytest.param("{c.decimal}", "123.45"),
        pytest.param("{c.decimal:015,.4f}", "00,000,123.4500"),
        pytest.param("{c.decimal:015,.{d.digit_len}f}", "0,000,123.450000"),
        pytest.param("{c.datetime}", "2026-04-30 20:47:13.123456"),
        pytest.param("{c.datetime:{d.datetime_format}}", "20260430204713.123456"),
        pytest.param("{c.datetime:{d.date_format}}", "20260430"),
   ]
)
def test_spec(expr, expect):
    """フォーマット指定"""
    ret = format(expr, data=INPUT_DATA)
    assert ret == expect
    assert type(ret) == type(expect)


"""エスケープ"""
@pytest.mark.parametrize(
    [
        "expr", "expect",
    ],
    [
        pytest.param("{a.aa.aaa}_{{c.decimal}}_{c.datetime:{d.date_format}}", "AAA_{c.decimal}_20260430"),
   ]
)
def test_escape(expr, expect):
    """エスケープ"""
    ret = format(expr, data=INPUT_DATA)
    assert ret == expect
    assert type(ret) == type(expect)


"""パス指定エラー"""
@pytest.mark.parametrize(
    [
        "expr", "e_type", "e_msg", 
    ],
    [
        pytest.param("{a.xx}", KeyError, "'xx'"),                                                   # dict 非存在キー
        pytest.param("{xxx.xx}", KeyError, "'xxx'"),                                                # dict 非存在キー
        pytest.param("{a.aa.aaa.xxx}", TypeError, "string indices must be integers, not 'str'"),    # str  キー指定
        pytest.param("{b.unknown}", TypeError, "list indices must be integers or slices, not str"), # list キー指定
        pytest.param("{b.999}", IndexError, "list index out of range"),                             # list 非存在INDEX
    ]
)
def test_wrong_path(expr, e_type, e_msg):
    """エラー"""
    with pytest.raises(Exception) as e:
        ret = format(expr, data=INPUT_DATA)
    assert e.type == e_type
    assert str(e.value) == e_msg

