import pytest
from json_ex import JsonEx

from datetime import datetime
from decimal import Decimal
from uuid import uuid4
import os


def test_loads():

    # 入力（jsonc）
    input_str = """
{
  "str": "日本語",       // ダブルスラッシュ以降であるここは無視される
  // "int": 123,        // 先頭のダブルスラッシュにより行ごと無視される
  "float" : -234.56,
  "list"  : [
      "AAA",
      /* "BBB", */ "CCC",     // ブロックコメント部分は無視される。その外側は有効。
      "DDD",
      /*
      複数行のブロックコメント
      "EEE",
      "FFF",
      */
      "GGG"
  ],
  "comment in string" : [   // 文字列として扱う。コメントと見做さない。
      "aaa /* bbb */ bbb",
      "//aaa // bbb"
  ]
}
"""


    # 想定結果
    expected = {
        "str": "日本語",
        "float": -234.56,
        "list" : [
            "AAA",
            "CCC",
            "DDD",
            "GGG",
        ],
        "comment in string" : [
            "aaa /* bbb */ bbb",
            "//aaa // bbb"
        ]
    }

    # 実行
    ret = JsonEx.loads(input_str)
    assert ret == expected

