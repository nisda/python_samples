
import mylibs.dict_util as dict_util
import pytest


@pytest.mark.parametrize(
    ["input", "expect"],
    [
        pytest.param("",  []),
        pytest.param(None,  []),
        pytest.param("abc",  []),
        pytest.param([],  []),
        pytest.param({},  []),
        pytest.param((),  []),
        pytest.param(["a", "b", "c"],  [[0], [1], [2]]),
        pytest.param({"A": 1, "B": {"B1": {"B1a": 2, "B1b": 3}} }, [["A"], ["B", "B1", "B1a"], ["B", "B1", "B1b"]]),
        pytest.param(
            {"A": 1, "B": [2, 3, {"B3": 4, "B4": [5, 6]}]},
            [["A"], ["B", 0], ["B", 1], ["B", 2, "B3"], ["B", 2, "B4", 0], ["B", 2, "B4", 1]]
        ),
    ]
)
def test_get_paths(expect, input):
    ret = dict_util.paths(data=input)
    assert expect == ret

