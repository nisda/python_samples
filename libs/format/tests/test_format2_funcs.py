import pytest
from datetime import datetime
from format_ex.format2 import extract_placeholders
from format_ex.format2 import convert_placeholders
from format_ex.format2 import is_fieldname_only




@pytest.mark.parametrize(
    [
        "template", "expected",
    ],
    [
        pytest.param("a.b", []),                                        # プレースホルダーなし
        pytest.param("{a.b}", ["a.b"]),                                 # プレースホルダーあり
        pytest.param("{a.b}_{c.d}_{e}", ["a.b", "c.d", "e"]),           # 複数
        pytest.param("{a.b}_{{c.d}}_{e}", ["a.b", "e"]),                # エスケープ（2重） -> プレースホルダーではない
        pytest.param("{a.b}_{{{c.d}}}_{e}", ["a.b", "c.d", "e"]),       # エスケープ（3重） -> 文字列の{} + プレースホルダー
        pytest.param("{a.b}_{{{{c.d}}}}_{e}", ["a.b", "e"]),            # エスケープ（4重） -> 文字列の{{}}
        pytest.param("{a.b}_{{{{{c.d}}}}}_{e}", ["a.b", "c.d", "e"]),   # エスケープ（5重） -> 文字列の{{}} + プレースホルダー
        pytest.param("{a.b}_{{{{{{c.d}}}}}}_{e}", ["a.b", "e"]),        # エスケープ（6重） -> 文字列の{{{}}}
        pytest.param("_{a.b:_{c.d}_}", ["a.b", "c.d"]),                 # specのプレースホルダーも可（ここだけnest可能）
        pytest.param("_{a.b:_{c.d}_}_{c.d}_{a.b}", ["a.b", "c.d"]),     # 重複 -> ユニーク化
    ]
)
def test_extract_placeholders(template, expected):
    """プレースホルダー内の文言をすべて抽出（ユニーク化済み）"""
    ret = extract_placeholders(template)
    assert ret == expected



@pytest.mark.parametrize(
    [
        "template", "expected",
    ],
    [
        # -- 基本形
        pytest.param("a.b", "a.b"),
        pytest.param("{a.b}", "{a[b]}"),
        pytest.param("{a.b}_{c.d}_{e}", "{a[b]}_{c[d]}_{e}"),
        pytest.param("_{a.b:_{c.d}_}", "_{a[b]:_{c[d]}_}"),
        pytest.param("_{a.b:_{c.d}_}_{c.d}_{a.b}", "_{a[b]:_{c[d]}_}_{c[d]}_{a[b]}"),

        # 混在
        pytest.param("_{a.b.c.0.e:_{x.0.y.z}_} / {a.3}", "_{a[b][c][0][e]:_{x[0][y][z]}_} / {a[3]}"),
        pytest.param("_{a[b].c[0].e:_{x.0[y][z]}_} / {a[3]}", "_{a[b][c][0][e]:_{x[0][y][z]}_} / {a[3]}"),

        # エスケープ
        pytest.param("{a.b}_{{c.d}}"    , "{a[b]}_{{c.d}}"),
        pytest.param("{a.b}_{{{c.d}}}"  , "{a[b]}_{{{c[d]}}}"),
        pytest.param("{a.b}_{{{{c.d}}}}" , "{a[b]}_{{{{c.d}}}}"),
        pytest.param("{a.b}_{{{{{c.d}}}}}" , "{a[b]}_{{{{{c[d]}}}}}"),
        pytest.param("{a.b}_{{{{{{c.d}}}}}}" , "{a[b]}_{{{{{{c.d}}}}}}"),
    ]
)
def test_convert_placeholders(template, expected):
    """プレースホルダーの変換）"""
    ret = convert_placeholders(template)
    assert ret == expected




@pytest.mark.parametrize(
    [
        "template", "expected",
    ],
    [
        pytest.param("{a}", True),
        pytest.param("{a:}", True),
        pytest.param("{a.aa.aaa:}", True),
        pytest.param("{a[aa]aaa:}", True),
        pytest.param("_{a}", False), 
        pytest.param("{a}_", False),
        pytest.param("{a:b}", False),
        pytest.param("{a}{b}", False),
    ]
)
def test_is_fieldname_only(template, expected):
    """１フィールドのみチェック"""
    ret = is_fieldname_only(template)
    assert ret == expected



