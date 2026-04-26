import pytest

from typing import Tuple, Any, List, Dict, Type, Callable, Literal
from datetime import datetime, date, time, tzinfo
from zoneinfo import ZoneInfo
from decimal import Decimal
from uuid import uuid4, UUID
from pprint import pprint

from data_converter import DataConverter


"""文字列から変換"""
@pytest.mark.parametrize(
    ["value", "dtype", "params", "expected"],
    [

        # str
        pytest.param("-123.456", str, None, "-123.456"),
        # pytest.param("-123.456", str, {"format": " >10"}, "-123.456"),

        # decimal
        pytest.param("123", Decimal, None, Decimal("123")),
        pytest.param("123.456", Decimal, None, Decimal("123.456")),
        pytest.param("123.456", Decimal, {"digit":0}, Decimal("123")),
        pytest.param("123.456", Decimal, {"digit":0, "rounding": "round"}, Decimal("123")),
        pytest.param("123.456", Decimal, {"digit":0, "rounding": "floor"}, Decimal("123")),
        pytest.param("123.456", Decimal, {"digit":0, "rounding": "ceil"}, Decimal("124")),
        pytest.param("123.456", Decimal, {"digit":2, "rounding": "round"}, Decimal("123.46")),
        pytest.param("123.456", Decimal, {"digit":2, "rounding": "floor"}, Decimal("123.45")),
        pytest.param("123.456", Decimal, {"digit":2, "rounding": "ceil"}, Decimal("123.46")),
        pytest.param("-123.456", Decimal, None, Decimal("-123.456")),
        pytest.param("-123.456", Decimal, {"digit":0}, Decimal("-123")),
        pytest.param("-123.456", Decimal, {"digit":1, "rounding": "round"}, Decimal("-123.5")),
        pytest.param("-123.456", Decimal, {"digit":1, "rounding": "floor"}, Decimal("-123.5")),
        pytest.param("-123.456", Decimal, {"digit":1, "rounding": "ceil"}, Decimal("-123.4")),

        # float
        pytest.param("123", float, None, 123.0),
        pytest.param("123.456", float, None, 123.456),
        pytest.param("123.456", float, {"digit":0}, 123.0),
        pytest.param("123.456", float, {"digit":0, "rounding": "round"}, 123.0),
        pytest.param("123.456", float, {"digit":0, "rounding": "floor"}, 123.0),
        pytest.param("123.456", float, {"digit":0, "rounding": "ceil"}, 124.0),
        pytest.param("123.456", float, {"digit":2, "rounding": "round"}, 123.46),
        pytest.param("123.456", float, {"digit":2, "rounding": "floor"}, 123.45),
        pytest.param("123.456", float, {"digit":2, "rounding": "ceil"}, 123.46),
        pytest.param("-123.456", float, None, -123.456),
        pytest.param("-123.456", float, {"digit":0}, -123.0),
        pytest.param("-123.456", float, {"digit":1, "rounding": "round"}, -123.5),
        pytest.param("-123.456", float, {"digit":1, "rounding": "floor"}, -123.5),
        pytest.param("-123.456", float, {"digit":1, "rounding": "ceil"}, -123.4),

        # int
        pytest.param("123", int, None, 123),
        pytest.param("123.456", int, None, 123),
        pytest.param("123.456", int, {"rounding": "round"}, 123),
        pytest.param("123.456", int, {"rounding": "floor"}, 123),
        pytest.param("123.456", int, {"rounding": "ceil"}, 124),
        pytest.param("-123.456", int, {"rounding": "round"}, -123),
        pytest.param("-123.456", int, {"rounding": "floor"}, -124),
        pytest.param("-123.456", int, {"rounding": "ceil"}, -123),

        # bool
        pytest.param("a", bool, None, True),
        pytest.param("1", bool, None, True),
        pytest.param("0", bool, None, True),
        pytest.param("", bool, None, False),
        pytest.param("True", bool, None, True),
        pytest.param("False", bool, None, False),
        pytest.param("true", bool, None, True),
        pytest.param("false", bool, None, False),


        # uuid
        pytest.param("4469dc17-209e-fb7f-c44a-65397f9e1023", UUID, None, UUID("4469dc17-209e-fb7f-c44a-65397f9e1023")),


        # datetime
        pytest.param("2024-12-31T12:34:56.123456", datetime, None, datetime(2024, 12, 31, 12, 34, 56, 123456)),
        pytest.param("2024-12-31T12:34:56.123456Z", datetime, None, datetime(2024, 12, 31, 12, 34, 56, 123456, tzinfo=ZoneInfo("UTC"))),
        pytest.param("2024-12-31T12:34:56.123456+00:00", datetime, None, datetime(2024, 12, 31, 12, 34, 56, 123456, tzinfo=ZoneInfo("UTC"))),
        pytest.param("2024-12-31 12:34:56+09:00", datetime, None, datetime(2024, 12, 31, 12, 34, 56, 0, tzinfo=ZoneInfo("Asia/Tokyo"))),
        pytest.param("2024-12-31 12:34:56", datetime, None, datetime(2024, 12, 31, 12, 34, 56)),
        pytest.param("2024-12-31", datetime, None, datetime(2024, 12, 31, 0, 0, 0)),
        pytest.param("2024-12-31T12:34:56.123456Z", datetime, {"format": "iso"}, datetime(2024, 12, 31, 12, 34, 56, 123456, tzinfo=ZoneInfo("UTC"))),
        pytest.param("2024/12/31 12.34.56", datetime, {"format": r"%Y/%m/%d %H.%M.%S"}, datetime(2024, 12, 31, 12, 34, 56, 0)),
        pytest.param("2024/12/31 12.34.56 123456 +09:00", datetime, {"format": r"%Y/%m/%d %H.%M.%S %f %z"}, datetime(2024, 12, 31, 12, 34, 56, 123456, tzinfo=ZoneInfo("Asia/Tokyo"))),

        # date
        pytest.param("2024-12-31T01:34:56.123456+00:00", date, None, date(2024, 12, 31)),
        pytest.param("2024-12-31T12:34:56.123456-09:00", date, None, date(2024, 12, 31)),
        pytest.param("2024-12-31T23:34:56.123456+09:00", date, None, date(2024, 12, 31)),
        pytest.param("2024-12-31", date, None, date(2024, 12, 31)),
        pytest.param("2024-12-31", date, {"format": "iso"}, date(2024, 12, 31)),
        pytest.param("April 26, 2026", date, {"format": r"%B %d, %Y"}, date(2026, 4, 26)),
        pytest.param("1201", date, {"format": r"%m%d"}, date(1900, 12, 1)),

        # time
        pytest.param("01:34:56", time, None, time( 1, 34, 56)),
        pytest.param("1:34:56", time, None, time( 1, 34, 56)),
        pytest.param("2359", time, {"format": r"%H%M"}, time(23, 59, 0)),
        pytest.param("2024-12-31T23:34:56.123456+09:00", time, {"format": "iso"}, time(23, 34, 56, 123456)),
        pytest.param("2024-12-31 12:34:56", time, {"format": "iso"}, time(12, 34, 56)),

        # bytes
        pytest.param("abcde_12345", bytes, None, b'abcde_12345'),
        pytest.param("あいうえお", bytes, None, b'\xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88\xe3\x81\x8a'), 
        pytest.param("あいうえお", bytes, {"encoding": "utf-8"}, b'\xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88\xe3\x81\x8a'), 
        pytest.param("あいうえお", bytes, {"encoding": "sjis"}, b'\x82\xa0\x82\xa2\x82\xa4\x82\xa6\x82\xa8'),
    ]
)
def test_str(value:Any, dtype:Type, params:Any, expected:Any):
    """文字列から変換"""

    ret = DataConverter.convert(value=value, dtype=dtype, params=params)
    assert expected == ret
    assert type(expected) == type(ret)



