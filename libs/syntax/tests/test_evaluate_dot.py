import pytest
import re

from syntax import Evaluater


CONTEXT = {
    "a" : {"aa" : {"aaa": "AAA"}},
    "b" : ["B0", "B1"],
    "c" : {
        "ca": [
            {
                "ca0a" : (
                    { "ca0a0a": "CA0A0A" },
                )
            }
        ]
    }
}

@pytest.mark.parametrize(
    ["expr", "expected"],
    [
        # pytest.param("a['aa']['aaa']", 'AAA'),
        pytest.param("a.aa.aaa", 'AAA'),
        pytest.param("b[0]", 'B0'),
        pytest.param("c.ca[0].ca0a[0].ca0a0a", "CA0A0A"),
        pytest.param("c.ca[0].ca0a[0]", { "ca0a0a": "CA0A0A" }),
        pytest.param("c.ca[0].ca0a", ({ "ca0a0a": "CA0A0A" },)),
    ]
)
def test_evaluate_func(expr, expected):


    evaluate = Evaluater()

    ret = evaluate.evaluate(expr=expr, context=CONTEXT)
    assert ret == expected

