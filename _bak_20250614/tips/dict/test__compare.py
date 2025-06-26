
from mylibs import dict_util
import pytest


@pytest.mark.parametrize(
    ["compare_paths", "expect"],
    [
        pytest.param([["a"]], True),
        pytest.param([["b"]], True),
        pytest.param([["c"]], False),
        pytest.param([["a"], ["b"]], True),
        pytest.param([["a"], ["c"]], False),
    ]
)
def test_compare_basic(compare_paths, expect):

    data_left = {
        "a" : "A",
        "b" : "B",
        "c" : "C",
    }
    data_right = {
        "a" : "A",
        "b" : "B",
        "c" : "X",
    }

    ret = dict_util.compare(dict_left=data_left, dict_right=data_right, compare_paths=compare_paths)
    assert ret == expect




@pytest.mark.parametrize(
    ["compare_paths", "expect"],
    [
        pytest.param([["a"], ["b", "ba"]], True),
        pytest.param([["a"], ["b", "ba"], ["b", "bb", "bbb"]], True),
        pytest.param([["a"], ["b", "ba"], ["b", "bb", "bbc"]], False),
    ]
)
def test_compare_depth(compare_paths, expect):

    data_left = {
        "a" : "A",
        "b" : {
            "ba" : "BA",
            "bb" : {
                "bba" : "BBA",
                "bbb" : "BBB",
                "bbc" : "BBC",
            }
        },
    }
    data_right = {
        "a" : "A",
        "b" : {
            "ba" : "BA",
            "bb" : {
                "bba" : "BBA",
                "bbb" : "BBB",
                "bbc" : "XXX",
            }
        },
    }

    ret = dict_util.compare(dict_left=data_left, dict_right=data_right, compare_paths=compare_paths)
    assert ret == expect


@pytest.mark.parametrize(
    ["compare_paths", "expect"],
    [
        pytest.param([["a"], ["b", 0]], True),
        pytest.param([["a"], ["b", 1]], False),
        pytest.param([["a"], ["b", 2, "b31"]], True),
        pytest.param([["a"], ["b", 2, "b33"]], False),
    ]
)
def test_compare_list(compare_paths, expect):

    data_left = {
        "a" : "A",
        "b" : [
            "b1",
            2,
            {
                "b31" : "B31",
                "b32" : "B32",
                "b33" : 333,
            }
        ],
    }
    data_right = {
        "a" : "A",
        "b" : [
            "b1",
            22,
            {
                "b31" : "B31",
                "b32" : "B32",
                "b33" : "999",
            }
        ],
    }

    ret = dict_util.compare(dict_left=data_left, dict_right=data_right, compare_paths=compare_paths)
    assert ret == expect



@pytest.mark.parametrize(
    ["compare_paths", "expect"],
    [
        pytest.param([["a"], "b.0"], True),
        pytest.param([["a"], "b.1"], False),
        pytest.param([["a"], "b.2.b31"], True),
        pytest.param([["a"], "b.2.b33"], False),
    ]
)
def test_compare_str_path_default(compare_paths, expect):

    data_left = {
        "a" : "A",
        "b" : [
            "b1",
            2,
            {
                "b31" : "B31",
                "b32" : "B32",
                "b33" : 333,
            }
        ],
    }
    data_right = {
        "a" : "A",
        "b" : [
            "b1",
            22,
            {
                "b31" : "B31",
                "b32" : "B32",
                "b33" : "999",
            }
        ],
    }

    ret = dict_util.compare(dict_left=data_left, dict_right=data_right, compare_paths=compare_paths)
    assert ret == expect




@pytest.mark.parametrize(
    ["compare_paths", "path_separator", "expect"],
    [
        pytest.param([["a"], "b//0"]     , "//", True),
        pytest.param([["a"], "b//1"]     , "//", False),
        pytest.param([["a"], "b//2//b31"] , "//", True),
        pytest.param([["a"], "b//2//b33"] , "//", False),
    ]
)
def test_compare_str_path_separator(compare_paths, path_separator, expect):

    data_left = {
        "a" : "A",
        "b" : [
            "b1",
            2,
            {
                "b31" : "B31",
                "b32" : "B32",
                "b33" : 333,
            }
        ],
    }
    data_right = {
        "a" : "A",
        "b" : [
            "b1",
            22,
            {
                "b31" : "B31",
                "b32" : "B32",
                "b33" : "999",
            }
        ],
    }

    ret = dict_util.compare(
        dict_left=data_left,
        dict_right=data_right,
        compare_paths=compare_paths,
        path_separator=path_separator,
        )
    assert ret == expect