"""Decimalから変換"""
@pytest.mark.parametrize(
    ["value", "dtype", "params", "expected"],
    [

        # str
        pytest.param(Decimal("-123"), str, None, "-123"),
        pytest.param(Decimal("-123.0"), str, None, "-123.0"),
        pytest.param(Decimal("-123.456"), str, None, "-123.456"),

        # decimal
        pytest.param(Decimal("-123.456"), Decimal, None, Decimal("-123.456")),
        pytest.param(Decimal("123.456"), Decimal, {"digit":0}, Decimal("123")),
        pytest.param(Decimal("123.456"), Decimal, {"digit":2, "rounding": "floor"}, Decimal("123.45")),
        pytest.param(Decimal("123.456"), Decimal, {"digit":2, "rounding": "ceil"}, Decimal("123.46")),
        pytest.param(Decimal("-123.456"), Decimal, {"digit":1, "rounding": "round"}, Decimal("-123.5")),
        pytest.param(Decimal("-123.456"), Decimal, {"digit":1, "rounding": "floor"}, Decimal("-123.5")),

        # float
        pytest.param(Decimal("123"), float, None, 123.0),
        pytest.param(Decimal("123.456"), float, None, 123.456),
        pytest.param(Decimal("123.456"), float, {"digit":0}, 123.0),
        pytest.param(Decimal("123.456"), float, {"digit":0, "rounding": "round"}, 123.0),
        pytest.param(Decimal("123.456"), float, {"digit":0, "rounding": "floor"}, 123.0),
        pytest.param(Decimal("123.456"), float, {"digit":0, "rounding": "ceil"}, 124.0),
        pytest.param(Decimal("123.456"), float, {"digit":2, "rounding": "round"}, 123.46),
        pytest.param(Decimal("123.456"), float, {"digit":2, "rounding": "floor"}, 123.45),
        pytest.param(Decimal("123.456"), float, {"digit":2, "rounding": "ceil"}, 123.46),
        pytest.param(Decimal("-123.456"), float, None, -123.456),
        pytest.param(Decimal("-123.456"), float, {"digit":0}, -123.0),
        pytest.param(Decimal("-123.456"), float, {"digit":1, "rounding": "round"}, -123.5),
        pytest.param(Decimal("-123.456"), float, {"digit":1, "rounding": "floor"}, -123.5),
        pytest.param(Decimal("-123.456"), float, {"digit":1, "rounding": "ceil"}, -123.4),

        # int
        pytest.param(Decimal("123"), int, None, 123),
        pytest.param(Decimal("123.456"), int, None, 123),
        pytest.param(Decimal("123.456"), int, {"rounding": "round"}, 123),
        pytest.param(Decimal("123.456"), int, {"rounding": "floor"}, 123),
        pytest.param(Decimal("123.456"), int, {"rounding": "ceil"}, 124),
        pytest.param(Decimal("-123.456"), int, {"rounding": "round"}, -123),
        pytest.param(Decimal("-123.456"), int, {"rounding": "floor"}, -124),
        pytest.param(Decimal("-123.456"), int, {"rounding": "ceil"}, -123),

        # bool
        pytest.param(Decimal("-123.456"), bool, None, True),
        pytest.param(Decimal("0"), bool, None, False),
        pytest.param(Decimal(), bool, None, False),

        # -- NG --
        # uuid
        # datetime
        # date
        # time
        # bytes
    ]
)
def test_decimal(value:Any, dtype:Type, params:Any, expected:Any):
    """decimalから変換"""

    ret = DataConverter.convert(value=value, dtype=dtype, params=params)
    assert expected == ret
    assert type(expected) == type(ret)



