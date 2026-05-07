import pytest
import re
from types import SimpleNamespace

from syntax import Evaluater




@pytest.mark.parametrize(
    ["expr", "expected"],
    [

        # Literal
        pytest.param("None", None),
        pytest.param("123.456", 123.456),
        pytest.param("'123.456'", "123.456"),
        pytest.param("'a'", "a"),
        pytest.param("r'a'", "a"),
        pytest.param("True", True),

        # List / Tuple / Dict / Set
        pytest.param("[0, 1, 'a', 'b']", [0, 1, 'a', 'b']),
        pytest.param("(0, 1, 'a', 'b')", (0, 1, 'a', 'b')),
        pytest.param("{'aaa': 'AAA', 0: 0, '1': 1}", {'aaa': 'AAA', 0: 0, '1': 1}),
        pytest.param("{'a', 'b', 'c'}", {'a', 'b', 'c'}),

        # 単項演算
        pytest.param("-123.456", -123.456),
        pytest.param("not True", False),
        pytest.param("not False", True),

        # 二項演算
        pytest.param("2 + 3", 5),
        pytest.param("2 * 4 % 3", 2),
        pytest.param("2-(2**3)", -6),

        # 比較
        pytest.param("2 == 2", True),
        pytest.param("2 != 2", False),
        pytest.param("2 == 2 < 2.1",True ),
        pytest.param("2 == 2 < 2.1 >= 2.2", False),

        # 論理演算
        pytest.param("2 <  3 and 'a' == 'a'", True),
        pytest.param("2 <  3 and 'a' == 'b'", False),
        pytest.param("2 < -3 and 'a' == 'a'", False),
        pytest.param("2 < -3 or  'a' == 'a'", True),
        pytest.param("2 < -3 or  'a' == 'b'", False),

        # 論理演算＋順番
        pytest.param("1 == 1 and ('a' == 'b' or 'A' == 'A')", True),
        pytest.param("1 == -1 and ('a' == 'b' or 'A' == 'A')", False),
        pytest.param("1 == 1 and ('a' == 'b' or 'A' == 'B')", False),
        pytest.param("1 == 1 and not ('a' == 'b' or 'A' == 'B')", True),

        # 添え字
        pytest.param("a", "A"),
        pytest.param("b['ba']", {"baa" : "BAA"}),
        pytest.param("c[0]['a'][2]['c0a2a']", "C0A2A"),

        # 添え字 + Slice
        pytest.param("c[0]['a'][0:2]", ("C0A0", "C0A1")),

        # function
        pytest.param("int('-123')", -123),

        # method/property
        pytest.param("d.prop1", "Sample.Propery1"),
        pytest.param("d.method1(123, 'abc')", "Sample.Method1.123+abc"),
        pytest.param("e.ea.eaa", "EAA"),
        pytest.param("'ABCDE'.lower().split('c')", ["ab", "de"]),

        # format
        pytest.param("'__{a}__{b}__'.format(a='X', b='Y')", "__X__Y__"),
        pytest.param("'float: {a:0>10.{b}f}'.format(a=123.45, b=4)", "float: 00123.4500"),

        # f-srting
        pytest.param("f'__{a}__'", "__A__"),
        pytest.param("f'[{f:0>15,.4f}]'", "[000-12,345.6700]"),
        pytest.param("f'[{{f:0>15,.4f}}]'", "[{f:0>15,.4f}]"),      # escape
        pytest.param("f'[{{{f:0>15,.4f}}}]'", "[{000-12,345.6700}]"),

    ]
)
def test_evaluate(expr, expected):

    class SampleClass():
        @property
        def prop1(self) -> str:
            return "Sample.Propery1"

        def method1(self, value1, value2) -> str:
            return f"Sample.Method1.{value1}+{value2}"



    data = {
        "a" : "A",
        "b" : {
            "ba" : {
                "baa" : "BAA",
            }
        },
        "c" : [
            {
                "a" : (
                    "C0A0",
                    "C0A1",
                    { "c0a2a" : "C0A2A"},
                )
            }
        ],
        "d" : SampleClass(),
        "e" : SimpleNamespace(**{
            "ea" : SimpleNamespace(**{
                "eaa": "EAA"
            })
        }),
        "f" : -12345.67,
    }
    # ret = evaluate_entrance(expr=expr, mapping=data)
    # assert ret == expected

    ret = Evaluater().eval(expr, mapping=data)
    assert ret == expected



