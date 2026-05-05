import pytest
from typing import Final
from json_ex import JsonEx

from datetime import datetime
from decimal import Decimal
from uuid import uuid4
import os

SCRIPT_PATH:Final[str] = os.path.dirname(__file__)
OUTPUT_PATH:Final[str] = os.path.join(SCRIPT_PATH, "_test_data", "output.json")

def test_loads():


    # 入力値
    input_obj = {
        "id" : "00001", 
        "color" : "yellow",
        "price" : 100,
        "rate"  : Decimal("1.64"), 
        "date"  : datetime(2025, 12, 26).date(),
    }

    # 想定結果
    excepted = """
{
  "id": "00001",
  "color": "yellow",
  "price": 100,
  "rate": "Decimal('1.64')",
  "date": "datetime.date(2025, 12, 26)"
}
""".strip()


    # ファイル事前削除
    os.remove(OUTPUT_PATH)
    assert not os.path.isfile(OUTPUT_PATH)


    # 実行
    JsonEx.dump(input_obj, path=OUTPUT_PATH)


    # 結果取得＆比較
    assert os.path.isfile(OUTPUT_PATH)
    with open(OUTPUT_PATH, "r") as f:
        content = f.read()
    assert content == excepted
