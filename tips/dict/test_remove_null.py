import mylibs.dict_util as dict_util



def test_remove_null():
    original_input:dict = {
        "a" : "AAA",
        "b" : None,
        "c" : {
            "ca" : "CCC/AAA",
            "cb" : None,
            "cc" : "CCC/CCC",
        },
    }
    ret = dict_util.remove_null(data=original_input)

    assert list(ret.keys()) == ["a", "c"]
    assert list(ret["c"].keys()) == ["ca", "cc"]



def test_remove_null_ignore_list():
    original_input:dict = {
        "a" : "AAA",
        "b" : [1, 2, None, 4],
    }
    ret = dict_util.remove_null(data=original_input)

    assert ret['b'] == [1, 2, None, 4]
