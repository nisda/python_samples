import pytest
from typing import Final
from json_ex import JsonEx

from datetime import datetime
from decimal import Decimal
from uuid import uuid4
import os

SCRIPT_PATH:Final[str] = os.path.dirname(__file__)
INPUT_PATH:Final[str] = os.path.join(SCRIPT_PATH, "_test_data", "sample.jsonc")

def test_loads():


    # 想定結果
    expected = {
        "id" : "00001", 
        "color" : "yellow",
        "price" : 100,
        "country": ["Philippines", "Indonesia"]  
    }

    # 実行
    ret = JsonEx.load(INPUT_PATH)
    assert ret == expected

