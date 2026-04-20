
import pytest
import os
import io
from excel import ExcelWorkbook
from pprint import pprint

SCRIPT_DIR = os.path.dirname(__file__)
SAMPLE_EXCEL_PATH = os.path.join(SCRIPT_DIR, "test_data", "sample.xlsx")


def test_new():
    """新規作成"""
    book1 = ExcelWorkbook()
    book2 = book1.new()

    # 同一オブジェクト
    assert book1 == book2

    # 初期シート名
    assert book2.sheetnames == ["Sheet"]


def test_new_sheetname():
    """新規作成"""
    book1 = ExcelWorkbook()
    book2 = book1.new(sheetname="テスト１")

    # 初期シート名
    assert book2.sheetnames == ["テスト１"]



def test_already_loaded_file():
    """読み込み済みの場合はエラー（ファイル指定）"""

    book1 = ExcelWorkbook()
    book1.load(file=SAMPLE_EXCEL_PATH)

    with pytest.raises(Exception) as e:
        book2 = book1.new()
    assert "The workbook has already been loaded." in str(e.value)


def test_already_loaded_binary():
    """読み込み済みの場合はエラー（バイナリ指定）"""

    with open(SAMPLE_EXCEL_PATH, "rb") as f:
        file_bin:bytes = f.read()
        assert isinstance(file_bin, bytes)
    
    excel = ExcelWorkbook()
    excel.load(file=file_bin)               # bytes 渡し

    with pytest.raises(Exception) as e:
        excel.new()
    assert "The workbook has already been loaded." in str(e.value)

