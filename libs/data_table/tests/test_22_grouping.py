import pytest
from data_table import DataTable
from pprint import pprint



def test_grouping_no_aggregation():
    """グルーピング指定あり／集計なし"""

    columns = ["name", "color", "date", "price", "quantity"]
    data = [
        ["apple", "red", "2026/02/04", 100, 2000],
        ["apple", "green", "2026/02/01", None, 400],
        ["banana", "yellow", "2025/01/05", 80, 1200],
        ["apple", "red", None, 140, 1000],
        ["apple", "red", "2026/01/14", 90, 500],
    ]

    # １項目でグルーピング
    dt = DataTable(data=data, columns=columns)
    dt1 = dt.grouping(group_by=["name"], aggregation={})
    rows = dt1.rows(type='list')
    assert dt1.columns == ("name",)
    assert dt1.row_count == 2
    assert rows[0] == ["apple" ]
    assert rows[1] == ["banana"]

    # ２項目でグルーピング
    dt = DataTable(data=data, columns=columns)
    dt2 = dt.grouping(group_by=["name", "color"], aggregation={})
    rows = dt2.rows(type='list')
    assert dt2.columns == ("name", "color")
    assert dt2.row_count == 3
    assert rows[0] == ["apple" , "green"]
    assert rows[1] == ["apple" , "red"]
    assert rows[2] == ["banana", "yellow"]



def test_grouping_and_aggregation():
    """グルーピング指定あり／集計あり"""

    columns = ["name", "color", "date", "price", "quantity"]
    data = [
        ["banana", "yellow", None, 80, 1200],
        ["apple", "red", "2026/02/04", 100, 2000],
        ["apple", "green", "2026/01/05", None, 400],
        ["apple", "red", None, 140, 1000],
        ["apple", "red", "2026/01/20", 90, 500],
    ]


    # １項目でグルーピング
    dt = DataTable(data=data, columns=columns)
    dt1 = dt.grouping(group_by=["name"], aggregation={
        "cnt": "count(*)",
        "date_cnt": "count(date)",
        "date_min": "min(date)",
        "date_max": "max(date)",
        "price_min": "min(price)",
        "price_max": "max(price)",
        "price_avg": "avg(price)",
        "quantity_sum": "sum(quantity)",
    })
    rows = dt1.rows(type='list')
    assert dt1.columns == ("name", "cnt", 
        "date_cnt",
        "date_min",
        "date_max",
        "price_min",
        "price_max",
        "price_avg",
        "quantity_sum"
    )
    assert dt1.row_count == 2
    assert rows[0] == ["apple" , 4, 3, "2026/01/05", "2026/02/04", 90, 140, 110, 3900]
    assert rows[1] == ["banana", 1, 0, None, None, 80, 80, 80, 1200]


    # ２項目でグルーピング
    dt = DataTable(data=data, columns=columns)
    dt2 = dt.grouping(group_by=["name", "color"], aggregation={
        "cnt": "count(*)",
        "date_cnt": "count(date)",
        "date_min": "min(date)",
        "date_max": "max(date)",
        "price_min": "min(price)",
        "price_max": "max(price)",
        "price_avg": "avg(price)",
        "quantity_sum": "sum(quantity)",
    })
    rows = dt2.rows(type='list')
    assert dt2.columns == ("name", "color", "cnt", 
        "date_cnt",
        "date_min",
        "date_max",
        "price_min",
        "price_max",
        "price_avg",
        "quantity_sum"
    )
    assert dt2.row_count == 3
    assert rows[0] == ["apple", "green"     , 1, 1, "2026/01/05", "2026/01/05", None, None, None, 400]
    assert rows[1] == ["apple", "red"       , 3, 2, "2026/01/20", "2026/02/04", 90, 140, 110, 3500]
    assert rows[2] == ["banana", "yellow"   , 1, 0, None, None, 80, 80, 80, 1200]







def test_no_grouping_and_aggregation():
    """グルーピング指定なし／集計あり"""

    columns = ["name", "color", "date", "price", "quantity"]
    data = [
        ["banana", "yellow", None, 80, 1200],
        ["apple", "red", "2026/02/04", 100, 2000],
        ["apple", "green", "2026/01/05", None, 400],
        ["apple", "red", None, 140, 1000],
        ["apple", "red", "2026/01/20", 90, 500],
    ]

    # 0項目でグルーピング
    dt = DataTable(data=data, columns=columns)
    dt0 = dt.grouping(group_by=[], aggregation={
        "cnt": "count(*)",
        "date_cnt": "count(date)",
        "date_min": "min(date)",
        "date_max": "max(date)",
        "price_min": "min(price)",
        "price_max": "max(price)",
        "price_avg": "avg(price)",
        "quantity_sum": "sum(quantity)",
    })
    rows = dt0.rows(type='list')
    assert dt0.row_count == 1
    assert rows[0] == [5, 3, "2026/01/05", "2026/02/04", 80, 140, 102.5, 5100]

def test_none():
    """両方指定なし = 空"""

    columns = ["name", "color", "date", "price", "quantity"]
    data = [
        ["banana", "yellow", None, 80, 1200],
        ["apple", "red", "2026/02/04", 100, 2000],
        ["apple", "green", "2026/01/05", None, 400],
        ["apple", "red", None, 140, 1000],
        ["apple", "red", "2026/01/20", 90, 500],
    ]

    dt = DataTable(data=data, columns=columns)
    dt0 = dt.grouping()
    rows = dt0.rows()
    assert dt0.columns == ()
    assert dt0.column_count == 0
    assert dt0.row_count == 0
    assert rows == []
