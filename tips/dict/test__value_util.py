import pytest

import decimal
import uuid
from datetime import time, date, datetime
import mylibs.value_util as value_util


@pytest.mark.parametrize(
    ["expect", "left", "right"],
    [
        # int, float, Decimal
        pytest.param( 0, 1,  float(1.0)),
        pytest.param(-1, 1, float(1.1)),
        pytest.param( 1, 2, float(1.2)),
        pytest.param( 0,  decimal.Decimal(2.5), float(2.5)),
        pytest.param(-1,  decimal.Decimal(2.5), float(2.7)),
        pytest.param( 1,  decimal.Decimal(2.51), float(2.5)),
        # bool
        pytest.param( 0,  True, True),
        pytest.param( 0,  False, False),
        pytest.param(-1,  False, True),
        pytest.param( 1,  True, False),
        # str
        pytest.param( 0,  "aaa", "aaa"),
        pytest.param(-1,  "aa", "aaa"),
        pytest.param( 1,  "aaa", "aa"),
        pytest.param(-1,  "aaa", "aab"),
        pytest.param( 1,  "aac", "aab"),
        pytest.param( 1,  "ac", "aab"),
        pytest.param(-1,  "aad", "ab"),
        # byte
        pytest.param( 0,  b"aaa", b"aaa"),
        pytest.param(-1,  b"aa", b"aaa"),
        pytest.param( 1,  b"aaa", b"aa"),
        pytest.param(-1,  b"aaa", b"aab"),
        pytest.param( 1,  b"aac", b"aab"),
        pytest.param( 1,  b"ac", b"aab"),
        pytest.param(-1,  b"aad", b"ab"),
        # UUID
        pytest.param( 0,  uuid.UUID('67f31d02-82ff-4d30-a884-88f37ee24227'), uuid.UUID('67f31d02-82ff-4d30-a884-88f37ee24227')),
        pytest.param(-1,  uuid.UUID('67f31d02-82ff-4d30-a884-88f37ee24227'), uuid.UUID('a2822322-2f07-44d5-8716-abcd37e921ce')),
        pytest.param( 1,  uuid.UUID('7354682c-e596-4aa7-b152-7917fd4d667e'), uuid.UUID('67f31d02-82ff-4d30-a884-88f37ee24227')),
        # undefined: time
        pytest.param( 0,  time(13, 20, 42), time(13, 20, 42)),
        pytest.param(-1,  time(13, 20, 41), time(13, 20, 42)),
        pytest.param( 1,  time(13, 20, 42), time(13, 19, 42)),
        # undefined: date
        pytest.param( 0,  date(2024, 7, 16), date(2024, 7, 16)),
        pytest.param(-1,  date(2024, 7, 15), date(2024, 7, 16)),
        pytest.param( 1,  date(2024, 7, 17), date(2024, 7, 16)),
        # undefined: datetime
        pytest.param( 0,  datetime(2024, 7, 16, 9, 42, 36), datetime(2024, 7, 16, 9, 42, 36)),
        pytest.param(-1,  datetime(2024, 7, 16, 9, 42, 36), datetime(2024, 7, 16, 9, 42, 37)),
        pytest.param( 1,  datetime(2024, 7, 16, 9, 42, 36), datetime(2024, 7, 16, 9, 42, 35)),
        # mix: num/bool
        pytest.param(-1, 0,  True),
        pytest.param(-1, 0,  False),
        # mix: num/str
        pytest.param(-1, 10,  "10"),
        pytest.param(-1, 10,  "9"),
        pytest.param(-1, decimal.Decimal(10.1),  "9"),
        pytest.param(-1, 10,  "a"),
        # mix: num/byte
        pytest.param(-1, 10,  b"10"),
        pytest.param(-1, 10,  b"9"),
        pytest.param(-1, decimal.Decimal(10.1),  b"9"),
        pytest.param(-1, 10,  b"a"),
        # mix: str/byte
        pytest.param(-1, "abc",  b"abc"),
        pytest.param(-1, "abc",  b"abcc"),
        pytest.param(-1, "abcc",  b"abcc"),
        # mix: str/UUID
        pytest.param(-1,  '67f31d02-82ff-4d30-a884-88f37ee24227', uuid.UUID('67f31d02-82ff-4d30-a884-88f37ee24227')),
        pytest.param(-1,  '67f31d02-82ff-4d30-a884-88f37ee24227', uuid.UUID('a2822322-2f07-44d5-8716-abcd37e921ce')),
        pytest.param(-1,  '7354682c-e596-4aa7-b152-7917fd4d667e', uuid.UUID('67f31d02-82ff-4d30-a884-88f37ee24227')),
        # mix: str/time
        pytest.param(-1, "235959",  time(13, 20, 42)),
        # mix: str/date
        pytest.param(-1, "20241231",  date(2024, 6, 27)),
        # mix: date/time
        pytest.param(-1, date(2024, 6, 27), time(13, 20, 42)),
        # mix: date/datetime
        pytest.param(-1, date(2024, 12, 31), datetime(2024, 1, 1, 1, 1, 1)),
        # mix: datetime/time
        pytest.param(-1, datetime(2024, 1, 1, 1, 1, 1), time(13, 20, 42)),
    ]
)
def test_value_compare(left, right, expect):
    ret = value_util.compare(value_left=left, value_right=right)
    assert ret == expect

    # 左右反転
    ret = value_util.compare(value_left=right, value_right=left)
    assert ret == expect * -1
