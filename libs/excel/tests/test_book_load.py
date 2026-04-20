
import pytest
import os
import io
from excel import ExcelWorkbook


SCRIPT_DIR = os.path.dirname(__file__)
SAMPLE_EXCEL_PATH = os.path.join(SCRIPT_DIR, "test_data", "sample.xlsx")



def test_file_not_exists():
    """ファイル非存在"""

    with pytest.raises(FileNotFoundError) as e:
        book1 = ExcelWorkbook()
        book1.load(file="not_exists.xlsx")
    assert "No such file or directory" in str(e.value)


def test_load_file():
    """ファイルパス指定"""

    book1 = ExcelWorkbook()
    book2 = book1.load(file=SAMPLE_EXCEL_PATH)

    # 同一インスタンスである
    assert book1 == book2


def test_load_binary():
    """バイナリ指定"""

    with open(SAMPLE_EXCEL_PATH, "rb") as f:
        file_bin:bytes = f.read()
        assert isinstance(file_bin, bytes)
    
    book1 = ExcelWorkbook()
    book2 = book1.load(file=file_bin)               # bytes 渡し
    book3 = book1.load(file=io.BytesIO(file_bin))   # ByteIO 渡し

    # 同一インスタンスである
    assert book1 == book2
    assert book1 == book3


