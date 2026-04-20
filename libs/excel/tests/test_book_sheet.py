
import pytest
import os
import io
from excel import ExcelWorkbook
from pprint import pprint

SCRIPT_DIR = os.path.dirname(__file__)
SAMPLE_EXCEL_PATH = os.path.join(SCRIPT_DIR, "test_data", "sample.xlsx")



def test_sheet_create():
    """新規作成"""
    book1 = ExcelWorkbook()
    book1.new(sheetname="シートA")
    assert book1.sheetnames == ["シートA"]

    sheet1 = book1.create_sheet(sheetname="追加1")
    assert book1.sheetnames == ["シートA", "追加1"]
    assert sheet1.sheetname == "追加1"

    sheet2 = book1.create_sheet(sheetname="追加2", index=0)
    assert book1.sheetnames == ["追加2", "シートA", "追加1"]
    assert sheet2.sheetname == "追加2"

    sheet3 = book1.create_sheet(sheetname="追加3", index=-1) # 末尾の１つ前
    assert book1.sheetnames == ["追加2", "シートA", "追加3", "追加1"]
    assert sheet3.sheetname == "追加3"


def test_sheet_duplication():
    """シート名重複エラー"""

    book1 = ExcelWorkbook()
    book1.new(sheetname="シートA")
    sheet1 = book1.create_sheet(sheetname="追加1")

    with pytest.raises(Exception) as e:
        sheet1 = book1.create_sheet(sheetname="追加1")
    assert "already exists" in str(e.value)


def test_sheet_remove():
    """シート削除"""

    book1 = ExcelWorkbook()
    book1.new(sheetname="シートA")
    sheet1 = book1.create_sheet(sheetname="追加1")
    sheet2 = book1.create_sheet(sheetname="追加2")
    assert book1.sheetnames == ["シートA", "追加1", "追加2"]

    book1.remove_sheet(sheetname="シートA")
    assert book1.sheetnames == ["追加1", "追加2"]

    book1.remove_sheet(sheetname="追加2")
    assert book1.sheetnames == ["追加1"]

    book1.remove_sheet(sheetname="追加1")
    assert book1.sheetnames == []


def test_sheet_remove_not_found():
    """シート削除：非存在エラー"""

    book1 = ExcelWorkbook()
    book1.new(sheetname="シートA")
    with pytest.raises(KeyError) as e:
        book1.remove_sheet(sheetname="追加1")
    assert "does not exist." in str(e.value)


def test_sheet_copy():

    # ベースのファイルを作成
    book1 = ExcelWorkbook()
    book1.new(sheetname="シートA")
    sheet1 = book1.create_sheet(sheetname="追加1")
    sheet2 = book1.create_sheet(sheetname="追加2")
    assert book1.sheetnames == ["シートA", "追加1", "追加2"]

    # コピー元が非存在
    with pytest.raises(KeyError) as e:
        book1.copy_sheet(src="シートX", dest="コピーA")
    assert "not found." in str(e.value)

    # コピー先が重複
    with pytest.raises(KeyError) as e:
        book1.copy_sheet(src="シートA", dest="追加1")
    assert "already exists." in str(e.value)

    # コピーOK（場所指定なし）
    ws_copy1 = book1.copy_sheet(src="シートA", dest="コピー1")
    assert book1.sheetnames == ["シートA", "追加1", "追加2", "コピー1"]

    # コピーOK（場所指定あり）
    ws_copy2 = book1.copy_sheet(src="シートA", dest="コピー2", index=0)
    assert book1.sheetnames == ["コピー2", "シートA", "追加1", "追加2", "コピー1"]

    ws_copy3 = book1.copy_sheet(src="シートA", dest="コピー3", index=1)
    assert book1.sheetnames == ["コピー2", "コピー3", "シートA", "追加1", "追加2", "コピー1"]

    ws_copy4 = book1.copy_sheet(src="シートA", dest="コピー4", index=6)
    assert book1.sheetnames == ["コピー2", "コピー3", "シートA", "追加1", "追加2", "コピー1", "コピー4"]

    ws_copy5 = book1.copy_sheet(src="シートA", dest="コピー5", index=9999)
    assert book1.sheetnames == ["コピー2", "コピー3", "シートA", "追加1", "追加2", "コピー1", "コピー4", "コピー5"]


def test_sheet_sort():
    """シート並べ替え"""

    book1 = ExcelWorkbook()
    book1.new(sheetname="シートA")
    sheet1 = book1.create_sheet(sheetname="追加1")
    sheet2 = book1.create_sheet(sheetname="追加2")
    sheet3 = book1.create_sheet(sheetname="追加3")
    sheet3 = book1.create_sheet(sheetname="追加4")

    ret = book1.sort_sheet(["追加2", "非存在", "シートA", "追加4"])
    assert book1.sheetnames == ["追加2", "シートA", "追加4", "追加1", "追加3"]
    assert book1.sheetnames == ret