"""floatから変換"""
@pytest.mark.parametrize(
    ["value", "dtype", "params", "expected"],
    [

        # str
        pytest.param(float("-123"), str, None, "-123.0"),
        pytest.param(float("-123.0"), str, None, "-123.0"),
        pytest.param(float("-123.456"), str, None, "-123.456"),

        # decimal
        pytest.param(float("-123.456"), Decimal, None, Decimal("-123.456")),
        pytest.param(float("123.456"), Decimal, {"digit":0}, Decimal("123")),
        pytest.param(float("123.456"), Decimal, {"digit":2, "rounding": "floor"}, Decimal("123.45")),
        pytest.param(float("123.456"), Decimal, {"digit":2, "rounding": "ceil"}, Decimal("123.46")),
        pytest.param(float("-123.456"), Decimal, {"digit":1, "rounding": "round"}, Decimal("-123.5")),
        pytest.param(float("-123.456"), Decimal, {"digit":1, "rounding": "floor"}, Decimal("-123.5")),

        # float
        pytest.param(float("123"), float, None, 123.0),
        pytest.param(float("123.456"), float, None, 123.456),
        pytest.param(float("123.456"), float, {"digit":0}, 123.0),
        pytest.param(float("123.456"), float, {"digit":0, "rounding": "round"}, 123.0),
        pytest.param(float("123.456"), float, {"digit":0, "rounding": "floor"}, 123.0),
        pytest.param(float("123.456"), float, {"digit":0, "rounding": "ceil"}, 124.0),
        pytest.param(float("123.456"), float, {"digit":2, "rounding": "round"}, 123.46),
        pytest.param(float("123.456"), float, {"digit":2, "rounding": "floor"}, 123.45),
        pytest.param(float("123.456"), float, {"digit":2, "rounding": "ceil"}, 123.46),
        pytest.param(float("-123.456"), float, None, -123.456),
        pytest.param(float("-123.456"), float, {"digit":0}, -123.0),
        pytest.param(float("-123.456"), float, {"digit":1, "rounding": "round"}, -123.5),
        pytest.param(float("-123.456"), float, {"digit":1, "rounding": "floor"}, -123.5),
        pytest.param(float("-123.456"), float, {"digit":1, "rounding": "ceil"}, -123.4),

        # int
        pytest.param(float("123"), int, None, 123),
        pytest.param(float("123.456"), int, None, 123),
        pytest.param(float("123.456"), int, {"rounding": "round"}, 123),
        pytest.param(float("123.456"), int, {"rounding": "floor"}, 123),
        pytest.param(float("123.456"), int, {"rounding": "ceil"}, 124),
        pytest.param(float("-123.456"), int, {"rounding": "round"}, -123),
        pytest.param(float("-123.456"), int, {"rounding": "floor"}, -124),
        pytest.param(float("-123.456"), int, {"rounding": "ceil"}, -123),

        # bool
        pytest.param(float("-123.456"), bool, None, True),
        pytest.param(float("0"), bool, None, False),
        pytest.param(float(), bool, None, False),

        # -- NG --
        # uuid
        # datetime
        # date
        # time
        # bytes
    ]
)
def test_float(value:Any, dtype:Type, params:Any, expected:Any):
    """floatから変換"""

    ret = DataConverter.convert(value=value, dtype=dtype, params=params)
    assert expected == ret
    assert type(expected) == type(ret)



