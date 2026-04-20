
import pytest
import os
import io
from excel import ExcelWorkbook, ExcelWorksheet, Direction, Oriented
from datetime import datetime


SCRIPT_DIR = os.path.dirname(__file__)
# SAMPLE_EXCEL_PATH = os.path.join(SCRIPT_DIR, "test_data", "sample.xlsx")
OUTPUT_EXCEL_PATH_1 = os.path.join(SCRIPT_DIR, "test_data", f"output_{datetime.now().strftime("%Y%m%d%H%M%S")}_1.xlsx")
OUTPUT_EXCEL_PATH_2 = os.path.join(SCRIPT_DIR, "test_data", f"output_{datetime.now().strftime("%Y%m%d%H%M%S")}_2.xlsx")


@pytest.mark.parametrize(
    ["p_data"],
    [
        pytest.param(
            [
                ["ID", "NAME", "AGE"],
                ["00001", "Alan", 30],
                ["00002", "Bob", 20],
                ["00003", "Charlie", 40],
            ]
        ),
        pytest.param(
            [
                {"ID": "00001", "NAME": "Alan", "AGE": 30},
                {"NAME": "Bob", "AGE": 20, "ID": "00002"},
                {"ID": "00003", "AGE": 40, "NAME": "Charlie"},
            ]
        ),
        pytest.param(
            {
                "ID": ["00001", "00002", "00003"],
                "NAME": ["Alan", "Bob", "Charlie"],
                "AGE": [30, 20, 40],
            }
        ),
    ],
)
def test_data_type(p_data):
    """新規作成"""
    book1 = ExcelWorkbook()
    book1.new(sheetname="追加1")
    sheet1:ExcelWorksheet = book1.worksheet(sheetname="追加1")

    # 書き込み
    sheet1.put_values(data=p_data)

    # 取得して比較
    ret = sheet1.get_values(min_col=0, min_row=0)
    assert ret == [['ID', 'NAME', 'AGE'], ['00001', 'Alan', 30], ['00002', 'Bob', 20], ['00003', 'Charlie', 40]]


# @pytest.mark.parametrize(
#     ["p_data"],
#     [
#         pytest.param(),
#         pytest.param(),
#         pytest.param(),
#     ],
# )
def test_resize():
    """新規作成"""
    book1 = ExcelWorkbook()
    book1.new(sheetname="追加1")
    sheet1:ExcelWorksheet = book1.worksheet(sheetname="追加1")

    # 書き込み
    sheet1.put_values(data=
        [
            ["ID", "NAME", "AGE"],
            ["00001", "Alan", 30],
            ["00002", "Bob", 20],
            ["00003", "Charlie", 40],
        ],
        min_col="B", min_row=3,
        max_col="C", max_row=4
    )

    # # 取得して比較
    # ret = sheet1.get_values(min_col=0, min_row=0)
    # assert ret == [['ID', 'NAME', 'AGE'], ['00001', 'Alan', 30], ['00002', 'Bob', 20], ['00003', 'Charlie', 40]]


def test_direction():
    """新規作成"""
    book1 = ExcelWorkbook()
    book1.new()

    data = [
        ["ID", "NAME", "AGE"],
        ["00001", "Alan", 30],
        ["00002", "Bob", 20],
        ["00003", "Charlie", 40],
    ]

    # 書き込み（縦方向）
    sheet1:ExcelWorksheet = book1.create_sheet(sheetname="V")
    sheet1.put_values(data=data, direction="vertical")
    ret = sheet1.get_values()
    assert ret == [
        ["ID", "NAME", "AGE"],
        ["00001", "Alan", 30],
        ["00002", "Bob", 20],
        ["00003", "Charlie", 40],
    ]

    # 書き込み（横方向）
    sheet2:ExcelWorksheet = book1.create_sheet(sheetname="H")
    sheet2.put_values(data=data, direction="horizontal")
    ret = sheet2.get_values()
    assert ret == [
        ["ID", "00001", "00002", "00003"],
        ["NAME", "Alan", "Bob", "Charlie"],
        ["AGE", 30, 20, 40],
    ]
