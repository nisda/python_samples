import pytest
from json_ex import JsonEx

from datetime import datetime
from decimal import Decimal
from uuid import uuid4
import os


def test_dumps():

    # 入力
    input_obj = {
        # 一部データ型を抜粋してテスト
        "str": "日本語",
        "int": 123,
        "decimal": Decimal("-1.234"),
        "datetime" : datetime(2025, 12, 26, 12, 34, 56, 123456),
    }

    # 想定結果
    expected = """
{
  "str": "日本語",
  "int": 123,
  "decimal": "Decimal('-1.234')",
  "datetime": "datetime.datetime(2025, 12, 26, 12, 34, 56, 123456)"
}
""".strip()

    # 実行
    ret = JsonEx.dumps(input_obj)
    assert ret == expected