"""intから変換"""
@pytest.mark.parametrize(
    ["value", "dtype", "params", "expected"],
    [

        # str
        pytest.param(123, str, None, "123"),
        pytest.param(-123, str, None, "-123"),

        # decimal
        pytest.param(123, Decimal, None, Decimal(123)),
        pytest.param(-123, Decimal, None, Decimal(-123)),

        # # float
        pytest.param(123, float, None, float(123)),
        pytest.param(-123, float, None, float(-123)),

        # # int
        pytest.param(-123, int, None, -123),

        # bool
        pytest.param(123, bool, None, True),
        pytest.param(-1, bool, None, True),
        pytest.param(0, bool, None, False),

        # -- NG --
        # uuid
        # date
        # time

        # bytes -> 別枠で
    ]
)
def test_int(value:Any, dtype:Type, params:Any, expected:Any):
    """intから変換"""

    ret = DataConverter.convert(value=value, dtype=dtype, params=params)
    assert expected == ret
    assert type(expected) == type(ret)




"""datetimeから変換"""
@pytest.mark.parametrize(
    ["value", "dtype", "params", "expected"],
    [

        # str: formatは別枠で実施
        pytest.param(datetime(2024, 12, 31, 12, 34, 56, 0), str, None, "2024-12-31T12:34:56"),
        pytest.param(datetime(2024, 12, 31, 12, 34, 56, 123456), str, None, "2024-12-31T12:34:56.123456"),
        pytest.param(datetime(2024, 12, 31, 12, 34, 56, 123456, tzinfo=ZoneInfo("UTC")), str, None, "2024-12-31T12:34:56.123456+00:00"),
        pytest.param(datetime(2024, 12, 31, 12, 34, 56, 0, tzinfo=ZoneInfo("Asia/Tokyo")), str, None, "2024-12-31T12:34:56+09:00"),

        # bool
        pytest.param(datetime(2024, 12, 31, 12, 34, 56, 123456), bool, None, True),


        ## -- 別枠で実施
        # Decimal
        # float
        # int

        # datetime
        pytest.param(datetime(2024, 12, 31, 12, 34, 56, 123456, tzinfo=ZoneInfo("UTC")), datetime, None,
                     datetime(2024, 12, 31, 12, 34, 56, 123456, tzinfo=ZoneInfo("UTC"))),


        # datetime(tz編集, TZ未設定 -> TZ変更)
        pytest.param(datetime(2024, 12, 31, 20, 34, 56, 123456), datetime, {"base_tz": None , "tz": None},
                     datetime(2024, 12, 31, 20, 34, 56, 123456)),
        pytest.param(datetime(2024, 12, 31, 20, 34, 56, 123456), datetime, {"base_tz": "UTC" , "tz": None},
                     datetime(2024, 12, 31, 20, 34, 56, 123456, tzinfo=ZoneInfo("UTC"))),
        pytest.param(datetime(2024, 12, 31, 20, 34, 56, 123456), datetime, {"base_tz": "UTC" , "tz": "Asia/Tokyo"},
                     datetime(2025,  1,  1,  5, 34, 56, 123456, tzinfo=ZoneInfo("Asia/Tokyo"))),

        # datetime(tz編集, TZ設定済み -> TZ変更)
        pytest.param(datetime(2024, 12, 31, 20, 34, 56, 123456, tzinfo=ZoneInfo("UTC")), datetime, {"base_tz": None , "tz": None},
                     datetime(2024, 12, 31, 20, 34, 56, 123456, tzinfo=ZoneInfo("UTC"))),
        pytest.param(datetime(2024, 12, 31, 20, 34, 56, 123456, tzinfo=ZoneInfo("UTC")), datetime, {"base_tz": "Asia/Tokyo" , "tz": None},
                     datetime(2024, 12, 31, 20, 34, 56, 123456, tzinfo=ZoneInfo("UTC"))),
        pytest.param(datetime(2024, 12, 31, 20, 34, 56, 123456, tzinfo=ZoneInfo("UTC")), datetime, {"base_tz": None, "tz": "Asia/Tokyo"},
                     datetime(2025,  1,  1,  5, 34, 56, 123456, tzinfo=ZoneInfo("Asia/Tokyo"))),

        # date
        pytest.param(datetime(2024, 12, 31, 20, 34, 56, 123456, tzinfo=ZoneInfo("UTC")), date, None, date(2024, 12, 31)),
        pytest.param(datetime(2024, 12, 31, 20, 34, 56, 123456, tzinfo=ZoneInfo("Asia/Tokyo")), date, None, date(2024, 12, 31)),

        # time
        pytest.param(datetime(2024, 12, 31, 20, 34, 56, 123456, tzinfo=ZoneInfo("UTC")), time, None, time( 20, 34, 56, 123456)),
        pytest.param(datetime(2024, 12, 31, 20, 34, 56,      0, tzinfo=ZoneInfo("UTC")), time, None, time( 20, 34, 56, 0)),
        pytest.param(datetime(2024, 12, 31, 20, 34, 56,      0, tzinfo=ZoneInfo("Asia/Tokyo")), time, None, time( 20, 34, 56, 0)),

        # bytes -> NG
    ]
)
def test_datetime(value:Any, dtype:Type, params:Any, expected:Any):
    """datetimeから変換"""

    ret = DataConverter.convert(value=value, dtype=dtype, params=params)
    assert expected == ret
    assert type(expected) == type(ret)



