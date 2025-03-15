import pytest
import datetime
import decimal
import uuid

import mylibs.json as json

@pytest.mark.parametrize(
    ["input", "expect_type", "expect_value"],
    [
        pytest.param(datetime.datetime(2025, 2, 15, 12, 34, 56)         , str, "2025-02-15T12:34:56"),
        pytest.param(datetime.time(12, 34, 56)                          , str, "12:34:56"),
        pytest.param(decimal.Decimal(123)                               , int, 123),
        pytest.param(decimal.Decimal(123.45)                            , float, 123.45),
        pytest.param(uuid.UUID("93035c19-d9bb-4c69-8785-5463ec60a3df")  , str, "93035c19-d9bb-4c69-8785-5463ec60a3df"),
    ]
)
def test_json_serialize(input, expect_type, expect_value):
    json_str = json.dumps(input)
    ret = json.loads(json_str)
    assert isinstance(ret, expect_type)
    assert expect_value == ret

def test_json_sort():
    input  = {"c": "789", "a": "1234", "b": "852"}
    expect = {"a": "1234", "b": "852", "c": "789"}

    input_str = json.dumps(input, sort_keys=False)
    sorted_str = json.dumps(input, sort_keys=True)
    expect_str = json.dumps(expect)

    assert input_str  != sorted_str
    assert input_str  != expect_str
    assert sorted_str == expect_str

