
import mylibs.dict_util as dict_util
import pytest
import re


@pytest.mark.parametrize(
    ["expected", "input"],
    [
        pytest.param(True,  {"del" : False, "name" : "apple", "price" : 100,}, id="match"),
        pytest.param(True,  {"del" : False, "name" : "apple", "price" : 100, "quantity": 100}, id="contain"),
        pytest.param(False, {"del" : True,  "name" : "apple", "price" : 100, "quantity": 100}, id="del unmatch"),
        pytest.param(False, {"del" : False, "name" : "apple", "price" : 200,}, id="price unmatch"),
        pytest.param(False, {"del" : False, "name" : "banana", "price" : 100,}, id="name unmatch"),
    ]
)
def test_simple_value(expected, input):
    """単純な値の比較"""
    condition:dict = {
        "name" : "apple",
        "price" : 100,
        "del" : False,
    }
    ret = dict_util.is_contains(data=input, condition=condition)
    assert expected == ret


@pytest.mark.parametrize(
    ["expected", "input"],
    [
        pytest.param(True,  {"name" : "apple tea", "price" : 100,}, id="match"),
        pytest.param(False, {"name" : "banana", "price" : 300,}, id="unmatch"),
        pytest.param(False, {"name" : "apple", "price" : 100,}, id="unmatch: short"),
        pytest.param(False, {"name" : "green apple", "price" : 200,}, id="unmatch: not a prefix match"),
    ]
)
def test_regular_expression(expected, input):
    """正規表現の比較"""
    condition:dict = {
        "name" : re.compile(r'^apple(.+)'),
    }
    ret = dict_util.is_contains(data=input, condition=condition)
    assert expected == ret


@pytest.mark.parametrize(
    ["expected", "input"],
    [
        pytest.param(True,  {"name" : "apple tea",   "price" : 200,}, id="match"),
        pytest.param(False, {"name" : "banana",      "price" : 149,}, id="unmatch: value < range"),
        pytest.param(False, {"name" : "green apple", "price" : 251,}, id="unmatch: range < value"),
    ]
)
def test_funciton(expected, input):
    """ファンクションでの判定"""

    def __in_range(value, range_from:int, range_to:int) -> bool:
        return (range_from <= value and value <= range_to)

    condition:dict = {
        "price" : lambda v :__in_range(value=v, range_from=150, range_to=250)
    }
    ret = dict_util.is_contains(data=input, condition=condition)
    assert expected == ret


@pytest.mark.parametrize(
    ["expected", "input"],
    [
        pytest.param(False,  {"name" : "aaa", "category" : 2}               , id="01"),
        pytest.param(True,   {"name" : "aaa", "category" : 3}               , id="02"),
        pytest.param(False,  {"name" : "ccc", "category" : [2]}             , id="03"),
        pytest.param(True,   {"name" : "ccc", "category" : [3]}             , id="04"),
        pytest.param(False,  {"name" : "ccc", "category" : [1, 2]}          , id="05"),
        pytest.param(True,   {"name" : "ccc", "category" : [2, 3]}          , id="06"),
        pytest.param(True,   {"name" : "ccc", "category" : [3, 4]}          , id="07"),
        pytest.param(True,   {"name" : "ccc", "category" : [4, 5]}          , id="08"),
        pytest.param(False,  {"name" : "ccc", "category" : [5, 6]}          , id="09"),
        pytest.param(True,   {"name" : "ccc", "category" : [1, 2, 3]}       , id="10"),
        pytest.param(True,   {"name" : "ccc", "category" : [2, 3, 4]}       , id="11"),
        pytest.param(True,   {"name" : "ccc", "category" : [3, 4, 5]}       , id="12"),
        pytest.param(True,   {"name" : "ccc", "category" : [4, 5, 6]}       , id="13"),
        pytest.param(False,  {"name" : "ccc", "category" : [5, 6, 7]}       , id="14"),
        pytest.param(False,  {"name" : "ccc", "category" : []}              , id="15"),
    ]
)
def test_multi_value_any_included(expected, input):
    """リストの判定（１つ以上が候補に含まれている）"""

    condition:dict = {
        "category" : [3, 4]
    }
    ret = dict_util.is_contains(
        data=input,
        condition=condition,
    )
    assert expected == ret