"""dateから変換"""
@pytest.mark.parametrize(
    ["value", "dtype", "params", "expected"],
    [

        # str: formatは別枠で実施
        pytest.param(date(2024, 12, 31), str, None, "2024-12-31"),

        # bool
        pytest.param(date(2024, 12, 31), bool, None, True),

        # ## -- 別枠で実施
        # # Decimal
        # # float
        # # int

        # datetime
        pytest.param(date(2024, 12, 31), datetime, None, datetime(2024, 12, 31, 0, 0, 0, 0)),

        # date
        pytest.param(date(2024, 12, 31), date, None, date(2024, 12, 31)),

        # time -> NG
        # bytes -> NG
    ]
)
def test_date(value:Any, dtype:Type, params:Any, expected:Any):
    """dateから変換"""

    ret = DataConverter.convert(value=value, dtype=dtype, params=params)
    assert expected == ret
    assert type(expected) == type(ret)



"""timeから変換"""
@pytest.mark.parametrize(
    ["value", "dtype", "params", "expected"],
    [

        # str: formatは別枠で実施
        pytest.param(time(9, 23, 45), str, None, "09:23:45"),
        pytest.param(time(9, 23, 45, 123456), str, None, "09:23:45.123456"),

        # bool
        pytest.param(time(9, 23, 45), bool, None, True),

        ## -- 別枠で実施
        # Decimal
        # float
        # int

        # datetime -> NG
        # date -> NG

        # time
        pytest.param(time(9, 23, 45), time, None, time(9, 23, 45)),

        # # bytes -> NG
    ]
)
def test_time(value:Any, dtype:Type, params:Any, expected:Any):
    """timeから変換"""

    ret = DataConverter.convert(value=value, dtype=dtype, params=params)
    assert expected == ret
    assert type(expected) == type(ret)



