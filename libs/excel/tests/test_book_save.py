
import pytest
import os
import io
from excel import ExcelWorkbook
from pprint import pprint
from datetime import datetime

SCRIPT_DIR = os.path.dirname(__file__)
SAMPLE_EXCEL_PATH = os.path.join(SCRIPT_DIR, "test_data", "sample.xlsx")

OUTPUT_EXCEL_PATH_1 = os.path.join(SCRIPT_DIR, "test_data", f"output_{datetime.now().strftime("%Y%m%d%H%M%S")}_1.xlsx")
OUTPUT_EXCEL_PATH_2 = os.path.join(SCRIPT_DIR, "test_data", f"output_{datetime.now().strftime("%Y%m%d%H%M%S")}_2.xlsx")


def test_blank_save():
    """未作成では保存不可"""
    book1 = ExcelWorkbook()

    # save: book未作成エラー
    with pytest.raises(Exception) as e:
        book1.save()
    assert "Workbook is not loaded." in str(e.value)

    # save: book未作成エラー
    with pytest.raises(Exception) as e:
        book1.save_as(path=OUTPUT_EXCEL_PATH_1)
    assert "Workbook is not loaded." in str(e.value)



def test_new_book_save():
    """新規作成＆保存"""

    # ファイル新規作成
    book1 = ExcelWorkbook()
    book1.new(sheetname="テスト1")

    # save: パス不明なのでエラー
    with pytest.raises(Exception) as e:
        book1.save()
    assert "FilePath is not set." in str(e.value)

    # save_as: 保存可能
    book2 = book1.save_as(path=OUTPUT_EXCEL_PATH_1)
    assert os.path.isfile(OUTPUT_EXCEL_PATH_1)  # ファイル作成OK
    assert book1 == book2                       # 同一インスタンス

    # 後片付け：ファイル削除
    os.remove(OUTPUT_EXCEL_PATH_1)


def test_loaded_binary_save():
    """バイナリ読み込みの保存"""

    with open(SAMPLE_EXCEL_PATH, "rb") as f:
        file_bin:bytes = f.read()
        assert isinstance(file_bin, bytes)
    
    book1 = ExcelWorkbook()
    book1.load(file=file_bin, read_only=False)  # read_only=False でないと別ファイルへのSaveもNGらしい
    
    # save: パス不明なのでエラー
    with pytest.raises(Exception) as e:
        book1.save()
    assert "FilePath is not set." in str(e.value)

    # save_as: 保存可能
    book2 = book1.save_as(path=OUTPUT_EXCEL_PATH_1)
    assert os.path.isfile(OUTPUT_EXCEL_PATH_1)  # ファイル作成OK
    assert book1 == book2

    # 後片付け：ファイル削除
    os.remove(OUTPUT_EXCEL_PATH_1)


def test_loaded_file_save():
    """ファイル読み込みの保存"""

    # 新規作成
    book1 = ExcelWorkbook()
    book1.new(sheetname="テスト1")
    book1.save_as(path=OUTPUT_EXCEL_PATH_1)
    assert os.path.isfile(OUTPUT_EXCEL_PATH_1)

    # 作成した Book を読み込み
    book2 = ExcelWorkbook(file=OUTPUT_EXCEL_PATH_1, read_only=False)
    book2.create_sheet("追加1")
    assert book2.sheetnames == ["テスト1", "追加1"]

    # 保存
    book2.save()

    # 別名保存
    book3 = book2.save_as(path=OUTPUT_EXCEL_PATH_2)
    assert os.path.isfile(OUTPUT_EXCEL_PATH_2)

    # 後片付け：ファイル削除
    os.remove(OUTPUT_EXCEL_PATH_1)
    os.remove(OUTPUT_EXCEL_PATH_2)




def test_load_save_as():
    """読み込んだExcelを別名で保存"""

    # 新規作成
    book1 = ExcelWorkbook()
    book1.new(sheetname="テスト1")
 
    # 新規保存
    book2 = book1.save_as(path=OUTPUT_EXCEL_PATH_1)
    assert book1 == book2

    # 同一パスに保存
    book3 = book1.save_as(path=OUTPUT_EXCEL_PATH_1)
    assert book1 == book2   # 保存可能かつ同一インスタンス


    # 別名保存
    book4 = book1.save_as(path=OUTPUT_EXCEL_PATH_2)
    assert os.path.isfile(OUTPUT_EXCEL_PATH_2)
    assert book1 != book4   # 新しいオブジェクトが作られる。


    # もう一度別名保存 -> 上書き不可
    with pytest.raises(FileExistsError) as e:
        book5 = book1.save_as(path=OUTPUT_EXCEL_PATH_2)
    assert "already exists." in str(e.value)


    # 上書きフラグ=True で別名上書き保存 -> OK
    book6 = book1.save_as(path=OUTPUT_EXCEL_PATH_2, overwrite=True)
    assert book1 != book6   # 新しいオブジェクトが作られる。


    # 後片付け：ファイル削除
    os.remove(OUTPUT_EXCEL_PATH_1)
    os.remove(OUTPUT_EXCEL_PATH_2)

