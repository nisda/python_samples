
from mylibs import dict_util
import pytest

def test_dict_structure():

    paths = [
        ["a"],                  # 後続のパスに上書きされる（深いものが優先）
        ["a", "aa", "aaa"],
        ["a", "aa", "aab"],
        ["a", "aa"],            # 無視される（深いものが優先）
        ["b", "ba"],
        ["c"],
    ]
    ret = dict_util.dict_from_paths(paths=paths)

    assert ret == {
        "a" : {
            "aa" : {
                "aaa" : None,
                "aab" : None,
            },
        },
        "b" : {
            "ba" : None,
        },
        "c" : None,
    }


def test_empty():

    paths = []
    ret = dict_util.dict_from_paths(paths=paths)

    assert ret == {}


def test_valuse():

    paths = [
        ["a"],                  # 後続のパスに上書きされる（深いものが優先）
        ["a", "aa", "aaa"],
        ["a", "aa", "aab"],
        ["a", "aa"],            # 無視される（深いものが優先）
        ["b", "ba"],
        ["c"],
    ]
    values = [
        "A",    # 無視される
        "AAA",
        "AAB",
        "AA",   # 無視される。
        "BA",
        "C"
    ]
    ret = dict_util.dict_from_paths(paths=paths, values=values)

    assert ret == {
        "a" : {
            "aa" : {
                "aaa" : "AAA",
                "aab" : "AAB",
            },
        },
        "b" : {
            "ba" : "BA",
        },
        "c" : "C",
    }


def test_valuse_few():

    paths = [
        ["a", "ab", "aba"],
        ["a", "ab", "abb"],
        ["a", "aa"]
    ]
    values = [
        "ABA",
    ]
    ret = dict_util.dict_from_paths(paths=paths, values=values)

    # 渡した順番に割り当てられる
    assert ret == {
        "a" : {
            "aa" : None,
            "ab" : {
                "aba" : "ABA",
                "abb" : None,
            },
        },
    }


def test_valuse_many():

    paths = [
        ["a", "ab", "aba"],
        ["a", "ab", "abb"],
        ["a", "aa"]
    ]
    values = [
        "ABA",
        "ABB",
        "AA",
        "XX",
        "YY",
        "ZZ"
    ]
    ret = dict_util.dict_from_paths(paths=paths, values=values)

    # 渡した順番に割り当てられる
    assert ret == {
        "a" : {
            "aa" : "AA",
            "ab" : {
                "aba" : "ABA",
                "abb" : "ABB",
            },
        },
    }



@pytest.mark.parametrize(
    ["paths", "separator", "expect"],
    [
        pytest.param([["a"], ["b", "bb", "bbb"]], None, {"a": None, "b": {"bb" : {"bbb" : None}}}),
        pytest.param(["a", "b.bb.bbb"]          , "." , {"a": None, "b": {"bb" : {"bbb" : None}}}),
        pytest.param(["a", "b//bb//bbb"]        , "//", {"a": None, "b": {"bb" : {"bbb" : None}}}),
    ]
)
def test_separate_type(paths, separator, expect):

    ret = dict_util.dict_from_paths(paths=paths, path_separator=separator)
    assert ret == expect