"""boolから変換"""
@pytest.mark.parametrize(
    ["value", "dtype", "params", "expected"],
    [

        # str: formatは別枠で実施
        pytest.param(True, str, None, "True"),
        pytest.param(False, str, None, "False"),

        # bool
        pytest.param(True, bool, None, True),
        pytest.param(False, bool, None, False),

        # Decimal
        pytest.param(True, Decimal, None, Decimal("1")),
        pytest.param(False, Decimal, None, Decimal("0")),

        # float
        pytest.param(True, float, None, float("1")),
        pytest.param(False, float, None, float("0")),

        # int
        pytest.param(True, int, None, 1),
        pytest.param(False, int, None, 0),

        # datetime -> NG
        # date -> NG
        # time -> NG

        # # bytes -> NG
        pytest.param(True, bytes, None, b'\x00'),
        pytest.param(False, bytes, None, b''),
    ]
)
def test_bool(value:Any, dtype:Type, params:Any, expected:Any):
    """boolから変換"""

    ret = DataConverter.convert(value=value, dtype=dtype, params=params)
    assert expected == ret
    assert type(expected) == type(ret)



"""uuidから変換"""
@pytest.mark.parametrize(
    ["value", "dtype", "params", "expected"],
    [

        # str
        pytest.param(UUID("4469dc17-209e-fb7f-c44a-65397f9e1023"), str, None, "4469dc17-209e-fb7f-c44a-65397f9e1023"),

        # bool
        pytest.param(UUID("4469dc17-209e-fb7f-c44a-65397f9e1023"), bool, None, True),

        # uuid
        pytest.param(UUID("4469dc17-209e-fb7f-c44a-65397f9e1023"), UUID, None, UUID("4469dc17-209e-fb7f-c44a-65397f9e1023")),

        # Decimal -> NG
        # float -> NG
        # int -> NG
        # datetime -> NG
        # date -> NG
        # time -> NG
        # bytes -> NG
    ]
)
def test_uuid(value:Any, dtype:Type, params:Any, expected:Any):
    """uuidから変換"""

    ret = DataConverter.convert(value=value, dtype=dtype, params=params)
    assert expected == ret
    assert type(expected) == type(ret)



