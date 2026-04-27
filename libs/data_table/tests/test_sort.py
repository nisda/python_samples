import pytest
from data_table import DataTable
from pprint import pprint



def test_sort():
    """行指向データ(dict)の読み込み"""

    data = [
        {"id": 1, "name": "Alice", "sex": "F"},
        {"id": 2, "sex": None, "name": "Bob", "age": 22},
        {"name": "Charlie", "id": 3, "sex": "M", "age": None},
    ]

    # カラム、データの確認
    dt = DataTable(data=data)
    rows = list(dt.rows())
    assert dt.columns == ["id", "name", "sex", "age"]
    assert len(rows) == len(data)

    # sex でソート
    dt = dt.sort(sort_by=["sex"])
    rows = list(dt.rows())
    assert dt.columns == ["id", "name", "sex", "age"]
    assert len(rows) == len(data)
    assert rows[0]["id"] == 2
    assert rows[1]["id"] == 1
    assert rows[2]["id"] == 3

    # age, sex でソート
    dt = dt.sort(sort_by=["age", "sex"])
    rows = list(dt.rows())
    assert dt.columns == ["id", "name", "sex", "age"]
    assert len(rows) == len(data)
    assert rows[0]["id"] == 3
    assert rows[1]["id"] == 1
    assert rows[2]["id"] == 2



