import pytest
from typing import Dict, List, Any, Tuple
from format_ex import format_recursive
from datetime import datetime


# @pytest.mark.parametrize(
#     [
#         "expr", "expect",
#     ],
#     [
#         pytest.param("{int + 100}", 223),
#     ]
# )
def test_mix_template():
    """混合タイプ"""

    data_1:Dict = {
        "a" : {
            "aa" : [
                {"aa0a": "AA0A"}
            ]
        }
    }
    template:Dict = {
        "X1" : "__{a.aa[0].aa0a}__",
        "X2" : "a.aa[0].aa0a",
        "X3" : [
            "{a.aa[0].aa0a}",
            "{a.aa[0]}",
            (
                {"a": "{a.aa[0]}"},
            )
        ],
    }


    ret = format_recursive(template=template, mapping=data_1, original_type=True)
    assert ret["X1"] == "__AA0A__"
    assert ret["X2"] == "a.aa[0].aa0a"
    assert ret["X3"][0] == "AA0A"
    assert ret["X3"][1] == {"aa0a": "AA0A"}
    assert ret["X3"][2][0]["a"] == {"aa0a": "AA0A"}



def test_error_raise():
    """エラー： raise Exception"""

    data_1:Dict = {
        "a" : {
            "aa" : [
                {"aa0a": "AA0A"}
            ]
        }
    }
    template:Dict = {
        "X1" : "__{a.aa[0].aa0a}__",
        "X2" : "a.aa[0].aa0a",
        "X3" : [
            "{a.aa[0].aa0a.not_found}",
            "{a.aa[0]}",
            (
                {"a": "{a.aa[0]}"},
            )
        ],
    }

    with pytest.raises(Exception) as e:
        ret = format_recursive(template=template, mapping=data_1, original_type=True)



def test_error_coerce():
    """エラー: None変換"""

    data_1:Dict = {
        "a" : {
            "aa" : [
                {"aa0a": "AA0A"}
            ]
        }
    }
    template:Dict = {
        "X1" : "__{a.aa[0].aa0a}__",
        "X2" : "a.aa[0].aa0a",
        "X3" : [
            "{a.aa[0].aa0a.not_found}",
            "{a.aa[0]}",
            (
                {"a": "{a.aa[0]}"},
            )
        ],
    }

    ret = format_recursive(template=template, mapping=data_1, original_type=True, errors='coerce')
    assert ret["X1"] == "__AA0A__"
    assert ret["X2"] == "a.aa[0].aa0a"
    assert ret["X3"][0] == None                 # ここがformatエラー
    assert ret["X3"][1] == {"aa0a": "AA0A"}
    assert ret["X3"][2][0]["a"] == {"aa0a": "AA0A"}



def test_error_ignore():
    """エラー: 無変換"""

    data_1:Dict = {
        "a" : {
            "aa" : [
                {"aa0a": "AA0A"}
            ]
        }
    }
    template:Dict = {
        "X1" : "__{a.aa[0].aa0a}__",
        "X2" : "a.aa[0].aa0a",
        "X3" : [
            "{a.aa[0].aa0a.not_found}",
            "{a.aa[0]}",
            (
                {"a": "{a.aa[0]}"},
            )
        ],
    }

    ret = format_recursive(template=template, mapping=data_1, original_type=True, errors='ignore')
    assert ret["X1"] == "__AA0A__"
    assert ret["X2"] == "a.aa[0].aa0a"
    assert ret["X3"][0] == "{a.aa[0].aa0a.not_found}"            # ここがformatエラー
    assert ret["X3"][1] == {"aa0a": "AA0A"}
    assert ret["X3"][2][0]["a"] == {"aa0a": "AA0A"}

