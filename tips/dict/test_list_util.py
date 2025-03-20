import pytest

import decimal
import uuid
from datetime import time, date, datetime
import mylibs.list_util as list_util



@pytest.mark.parametrize(
    ["expect", "left", "right"],
    [
        # 同値。
        pytest.param( 0, [],  []),
        pytest.param( 0, [20],  [20]),
        pytest.param( 0, [20, 300, 4000],  [20, 300, 4000]),
        pytest.param( 0, ["20", 300, True, 123.45, date(2024, 10, 23)],  ["20", 300, True, 123.45, date(2024, 10, 23)]),
        # 値に差異あり
        pytest.param(-1, ["19", 300, True, 123.45, date(2024, 10, 23)],  ["20", 300, True, 123.45, date(2024, 10, 23)]),
        pytest.param(-1, ["20", 299, True, 123.45, date(2024, 10, 23)],  ["20", 300, True, 123.45, date(2024, 10, 23)]),
        pytest.param(-1, ["20", 300, False,123.45, date(2024, 10, 23)],  ["20", 300, True, 123.45, date(2024, 10, 23)]),
        pytest.param(-1, ["20", 300, True, 123.44, date(2024, 10, 23)],  ["20", 300, True, 123.45, date(2024, 10, 23)]),
        pytest.param(-1, ["20", 300, True, 123.45, date(2024, 10, 22)],  ["20", 300, True, 123.45, date(2024, 10, 23)]),
        # 数値は型が違っても比較可能
        pytest.param( 0, [20, 300, 4000, 5000.5],  [20, float(300.0), decimal.Decimal(4000), decimal.Decimal(5000.5)]),
        pytest.param(-1, [20, 300, 4000, 5000.5],  [21, float(300.0), decimal.Decimal(4000), decimal.Decimal(5000.5)]),
        pytest.param(-1, [20, 300, 4000, 5000.5],  [20, float(300.1), decimal.Decimal(4000), decimal.Decimal(5000.5)]),
        pytest.param(-1, [20, 300, 4000, 5000.5],  [20, float(300.0), decimal.Decimal(4001), decimal.Decimal(5000.5)]),
        pytest.param(-1, [20, 300, 4000, 5000.5],  [20, float(300.0), decimal.Decimal(4000), decimal.Decimal(5000.9)]),
        pytest.param( 1, [20, 300, 4000, 5000.5],  [19, float(300.0), decimal.Decimal(4000), decimal.Decimal(5000.5)]),
        pytest.param( 1, [20, 300, 4000, 5000.5],  [20, float(299.9), decimal.Decimal(4000), decimal.Decimal(5000.5)]),
        pytest.param( 1, [20, 300, 4000, 5000.5],  [20, float(300.0), decimal.Decimal(3999), decimal.Decimal(5000.5)]),
        pytest.param( 1, [20, 300, 4000, 5000.5],  [20, float(300.0), decimal.Decimal(4000), decimal.Decimal(5000.4)]),
        # 型違い
        pytest.param(-1, [20, 300, 4000],  [20, "aaa", 4000]),
        pytest.param(-1, [20, 300, 4000],  [20, "300", 4000]),
        pytest.param(-1, [20, 300, 4000],  [20, 300, False]),
        pytest.param(-1, [20, 300, 4000],  [20, uuid.uuid4(), 4000]),
        pytest.param(-1, [20, 300, 4000],  [date(2024, 10, 22), 300, 4000]),
        # 要素数
        pytest.param(-1, [20, 300, 4000],  [20, 300, 4000, 50000]),
        pytest.param(-1, [20, 300, "aa"],  [20, 300, "aa", 50000]),
        pytest.param(-1, [20, 300, "aa"],  [20, 300, "aa", 50000, 600000]),
        pytest.param(-1, [],  [20, 300, 4000, 50000]),
        # 要素数よりも値と型が優先
        pytest.param(-1, [20, 300, 4000, 9999, 9999],  [20, "aaa", 4000]),
        pytest.param(-1, [20, 300, 4000, 9999, 9999],  [20, "300", 4000]),
        pytest.param(-1, [20, 300, 4000, 9999, 9999],  [20, 300, False]),
        pytest.param(-1, [20, 300, 4000, 9999, 9999],  [20, uuid.uuid4(), 4000]),
        pytest.param(-1, [20, 300, 4000, 9999, 9999],  [date(2024, 10, 22), 300, 4000]),
    ]
)
def test_list_compare(left, right, expect):
    ret = list_util.compare(list_left=left, list_right=right)
    assert ret == expect

    # 左右反転
    ret = list_util.compare(list_left=right, list_right=left)
    assert ret == expect * -1




@pytest.mark.parametrize(
    ["data", "expect"],
    [
        # 同値。
        pytest.param( [],  []),
        pytest.param( [20],  [20]),
        pytest.param( ["22", 301, "200", 123.4, date(2024, 10, 23), "200", 300, True, 123.45],
                      [123.4, 123.45, 300, 301, True, "200", "200", "22", date(2024, 10, 23)]),
    ]
)
def test_list_sort(data, expect):
    ret = list_util.list_sort(data=data)
    assert ret == expect



@pytest.mark.parametrize(
    ["data", "expect"],
    [
        pytest.param([],  []),
        pytest.param(
            [
                ["mm", True, 101, "xx"],
                ["aaa", True, 333],
                ["mm", True, 100],
                ["a", False, 999],
                ["mm", True, 101, date(2024, 12, 31)],
                ["mm", True, 101, 1],
                ["mm", True, 101, "zz"],
                ["a", True, 333],
                ["mm", True, 101, date(2024, 10, 1)],
                ["mm", True, 101],
                ["zzz", False],
                ["mm", True, 101, "zz"],
            ],
            [
                ["a", False, 999],
                ["a", True, 333],
                ["aaa", True, 333],
                ["mm", True, 100],
                ["mm", True, 101],
                ["mm", True, 101, 1],
                ["mm", True, 101, "xx"],
                ["mm", True, 101, "zz"],
                ["mm", True, 101, "zz"],
                ["mm", True, 101, date(2024, 10, 1)],
                ["mm", True, 101, date(2024, 12, 31)],
                ["zzz", False],
            ]
        ),
    ]
)
def test_list_list_sort(data, expect):
    ret = list_util.list_list_sort(data=data)
    assert ret == expect

