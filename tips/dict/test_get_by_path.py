
import mylibs.dict_util as dict_util
import pytest


@pytest.mark.parametrize(
    ["path", "expect"],
    [
        pytest.param(["A"],  1),
        pytest.param(["B", "BA"], 2),
        pytest.param(["B", "BB", "BBA"],  3),
        pytest.param(["B", "BB", "BBB"],  4),
        pytest.param(["B", "BB"],  {"BBA": 3, "BBB": 4}),
    ]
)
def test_dict_data(path, expect):
    input: dict = {
        "A" : 1,
        "B" : {
            "BA" : 2,
            "BB" : {
                "BBA" : 3,
                "BBB" : 4,
            }
        }
    }
    ret = dict_util.get_by_path(data=input, path=path)
    assert expect == ret


@pytest.mark.parametrize(
    ["path", "expect"],
    [
        pytest.param([0],  0),
        pytest.param([1, 0],  10),
        pytest.param([1, 1],  11),
        pytest.param([2, 0, 0],  200),
        pytest.param([2, 0],  [200,201]),
        pytest.param([2, 1],  21),
        pytest.param([2, 2],  [220]),
    ]
)
def test_list_data(path, expect):
    input: dict = [
        0,
        [10, 11],
        [
            [200, 201],
            21,
            [220],
        ],
    ]
    ret = dict_util.get_by_path(data=input, path=path)
    assert expect == ret


@pytest.mark.parametrize(
    ["path", "expect"],
    [
        pytest.param([0],  0),
        pytest.param([1, 0],  10),
        pytest.param([1, 1],  11),
        pytest.param([2, 0, 0],  200),
        pytest.param([2, 0],  (200,201)),
        pytest.param([2, 1],  21),
        pytest.param([2, 2],  (220)),
    ]
)
def test_tuple_data(path, expect):
    input: dict = (
        0,
        (10, 11),
        (
            (200, 201),
            21,
            (220),
        ),
    )
    ret = dict_util.get_by_path(data=input, path=path)
    assert expect == ret



@pytest.mark.parametrize(
    ["path", "expect"],
    [
        pytest.param(["A", 0, "A1", 0, "A1A"],  "ABC!"),
    ]
)
def test_mix_data(path, expect):
    input: dict = {
        "A" : [
            {
                "A1" : (
                    {
                        "A1A" : "ABC!"
                    },
                ),
            },
        ],
    }
    ret = dict_util.get_by_path(data=input, path=path)
    assert expect == ret


@pytest.mark.parametrize(
    ["path", "expect"],
    [
        pytest.param([],  {"A": "AAA!"}),
    ]
)
def test_empty_path(path, expect):
    input: dict = {
        "A" : "AAA!"
    }
    ret = dict_util.get_by_path(data=input, path=path)
    assert expect == ret

