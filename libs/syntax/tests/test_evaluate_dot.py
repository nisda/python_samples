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



"""ドットアクセス"""
@pytest.mark.parametrize(
    ["expr", "expected"],
    [
        # pytest.param("a['aa']['aaa']", 'AAA'),
        pytest.param("a.aa.aaa", 'AAA'),
        pytest.param("b[0]", 'B0'),
        pytest.param("c.ca[0].ca0a[0].ca0a0a", "CA0A0A"),
        pytest.param("c.ca[0].ca0a[0]", { "ca0a0a": "CA0A0A" }),
        pytest.param("c.ca[0].ca0a", ({ "ca0a0a": "CA0A0A" },)),

        # f-string
        pytest.param("f\"{c.ca[0].ca0a[0].ca0a0a:_<10}\"", "CA0A0A____"),
        pytest.param("f\"text `{c.ca[0].ca0a[0].ca0a0a:.>10}` text\"", "text `....CA0A0A` text"),
    ]
)
def test_dot(expr, expected):
    """ドットアクセス"""

    evaluate = Evaluater()

    ret = evaluate.eval(expr, mapping=CONTEXT)
    assert ret == expected



"""メソッド"""
@pytest.mark.parametrize(
    ["expr", "expected"],
    [
        # pytest.param("a['aa']['aaa']", 'AAA'),
        pytest.param("a.aa.get('aaa')", 'AAA'),
    ]
)
def test_method(expr, expected):
    """
    メソッド
    """

    evaluate = Evaluater()

    ret = evaluate.eval(expr, mapping=CONTEXT)
    assert ret == expected

