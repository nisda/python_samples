import pytest
from data_table import DataTable
from pprint import pprint



def test_filter():
    """行指向データ(dict)の読み込み"""

    data = [
        {"id": 1, "name": "Alice", "sex": "F"},
        {"id": 2, "sex": None, "name": "Bob", "age": 22},
        {"name": "Charlie", "id": 3, "sex": "M", "age": None},
    ]

    # カラム、データの確認
    dt = DataTable(data=data)

    # 単一条件
    ret = dt.filter(match_with={"id": 3})
    rows = ret.rows(type='dict')
    assert len(rows) == 1
    assert rows[0]["id"] == 3

    # IN条件
    ret = dt.filter(match_with={"id": [1, 3]})
    rows = ret.rows(type='dict')
    assert len(rows) == 2
    assert rows[0]["id"] == 1
    assert rows[1]["id"] == 3

    # 複数条件（AND）
    ret = dt.filter(match_with={"id": [1, 2], "age": 22})
    rows = ret.rows(type='dict')
    assert len(rows) == 1
    assert rows[0]["id"] == 2

    # 複数条件（AND）別パターン
    ret = dt.filter(match_with={"id": [1, 2], "age": None})
    rows = ret.rows(type='dict')
    assert len(rows) == 1
    assert rows[0]["id"] == 1

    # 複数条件（OR)
    ret = dt.filter(match_with=[{"id": [1, 2], "age": None}, {"sex": "M"}])
    rows = ret.rows(type='dict')
    assert len(rows) == 2
    assert rows[0]["id"] == 1
    assert rows[1]["id"] == 3



def test_match_mismatch():


    data = [
        {"id": 1, "name": "Alice", "sex": "F", "age": 18},
        {"id": 2, "name": "Bob", "sex": "M", "age": 22},
        {"id": 3, "name": "Charlie", "sex": "M", "age": None},
        {"id": 4, "name": "Denis", "sex": "M", "age": 18},
    ]

    # カラム、データの確認
    dt = DataTable(data=data)

    # match のみ
    rows = dt.filter(match_with={"age": 18}).rows(type='dict')
    assert len(rows) == 2
    assert rows[0]["id"] == 1
    assert rows[1]["id"] == 4

    # mismatch のみ
    rows = dt.filter(mismatch_with={"age": None}).rows(type='dict')
    assert len(rows) == 3
    assert rows[0]["id"] == 1
    assert rows[1]["id"] == 2
    assert rows[2]["id"] == 4

    # match + mismatch
    rows = dt.filter(match_with={"sex": "M"}, mismatch_with={"age": None}).rows(type='dict')
    assert len(rows) == 2
    assert rows[0]["id"] == 2
    assert rows[1]["id"] == 4

