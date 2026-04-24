import pytest
from format_ex import format_map
from datetime import datetime



@pytest.fixture
def data_1() -> dict:
    return {
        "str" : "STR",
        "int" : 123,
        "float": 123.456,
        "dt" : datetime(year=2026, month=4, day=24, hour=17, minute=10, second=53, microsecond=123456),
        "mix" : [
            None,
            None,
            {
                "m2a" : (
                    None,
                    {"m_2_a_1_a": "m 2 s 1 a"},
                )
            }
        ],
        "reserved" : {
            "keys" : "[KEYS]",
            "__str__" : "[STR]",
            "__missing__" : "[MISSING]",
            "__getattr__" : "[GETATTR]",
            "__dict__" : {"dict_a": "DICT_A", "dict_b": "DICT_B"},
        },
        "num_and_space" : {
            "1 a" : "1-A",
        },
    }




@pytest.mark.parametrize(
    [
        "expr", "expect",
    ],
    [
        pytest.param("{str}", "STR"),
        pytest.param("{int}", "123"),
        pytest.param("{mix[2].m2a[1].m_2_a_1_a}", "m 2 s 1 a"),
    ]
)
def test_dot(expr, expect, data_1):
    """ドット連結形式での変数指定"""
    ret = format_map(expr=expr, mapping=data_1)
    assert ret == expect
    assert type(ret) == type(expect)




@pytest.mark.parametrize(
    [
        "expr", "e_convertible", "e_value",
    ],
    [
        # ドット連結はNGもある想定だが、実際は大体OKだったりする。
        # なぜそうなるのかわからないが、format関数の内部処理次第なのだろう。
        pytest.param("{reserved.keys}", True, "[KEYS]"),
        pytest.param("{reserved[keys]}", True, "[KEYS]"),
        pytest.param("{reserved.__str__}", True, "[STR]"),
        pytest.param("{reserved[__str__]}", True, "[STR]"),
        pytest.param("{reserved.__missing__}", True, "[MISSING]"),
        pytest.param("{reserved[__missing__]}", True, "[MISSING]"),
        pytest.param("{reserved.__getattr__}", True, "[GETATTR]"),
        pytest.param("{reserved[__getattr__]}", True, "[GETATTR]"),

        pytest.param("{reserved[__dict__]}", True, str({"dict_a": "DICT_A", "dict_b": "DICT_B"})),

        pytest.param("{num_and_space.1 a}", True, "1-A"),
        pytest.param("{num_and_space[1 a]}", True, "1-A"),

        # ▼これはデータの書き換え自体が起こらないのでNG。
        # pytest.param("{reserved.__dict__}", True, str({"dict_a": "DICT_A", "dict_b": "DICT_B"})),
    ]
)
def test_dot_convertible(expr, e_convertible, e_value, data_1):
    """予約語等のドット連結形式の可否"""

    if e_convertible:
        ret = format_map(expr=expr, mapping=data_1)
        assert ret == e_value
        assert type(ret) == type(e_value)
    else:
        with pytest.raises(KeyError) as e:
            ret = format_map(expr=expr, mapping=data_1)




@pytest.mark.parametrize(
    [
        "expr", "expect",
    ],
    [
        pytest.param("str={str}", "str=STR"),
        pytest.param("float={float}", "float=123.456"),
        pytest.param("float={float:.02f}", "float=123.46"),
        pytest.param("mix={mix[2].m2a[1].m_2_a_1_a}", "mix=m 2 s 1 a"),
        pytest.param("mix={mix[2].m2a[1].m_2_a_1_a:>15}", "mix=      m 2 s 1 a"),
        pytest.param("dt={dt:%Y%m%d%H%M%S.%f}", "dt=20260424171053.123456"),
    ]
)
def test_format(expr, expect, data_1):
    """書式指定"""
    ret = format_map(expr=expr, mapping=data_1)
    assert ret == expect
    assert type(ret) == type(expect)




@pytest.mark.parametrize(
    [
        "expr", "expect",
    ],
    [
        pytest.param("{str}", "STR"),
        pytest.param("{int}", 123),
        pytest.param("{float}", 123.456),
        pytest.param("{dt}", datetime(year=2026, month=4, day=24, hour=17, minute=10, second=53, microsecond=123456)),
        pytest.param("{float}", 123.456),
        pytest.param("{mix[2].m2a[1]}", {"m_2_a_1_a": "m 2 s 1 a"}),
    ]
)
def test_original_type(expr, expect, data_1):
    """オリジナルタイプ"""

    ret = format_map(expr=expr, mapping=data_1, original_type=True)
    assert ret == expect
    assert type(ret) == type(expect)



@pytest.mark.parametrize(
    [
        "expr", "expect",
    ],
    [
        # 可能
        pytest.param("{int}", 123),
        pytest.param("{int + 1.5}", 124.5),

        # 単一プレースホルダー以外はNG
        pytest.param("_{int}", "_123"),
        pytest.param("{int}_", "123_"),
        pytest.param("{int}{int}", "123123"),
    ]
)
def test_original_type_restorable(expr, expect, data_1):
    """オリジナルタイプ変換可否"""

    ret = format_map(expr=expr, mapping=data_1, original_type=True)
    assert ret == expect
    assert type(ret) == type(expect)





@pytest.mark.parametrize(
    [
        "expr", "expect",
    ],
    [
        pytest.param("{int + 100}", 223),
        # pytest.param("{int(float) + 100}", 223),  # 関数は不可。f-string方式なら使えるが…
    ]
)
def test_calc(expr, expect, data_1):
    """計算"""

    ret = format_map(expr=expr, mapping=data_1, original_type=True)
    assert ret == expect
    assert type(ret) == type(expect)



@pytest.mark.parametrize(
    [
        "expr", "expect",
    ],
    [
        pytest.param("-{str}-", "-STR-"),
        pytest.param("-{{str}}-", "-{str}-"),
        pytest.param("-{{unknown}}-", "-{unknown}-"),
    ]
)
def test_escape(expr, expect, data_1):
    """エスケープ"""

    ret = format_map(expr=expr, mapping=data_1)
    assert ret == expect
    assert type(ret) == type(expect)



