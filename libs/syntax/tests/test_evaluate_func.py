import pytest
import re

from syntax import Evaluater




SAFE_FUNCTIONS = {
    "my_func": lambda x, y, z='Z': f"{x}-{y}-{z}",
    "str": None,
    "int": None,
    "list": None,
    "len": None,
    "map": None,
    "unknown": None,
}



@pytest.mark.parametrize(
    ["expr", "expected"],
    [
        pytest.param("my_func('a', 12, 'x')", 'a-12-x'),
        pytest.param("my_func('a', 12)", 'a-12-Z'),
        pytest.param("int('12345')", 12345),
        pytest.param("int('100') * int('20') == 2000", True),
        pytest.param("int('100') * int('20') == 2001", False),
        pytest.param("len([0, 0, 0, 0])", 4),
        pytest.param("list(map(str, [0, 0, 0, 0]))", ["0", "0", "0", "0"]),

        # f-string 内
        pytest.param("f\"{len([0, 0, 0, 0])}\"", "4"),
        pytest.param("f\"text {len([0, 0, 0, 0])} text\"", "text 4 text"),
    ]
)
def test_evaluate_func(expr, expected):
    """正常系"""

    evaluate = Evaluater(funcs=SAFE_FUNCTIONS)

    ret = evaluate.eval(expr, mapping=None)
    assert ret == expected



@pytest.mark.parametrize(
    ["expr", "e_type", "e_msg"],
    [
        # func に未設定の既存function
        pytest.param("float('123.45')", PermissionError, "execution of `float` is not permitted."),

        # func に設定されているが存在しない function
        pytest.param("unknown('123.45')", NameError, "function 'unknown' is not defined"),

        # f-string 内
        pytest.param("f\"{float(123)}\"", PermissionError, "execution of `float` is not permitted."),
        pytest.param("f\"text {unknown([0, 0, 0, 0])} text\"", NameError, "function 'unknown' is not defined"),
    ]
)
def test_evaluate_error(expr, e_type, e_msg):
    """異常系"""

    evaluate = Evaluater(funcs=SAFE_FUNCTIONS)

    with pytest.raises(Exception) as e:
        ret = evaluate.eval(expr, mapping=None)

    assert e.type           == e_type
    assert e.value.args[0]  == e_msg

