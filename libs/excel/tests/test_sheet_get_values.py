import pytest
from typing import List,Dict,Any,Tuple
import os
from pprint import pprint

from excel import ExcelWorkbook, Direction, Oriented


SCRIPT_DIR = os.path.dirname(__file__)
SAMPLE_EXCEL_PATH = os.path.join(SCRIPT_DIR, "test_data", "sample.xlsx")
SAMPLE_COL_NAMES:List[str] =  ["id", "name", "age", "sex", "favorites", "favorites", "favorites"]
SAMPLE_COL_NAMES_UNIQUE:List[str] =  list(dict.fromkeys(SAMPLE_COL_NAMES))


def test_default():
    """パラメータ指定なしの既定動作"""

    excel = ExcelWorkbook(file=SAMPLE_EXCEL_PATH)
    data = excel.worksheet(sheetname="基本形").get_values()
    assert len(data) == 6
    assert data[0] == SAMPLE_COL_NAMES



@pytest.mark.parametrize(
    ["p_coord", "row_count", "first_row"],
    [
        # 左端からの全行/全列パターン
        pytest.param({}, 6, SAMPLE_COL_NAMES),
        pytest.param({"min_col": 1, "min_row": 1, "max_col": 0, "max_row": 0}, 6, SAMPLE_COL_NAMES),
        pytest.param({"min_col": 1, "min_row": 1, "max_col": None, "max_row": None}, 6, SAMPLE_COL_NAMES),
        pytest.param({"min_col": 1, "min_row": 1}, 6, SAMPLE_COL_NAMES),
        pytest.param({"min_col": "A", "min_row": 1, "max_col": "G", "max_row": 10}, 6, SAMPLE_COL_NAMES),
        pytest.param({"min_col": "A", "min_row": 1, "max_col": "G", "max_row": 100}, 6, SAMPLE_COL_NAMES),

        # 途中から
        pytest.param({"min_col": 4, "min_row": 3, "max_col": 0, "max_row": 0}, 4,
            [ x if x.strip() else None for x in "Male,Heavy Metal,,Hawaii".split(",")]),
        pytest.param({"min_col": "D", "min_row": 3, "max_col": 0, "max_row": 0}, 4,
            [ x if x.strip() else None for x in "Male,Heavy Metal,,Hawaii".split(",")]),

        # 途中から途中まで
        pytest.param({"min_col": 4, "min_row": 3, "max_col": 6, "max_row": 6}, 2,
            [ x if x.strip() else None for x in "Male,Heavy Metal,".split(",")]),
    ],
)
def test_coordinate(p_coord, row_count, first_row):
    """読み込み座標を指定"""

    excel = ExcelWorkbook(file=SAMPLE_EXCEL_PATH)
    data = excel.worksheet(sheetname="基本形").get_values(**p_coord)
    assert len(data) == row_count
    assert data[0] == first_row



def test_include_bkank():
    """ブランク行の読み込みあり"""

    excel = ExcelWorkbook(file=SAMPLE_EXCEL_PATH)
    data = excel.worksheet(sheetname="基本形").get_values(skip_blank=False)
    assert len(data) == 12
    assert data[0] == SAMPLE_COL_NAMES



def test_direction():
    """読み込み方向"""
    excel = ExcelWorkbook(file=SAMPLE_EXCEL_PATH)
    sheet_v = excel.worksheet(sheetname="縦持ち")
    sheet_h = excel.worksheet(sheetname="横持ち")


    # 未指定 = Vertical
    data = sheet_v.get_values(min_row=2)
    assert len(data) == 6
    assert data[0] == SAMPLE_COL_NAMES

    # Vertical
    data_v1 = sheet_v.get_values(min_row=2, read_direction=Direction.Vertical)
    assert len(data_v1) == 6
    assert data_v1[0] == SAMPLE_COL_NAMES

    data_v2 = sheet_v.get_values(min_row=2, read_direction="vertical")
    assert len(data_v2) == 6
    assert data_v2[0] == SAMPLE_COL_NAMES

    # Horizontal
    data_h1 = sheet_h.get_values(min_row=2, read_direction=Direction.Horizontal)
    assert len(data_h1) == 6
    assert data_h1[0] == SAMPLE_COL_NAMES

    data_h2 = sheet_h.get_values(min_row=2, read_direction="horiZonTAL")
    assert len(data_h2) == 6
    assert data_h2[0] == SAMPLE_COL_NAMES

    # 全部同一
    assert data_v1 == data_v2
    assert data_h2 == data_h2
    assert data_v1 == data_h2



def test_oriented():
    """戻り値の行指向/列指向"""
    excel = ExcelWorkbook(file=SAMPLE_EXCEL_PATH)
    sheet_v = excel.worksheet(sheetname="縦持ち")
    ret = sheet_v.get_values(min_row=2)

    # 行指向で返却
    ret_r1 = sheet_v.get_values(min_row=2, return_oriented=Oriented.Row)
    ret_r2 = sheet_v.get_values(min_row=2, return_oriented="row")
    assert ret == ret_r1
    assert ret == ret_r2

    # 列指向で返却
    data_c1 = sheet_v.get_values(min_row=2, return_oriented=Oriented.Column)
    data_c2 = sheet_v.get_values(min_row=2, return_oriented="column")
    assert data_c1 == data_c2
    assert len(data_c1) == len(SAMPLE_COL_NAMES)

    # １列目のみのリスト
    assert data_c1[0] == ["id", 1, 2, 3, 4, 5]

    # 各行の１要素目は列名
    for i in range(0, len(SAMPLE_COL_NAMES)):
        assert data_c1[i][0] == SAMPLE_COL_NAMES[i]



def test_header():
    """ヘッダ読み込み"""
    excel = ExcelWorkbook(file=SAMPLE_EXCEL_PATH)
    sheet_v = excel.worksheet(sheetname="縦持ち")

    # 行指向
    data = sheet_v.get_values(min_row=2, header=True, return_oriented=Oriented.Row)
    assert len(data) == 5
    assert list(data[0].keys()) == SAMPLE_COL_NAMES_UNIQUE
    assert isinstance(data[0]["name"], str)
    assert isinstance(data[0]["favorites"], list)
    assert len(data[0]["favorites"]) == 3

    # 列指向
    data = sheet_v.get_values(min_row=2, header=True, return_oriented=Oriented.Column)
    assert list(data.keys()) == SAMPLE_COL_NAMES_UNIQUE
    assert data["id"] == [1, 2, 3, 4, 5]
    assert data["favorites"][0] == ["red", "cat", "apple"]
    assert data["favorites"][-1] == ["dog", None, "hiphop"]





