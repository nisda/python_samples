import pytest
from format_ex import format_map
from datetime import datetime



@pytest.mark.parametrize(
    [
        "expr", "original_type"
    ],
    [
        pytest.param("{b}", False),     # str.format_map 失敗
        pytest.param("{b}", True),      # eval 失敗
    ]
)
def test_error_raise(expr, original_type):
    """エラー時: Exception"""

    mapping_dict = { "a" : {} }

    with pytest.raises(Exception) as e:
        ret = format_map(expr=expr, mapping=mapping_dict, original_type=original_type, errors='raise')


@pytest.mark.parametrize(
    [
        "expr", "original_type"
    ],
    [
        pytest.param("{b}", False),     # str.format_map 失敗
        pytest.param("{b}", True),      # eval 失敗
    ]
)
def test_error_coerce(expr, original_type):
    """エラー時: coerce（None）"""

    mapping_dict = { "a" : {} }

    ret = format_map(expr=expr, mapping=mapping_dict, original_type=original_type, errors='coerce')
    assert ret == None


@pytest.mark.parametrize(
    [
        "expr", "original_type"
    ],
    [
        pytest.param("{b}", False),     # str.format_map 失敗
        pytest.param("{b}", True),      # eval 失敗
    ]
)
def test_error_ignore(expr, original_type):
    """エラー時: ignore -> 変更しない"""

    mapping_dict = { "a" : {} }

    ret = format_map(expr=expr, mapping=mapping_dict, original_type=original_type, errors='ignore')
    assert ret == expr
