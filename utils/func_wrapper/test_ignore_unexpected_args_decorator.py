import pytest
from mylibs.func_wrapper import ignore_unexpected_args_decorator

#------------------------------------------------
# wrap target functions
#------------------------------------------------

@ignore_unexpected_args_decorator
def func_noargs():
    return {}


@ignore_unexpected_args_decorator
def func_fixed_args(p1, p2="OPT2", p3="OPT3", *, p101, p102="OPT102", p103="OPT103"):
    return {
        "p1" : p1,
        "p2" : p2,
        "p3" : p3,
        "p101" : p101,
        "p102" : p102,
        "p103" : p103,
    }


@ignore_unexpected_args_decorator
def func_flexible_args(p1, p2="OPT2", p3="OPT3", *args, p101, p102="OPT102", p103="OPT103", **kwargs):
    return {
        "p1" : p1,
        "p2" : p2,
        "p3" : p3,
        "p101" : p101,
        "p102" : p102,
        "p103" : p103,
        **{ i:args[i] for i in range(0, len(args)) },
        **kwargs,
    }


#------------------------------------------------
# pytest
#------------------------------------------------

@pytest.mark.parametrize(
    [
        "args",
        "kwargs",
        "expect",
    ],
    [
        pytest.param(
            [],
            {},
            {},
        ),
        pytest.param(
            [1, 2],
            {"kw1": "v1", "kw2": "v2"},
            {},
        ),
    ]
)
def test_func_noargs(args:list, kwargs:dict, expect:dict):
    ret = func_noargs(*args, **kwargs)
    assert expect == ret


@pytest.mark.parametrize(
    [
        "args",
        "kwargs",
        "expect",
    ],
    [
        pytest.param(
            ["a"],
            {"p101": "v1"},
            {
                "p1" : "a",
                "p2" : "OPT2",
                "p3" : "OPT3",
                "p101" : "v1",
                "p102" : "OPT102",
                "p103" : "OPT103",
            }
        ),
        pytest.param(
            ["a", "b", "c", "d", "e"],
            {"p101": "v1", "p102": "v2", "p104": "v4", "p105": "v5"},
            {
                "p1" : "a",
                "p2" : "b",
                "p3" : "c",
                "p101" : "v1",
                "p102" : "v2",
                "p103" : "OPT103",
            }
        ),
    ]
)
def test_func_fixed_args(args:list, kwargs:dict, expect:dict):
    ret = func_fixed_args(*args, **kwargs)
    assert expect == ret


@pytest.mark.parametrize(
    [
        "args",
        "kwargs",
        "expect",
    ],
    [
        pytest.param(
            ["a"],
            {"p101": "v1"},
            {
                "p1" : "a",
                "p2" : "OPT2",
                "p3" : "OPT3",
                "p101" : "v1",
                "p102" : "OPT102",
                "p103" : "OPT103",
            }
        ),
        pytest.param(
            ["a", "b", "c", "d", "e"],
            {"p101": "v1", "p102": "v2", "p104": "v4", "p105": "v5"},
            {
                "p1" : "a",
                "p2" : "b",
                "p3" : "c",
                0: "d",
                1: "e",
                "p101" : "v1",
                "p102" : "v2",
                "p103" : "OPT103",
                "p104" : "v4",
                "p105" : "v5",
            }
        ),
    ]
)
def test_func_flexible_args(args:list, kwargs:dict, expect:dict):
    ret = func_flexible_args(*args, **kwargs)
    assert expect == ret
