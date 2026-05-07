import pytest
from datetime import datetime
from decimal import Decimal
from syntax import Evaluater


INPUT_DATA = {
    "a" : {
         "aa" : {"aaa" : "AAA"},
         "ab" : "AB",
         "ac" : 123,
    },
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

        pytest.param("a['aa']['aaa']"   , "a['aa']['aaa']"),        # 対象外（プレースホルダーなし）
        pytest.param("a.aa.aaa"         , "a.aa.aaa"),              # 対象外（プレースホルダーなし）
        pytest.param("{a['aa']['aaa']}", "AAA"),                    # フィールド表記
        pytest.param("{a.aa.aaa}", "AAA"),                          # フィールド表記（ドット）
        pytest.param("{a['aa'].aaa}", "AAA"),                       # フィールド表記（混在）
        pytest.param("//{a.aa.aaa}//", "//AAA//"),                  # 固定文字列あり
        pytest.param("//{a.aa.aaa}-{a.ab}//", "//AAA-AB//"),        # 複数
        pytest.param("{b[0].b0a[0].b0a0a}", "B0A0A"),               # list, tuple 含みの多階層

        # 階層の途中（ノード）
        pytest.param("{b[0].b0a}"       , ({"b0a0a":"B0A0A"},)),               # 階層途中
        pytest.param("{b[0].b0a[0]}"    , {"b0a0a":"B0A0A"}),                  # 階層途中
        pytest.param("{b[0]}"           , {"b0a": ({"b0a0a":"B0A0A"},)}),      # 階層途中
        pytest.param("{b}"              , [{"b0a": ({"b0a0a":"B0A0A"},)}]),    # 階層途中
   ]
)
def test_format(expr, expect):
    """基本動作（階層アクセス）"""

    evaluater = Evaluater()
    ret = evaluater.format(expr, mapping=INPUT_DATA)
    assert ret == expect
    assert type(ret) == type(expect)



"""オリジナルタイプ指定"""
@pytest.mark.parametrize(
    [
        "expr", "original_type", "expcted"
    ],
    [
        # 基本動作
        pytest.param("{a.ab}"   , False , "AB"),
        pytest.param("{a.ab}"   , True  , "AB"),    # どちらにしろstr
        pytest.param("{a.ac}"   , False , "123"),
        pytest.param("{a.ac}"   , True  , 123),
        pytest.param("{c.decimal}"   , False , "123.45"),
        pytest.param("{c.decimal}"   , True  , Decimal("123.45")),

        # 単一プレースホルダー以外（strでの返却になる）
        pytest.param("_{a.ac}"      , True  , "_123"),          # 固定文字列あり
        pytest.param("{a.ac}_"      , True  , "123_"),          # 固定文字列あり    
        pytest.param("{a.ac}{a.ac}" , True  , "123123"),        # 複数プレースホルダー
        pytest.param("{a.ac:0>10}"  , True  , "0000000123"),    # specあり

   ]
)
def test_format(expr, original_type, expcted):
    """オリジナルタイプ指定"""

    evaluater = Evaluater()
    ret = evaluater.format(expr, mapping=INPUT_DATA, original_type=original_type)
    assert ret == expcted
    assert type(ret) == type(expcted)





"""フォーマット指定"""
@pytest.mark.parametrize(
    [
        "expr", "expect",
    ],
    [
        pytest.param("{c.decimal}", Decimal("123.45")),
        pytest.param("{c.decimal:015,.4f}", "00,000,123.4500"),
        pytest.param("{c.decimal:015,.{d.digit_len}f}", "0,000,123.450000"),
        pytest.param("{c.datetime}", datetime(2026, 4, 30, 20, 47, 13, 123456)),
        pytest.param("{c.datetime:{d.datetime_format}}", "20260430204713.123456"),
        pytest.param("{c.datetime:{d.date_format}}", "20260430"),
   ]
)
def test_spec(expr, expect):
    """フォーマット指定"""

    evaluater = Evaluater()
    ret = evaluater.format(expr, mapping=INPUT_DATA)
    assert ret == expect
    assert type(ret) == type(expect)



"""エスケープ"""
@pytest.mark.parametrize(
    [
        "expr", "expect",
    ],
    [
        pytest.param("{a.aa.aaa}_{{c.decimal}}_{c.datetime:{d.date_format}}", "AAA_{c.decimal}_20260430"),
        pytest.param("{a.aa.aaa}_{{{c.decimal}}}_{c.datetime:{d.date_format}}", "AAA_{123.45}_20260430"),
        pytest.param("{a.aa.aaa}_{{{{c.decimal}}}}_{c.datetime:{d.date_format}}", "AAA_{{c.decimal}}_20260430"),
   ]
)
def test_escape(expr, expect):
    """エスケープ"""

    evaluater = Evaluater()
    ret = evaluater.format(expr, mapping=INPUT_DATA)
    assert ret == expect
    assert type(ret) == type(expect)



"""パス指定エラー"""
@pytest.mark.parametrize(
    [
        "expr", "e_type", "e_msg", 
    ],
    [
        pytest.param("{a.xx}", KeyError, "\"'xx'. occurred at expression='{a.xx}'\""),                # dict 非存在キー（子要素）
        pytest.param("{xxx.xx}", KeyError, "\"'xxx'. occurred at expression='{xxx.xx}'\""),           # dict 非存在キー（親要素）
        pytest.param("{a.aa.aaa.xxx}", AttributeError, "'str' object has no attribute 'xxx'. occurred at expression='{a.aa.aaa.xxx}'"),    # str  キー指定
        pytest.param("{b.unknown}", AttributeError, "'list' object has no attribute 'unknown'. occurred at expression='{b.unknown}'"), # list キー指定
        pytest.param("{b[999]}", IndexError, "list index out of range. occurred at expression='{b[999]}'"),                             # list 非存在INDEX
    ]
)
def test_wrong_path(expr, e_type, e_msg):
    """エラー"""

    evaluater = Evaluater()
    with pytest.raises(Exception) as e:
        ret = evaluater.format(expr, mapping=INPUT_DATA)
    assert str(e.value) == e_msg
    assert e.type == e_type

