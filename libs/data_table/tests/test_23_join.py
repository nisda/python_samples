import pytest
from data_table import DataTable
from pprint import pprint
from typing import List, Dict


@pytest.fixture(scope="module")
def dt_1() -> DataTable:
    columns = ["seq", "fruits", "color"]
    data = [
        [1, "apple", "r"],
        [2, "berry", None],
        [3, "banana", "X"],
        [4, "lemon", "y"],
        [5, "apple", "r"],
    ]
    dt = DataTable(data=data, columns=columns)
    return dt


@pytest.fixture(scope="module")
def dt_2() -> DataTable:
    columns = ["price", "name", "color", "fullname"]
    data = [
        [100, "apple", "r", "apple"],
        [120, "apple", "y", "yellow apple"],
        [50, "banana", "y", "red apple"],
        [150, "tomato", "r", "tomato(ret)"],
        [120, "berry", "b", "brack berry"],
        [200, "berry", None, "unknown berry"],
    ]
    dt = DataTable(data=data, columns=columns)
    return dt

@pytest.fixture(scope="module")
def e_columns_1() -> List[str]:
    return [
        "left_seq",
        "left_fruits",
        "left_color",
    ]

@pytest.fixture(scope="module")
def e_columns_2() -> List[str]:
    return [
        "right_price",
        "right_name",
        "right_color",
        "right_fullname"
    ]



def test_cross_join(dt_1:DataTable, dt_2:DataTable, e_columns_1:List[str], e_columns_2:List[str]):
    """CROSS JOIN"""


    ret = dt_1.join(table=dt_2, how="cross")
    assert ret.columns == tuple(e_columns_1 + e_columns_2)
    assert ret.row_count == dt_1.row_count * dt_2.row_count



def test_inner_join(dt_1:DataTable, dt_2:DataTable, e_columns_1:List[str], e_columns_2:List[str]):
    """INNER JOIN"""

    ret = dt_1.join(table=dt_2, how="inner", left_on=["fruits", "color"], right_on=["name", "color"])
    rows = ret.rows(type='list')

    assert ret.columns == tuple(e_columns_1 + e_columns_2)
    assert ret.row_count == 3
    assert [1, "apple", "r", 100, "apple", "r", "apple"] in rows
    assert [2, "berry", None, 200, "berry", None, "unknown berry"] in rows
    assert [5, "apple", "r", 100, "apple", "r", "apple"] in rows


def test_left_join(dt_1:DataTable, dt_2:DataTable, e_columns_1:List[str], e_columns_2:List[str]):
    """LEFT JOIN"""

    ret = dt_1.join(table=dt_2, how="left",left_on=["fruits", "color"],right_on=["name", "color"])
    rows = ret.rows(type='list')

    assert ret.columns == tuple(e_columns_1 + e_columns_2)
    assert ret.row_count == 5
    assert [1, "apple", "r", 100, "apple", "r", "apple"] in rows
    assert [2, "berry", None, 200, "berry", None, "unknown berry"] in rows
    assert [3, "banana", "X", None, None, None, None] in rows
    assert [4, "lemon", "y", None, None, None, None] in rows
    assert [5, "apple", "r", 100, "apple", "r", "apple"] in rows


def test_right_join(dt_1:DataTable, dt_2:DataTable, e_columns_1:List[str], e_columns_2:List[str]):
    """RIGHT JOIN"""

    ret = dt_1.join(table=dt_2, how="right",left_on=["fruits", "color"],right_on=["name", "color"])
    rows = ret.rows(type='list')

    assert ret.columns == tuple(e_columns_1 + e_columns_2)
    assert ret.row_count == 7
    assert [1, "apple", "r", 100, "apple", "r", "apple"] in rows
    assert [2, "berry", None, 200, "berry", None, "unknown berry"] in rows
    assert [5, "apple", "r", 100, "apple", "r", "apple"] in rows

    assert [None, None, None, 120, "apple", "y", "yellow apple"] in rows
    assert [None, None, None, 50, "banana", "y", "red apple"] in rows
    assert [None, None, None, 150, "tomato", "r", "tomato(ret)"] in rows
    assert [None, None, None, 120, "berry", "b", "brack berry"] in rows


def test_full_join(dt_1:DataTable, dt_2:DataTable, e_columns_1:List[str], e_columns_2:List[str]):
    """FULL JOIN"""

    ret = dt_1.join(table=dt_2, how="full",left_on=["fruits", "color"],right_on=["name", "color"])
    rows = ret.rows(type='list')

    assert ret.columns == tuple(e_columns_1 + e_columns_2)
    assert ret.row_count == 9
    assert [1, "apple", "r", 100, "apple", "r", "apple"] in rows
    assert [2, "berry", None, 200, "berry", None, "unknown berry"] in rows
    assert [5, "apple", "r", 100, "apple", "r", "apple"] in rows

    assert [3, "banana", "X", None, None, None, None] in rows
    assert [4, "lemon", "y", None, None, None, None] in rows
    assert [5, "apple", "r", 100, "apple", "r", "apple"] in rows

    assert [None, None, None, 120, "apple", "y", "yellow apple"] in rows
    assert [None, None, None, 50, "banana", "y", "red apple"] in rows
    assert [None, None, None, 150, "tomato", "r", "tomato(ret)"] in rows
    assert [None, None, None, 120, "berry", "b", "brack berry"] in rows




