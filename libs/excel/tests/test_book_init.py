
import pytest
import os
import io
from excel import ExcelWorkbook


SCRIPT_DIR = os.path.dirname(__file__)
SAMPLE_EXCEL_PATH = os.path.join(SCRIPT_DIR, "test_data", "sample.xlsx")


def test_no_specified():
    """指定なし"""

    book1 = ExcelWorkbook()
    assert True # ここまで Exception なしであればOK


def test_init_file():
    """ファイルパス指定"""
    book1 = ExcelWorkbook(file=SAMPLE_EXCEL_PATH)


def test_init_binary():
    """バイナリ指定"""
    with open(SAMPLE_EXCEL_PATH, "rb") as f:
        file_bin:bytes = f.read()
        assert isinstance(file_bin, bytes)
    
    book1 = ExcelWorkbook(file=file_bin)
    book2 = ExcelWorkbook(file=io.BytesIO(file_bin))


def test_file_not_exists():
    """ファイル非存在"""

    with pytest.raises(FileNotFoundError) as e:
        book1 = ExcelWorkbook(file="not_exists.xlsx")
    assert "No such file or directory" in str(e.value)
