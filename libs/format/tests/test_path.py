import pytest
from format_ex import format_map
from datetime import datetime
from format_ex.path_util import get_nested_data




@pytest.fixture
def data_dict() -> dict:
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

@pytest.fixture
def data_list() -> list:
    return [
        float(123.45),
        {"2a": "2A"}
    ]



@pytest.mark.parametrize(
    [
        "path", "expected",
    ],
    [
        pytest.param("str", "STR"),
        pytest.param("int", 123),
        pytest.param("float", 123.456),
        pytest.param("mix[2][m2a][1][m_2_a_1_a]", "m 2 s 1 a"),
        pytest.param("mix[2][m2a][1]", {"m_2_a_1_a": "m 2 s 1 a"}),
        pytest.param("mix.2.m2a.1.m_2_a_1_a", "m 2 s 1 a"),
        pytest.param("mix[2].m2a.1", {"m_2_a_1_a": "m 2 s 1 a"}),
    ]
)
def test_get_nested_from_dict(path, expected, data_dict):
    ret = get_nested_data(data_dict, path)
    assert ret == expected
    assert type(ret) == type(expected)


@pytest.mark.parametrize(
    [
        "path", "expected",
    ],
    [
        pytest.param("0", 123.45),
        pytest.param("1", {"2a": "2A"}),
        pytest.param("1.2a", "2A"),
        pytest.param("1[2a]", "2A"),
    ]
)
def test_get_nested_from_list(path, expected, data_list):
    ret = get_nested_data(data_list, path)
    assert ret == expected
    assert type(ret) == type(expected)




@pytest.mark.parametrize(
    [
        "data", "path", "expected",
    ],
    [
        pytest.param("A", "", "A"),
        pytest.param(1, "", 1),
        pytest.param(1, ".", 1),
    ]
)
def test_get_nested_from_scalar(data, path, expected):
    """スカラー値からパスで取得"""
    # 一応テストするけど、この使い方は想定していない

    ret = get_nested_data(data, path)
    assert ret == expected
    assert type(ret) == type(expected)





@pytest.mark.parametrize(
    [
        "path", "e_type", "e_msg"
    ],
    [
        # dict に存在しないキー
        pytest.param("b", KeyError, " at '. <dict>'"),
        pytest.param("a.a", KeyError, " at '.a <dict>'"),
        pytest.param("a.aa.0.aa1b", KeyError, " at '.a.aa.0 <dict>'"),

        # list に存在しないインデックス
        pytest.param("a.aa.1", IndexError, " at '.a.aa <list>'"),

        # tuple に存在しないインデックス
        pytest.param("a.ab.1", IndexError, " at '.a.ab <tuple>'"),

        # list に文字列
        pytest.param("a.aa.X", ValueError, " at '.a.aa <list>'"),

        # list, tupe, dict 以外にノード指定
        pytest.param("a.aa.0.aa1a.0", TypeError, " at '.a.aa.0.aa1a <str>'"),
    ]
)
def test_get_nested_from_dict(path, e_type, e_msg):

    data = {
        "a": {
            "aa" : [
                {"aa1a": "AA1A"}
            ],
            "ab" : (
                "AB0",
            )
        }
    }

    with pytest.raises(e_type) as e:
        ret = get_nested_data(data, path)
    assert e_msg in str(e)
    print(str(e))
