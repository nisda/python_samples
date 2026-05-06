import pytest
import re

from syntax import Evaluater


SAFE_FUNCTIONS = {
    "my_func": lambda x, y, z='Z': f"{x}-{y}-{z}",
    "int": None,
    "len": None,
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
    ]
)
def test_evaluate_func(expr, expected):

    evaluate = Evaluater(funcs=SAFE_FUNCTIONS)

    ret = evaluate.evaluate(expr=expr, context=None)
    assert ret == expected


@pytest.mark.parametrize(
    ["expr", "e_type", "e_msg"],
    [
        # func に未設定の既存function
        pytest.param("float('123.45')", PermissionError, "execution of `float` is not permitted."),

        # func に設定されているが存在しない function
        pytest.param("unknown('123.45')", NameError, "function 'unknown' is not defined"),
    ]
)
def test_evaluate_error(expr, e_type, e_msg):
    evaluate = Evaluater(funcs=SAFE_FUNCTIONS)

    with pytest.raises(Exception) as e:
        ret = evaluate.evaluate(expr=expr, context=None)

    assert e.type           == e_type
    assert e.value.args[0]  == e_msg

