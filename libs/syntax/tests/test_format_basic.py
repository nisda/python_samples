import pytest
from datetime import datetime
from decimal import Decimal
from syntax import Evaluater


SAFE_FUNCTIONS = {
    "my_func": lambda x: x,
    "str": None,
    "int": None,
    "list": None,
    "len": None,
    "map": None,
    "unknown": None,
}



@pytest.mark.parametrize(
    [
        "expr", "expect",
    ],
    [

        pytest.param("a", "a"),
        pytest.param("{a}", -1234.56,),
        pytest.param("{a:0>10}", "00-1234.56",),
        pytest.param("a{a}", "a-1234.56"),
        pytest.param("a{a:0>10}", "a00-1234.56",),
        pytest.param("{a}_{a}", "-1234.56_-1234.56",),
        pytest.param("my_func(a)", "my_func(a)"),
        pytest.param("{my_func(a)}", -1234.56),
        pytest.param("{my_func(x=a)}_", "-1234.56_"),
        pytest.param("{my_func(x={})}", {}),
        pytest.param("{my_func(x={'a': 1})}", {'a': 1}),
        # pytest.param("{{my_func(x={'a':1})}}", "{my_func(x={'a':1})}"),   # 対応不可。:1 の format_spec扱いで。
        pytest.param("{{ {my_func(x={'a': 1})} }}", "{ {'a': 1} }"),

   ]
)
def test_deep_access(expr, expect):
    INPUT_DATA = {
        "a": -1234.56,
    }


    evaluater = Evaluater(funcs=SAFE_FUNCTIONS)
    ret = evaluater.format(expr, mapping=INPUT_DATA)
    assert ret == expect
    assert type(ret) == type(expect)


