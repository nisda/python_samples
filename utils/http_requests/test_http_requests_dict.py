from myutils.http_requests import CaseInsensitiveDict


def test_to_case_insensitive_dict():
    # 初期化
    params: dict = CaseInsensitiveDict({
        "AAA": "origin `AAA`",
        "BBB": "origin `BBB`",
        "CCC": "origin `CCC`",
        111: "origin `111`",
    })
    # 変更
    params["aAa"] = "updated `123`"

    # 結果確認

    assert params == {
        "aaa": "updated `123`",
        "bbb": "origin `BBB`",
        "ccc": "origin `CCC`",
        111: "origin `111`",
    }

    assert params["aaa"] == "updated `123`"
    assert params["AAA"] == "updated `123`"
    assert params.get("AAA") == "updated `123`"


def test_dict_convert_to_case_insensitive_dict():
    orogin: dict = {'AaA': 123, 'BBB': "qwe"}
    params: dict = CaseInsensitiveDict(orogin)

    assert params["aaa"] == 123
    assert params["aAa"] == 123
    assert params.get("aAa") == 123