"""bytesから変換"""
@pytest.mark.parametrize(
    ["value", "dtype", "params", "expected"],
    [

        # str
        pytest.param(b"abcde_12345", str, None, 'abcde_12345'),
        pytest.param(b'\xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88\xe3\x81\x8a', str, None, "あいうえお"), 
        pytest.param(b'\xe3\x81\x82\xe3\x81\x84\xe3\x81\x86\xe3\x81\x88\xe3\x81\x8a', str, {"encoding": "utf-8"}, "あいうえお"), 
        pytest.param(b'\x82\xa0\x82\xa2\x82\xa4\x82\xa6\x82\xa8', str, {"encoding": "sjis"}, "あいうえお"),

        # bool
        pytest.param(b'\x00', bool, None, True),
        pytest.param(b''    , bool, None, False),

        # Decimal -> NG
        # float -> NG

        # # datetime -> NG
        # # date -> NG
        # # time -> NG

        # bytes
        pytest.param(b''    , bytes, None, b''      ),
        pytest.param(b'\x03', bytes, None, b'\x03'  ),
    ]
)
def test_bytes(value:Any, dtype:Type, params:Any, expected:Any):
    """bytesから変換"""

    ret = DataConverter.convert(value=value, dtype=dtype, params=params)
    assert expected == ret
    assert type(expected) == type(ret)



""" bytes/int 変換"""
@pytest.mark.parametrize(
    ["value", "dtype", "params", "expected"],
    [
        pytest.param(0, bytes, None, b''),
        pytest.param(1, bytes, None, b'\x01'),
        pytest.param(3, bytes, None, b'\x03'),
        pytest.param(5000, bytes, {"byteorder":"big"   , "signed": True} , b'\x13\x88'),
        pytest.param(5000, bytes, {"byteorder":"little", "signed": False}, b'\x88\x13'),


        # int
        pytest.param(b'', int, None, 0),
        pytest.param(b'\x01', int, None, 1),
        pytest.param(b'\x03', int, None, 3),
        pytest.param(b'\x13\x88', int, {"byteorder":"big"   , "signed": True} , 5000),
        pytest.param(b'\x88\x13', int, {"byteorder":"little", "signed": False}, 5000),
    ]
)
def test_bytes_int(value:Any, dtype:Type, params:Any, expected:Any):
    """ bytes/int 変換"""

    ret = DataConverter.convert(value=value, dtype=dtype, params=params)
    assert expected == ret
    assert type(expected) == type(ret)



"""timestamp変換（float）"""
@pytest.mark.parametrize(
    ["value", "dtype", "params", "expected"],
    [

        # datetime -> int/Decimal/float(timestamp)
        pytest.param(datetime(2024, 12, 31, 12, 34, 56, 123456) , int    , None, 1735648496),
        pytest.param(datetime(2024, 12, 31, 12, 34, 56, 123456) , Decimal, None, Decimal(1735648496.123456)),
        pytest.param(datetime(2024, 12, 31, 12, 34, 56, 123456) , float  , None, float(1735648496.123456)),

        # int/Decimal/float(timestamp) -> datetime
        pytest.param(1735648496                     , datetime, None, datetime(2024, 12, 31, 12, 34, 56, 0)),
        pytest.param(Decimal("1735648496.123456")   , datetime, None, datetime(2024, 12, 31, 12, 34, 56, 123456)),
        pytest.param(float("1735648496.123456")     , datetime, None, datetime(2024, 12, 31, 12, 34, 56, 123456)),


        # date -> int/Decimal/float(timestamp)
        pytest.param(date(2024, 12, 31) , int    , None, 1735603200),
        pytest.param(date(2024, 12, 31) , Decimal, None, Decimal(1735603200)),
        pytest.param(date(2024, 12, 31) , float  , None, float(1735603200)),


        # datetime + timezone
        pytest.param(datetime(2024, 12, 31, 20, 34, 56, 123456, tzinfo=ZoneInfo("UTC"))         , float  , None, float(1735677296.123456)),
        pytest.param(datetime(2025,  1,  1,  5, 34, 56, 123456, tzinfo=ZoneInfo("Asia/Tokyo"))  , float  , None, float(1735677296.123456)),


    ]
)
def test_timestamp(value:Any, dtype:Type, params:Any, expected:Any):
    """timestamp変換（float）"""

    ret = DataConverter.convert(value=value, dtype=dtype, params=params)
    assert expected == ret
    assert type(expected) == type(ret)



"""文字列のformat"""
@pytest.mark.parametrize(
    ["value", "dtype", "params", "expected"],
    [

        # str -> str
        pytest.param("abcde", str, {"spec": " <10"}, "abcde     "),
        pytest.param("abcde", str, {"spec": "0>10"}, "00000abcde"),

        # Decimal -> str
        pytest.param(Decimal("-1234567.89"), str, {"spec": ",.05f"}, "-1,234,567.89000"),

        # float -> str
        pytest.param(float("-1234567.89"), str, {"spec": ",.05f"}, "-1,234,567.89000"),

        # int -> str
        pytest.param(-1234567, str, {"spec": ",.05f"}, "-1,234,567.00000"),

    ]
)
def test_str_format(value:Any, dtype:Type, params:Any, expected:Any):
    """文字列のformat"""

    ret = DataConverter.convert(value=value, dtype=dtype, params=params)
    assert expected == ret
    assert type(expected) == type(ret)




"""dtypeの文字列指定"""
@pytest.mark.parametrize(
    ["value", "dtype", "params", "expected"],
    [

        # str
        pytest.param("abcde", "str", None, "abcde"),

        # Decimal
        pytest.param("1234", "Decimal", None, Decimal("1234")),

        # float
        pytest.param("1234", "float", None, float("1234")),

        # int
        pytest.param("1234", "int", None, int("1234")),

        # datetime
        pytest.param("2026-04-05 12:34:56", "datetime", None, datetime(2026, 4, 5, 12, 34, 56)),
        
        # date
        pytest.param("2026-04-05", "date", None, date(2026, 4, 5)),

        # time
        pytest.param("12:34:56", "time", None, time(12, 34, 56)),

        # bool
        pytest.param("true", "bool", None, True),

        # uuid
        pytest.param("4469dc17-209e-fb7f-c44a-65397f9e1023", "UUID", None, UUID("4469dc17-209e-fb7f-c44a-65397f9e1023")),

        # bytes
        pytest.param("ABCDE", "bytes", None, b'ABCDE'),
    ]
)
def test_dtype_as_str(value:Any, dtype:str, params:Any, expected:Any):
    """文字列のformat"""

    ret = DataConverter.convert(value=value, dtype=dtype, params=params)
    assert expected == ret
    assert type(expected) == type(ret)








