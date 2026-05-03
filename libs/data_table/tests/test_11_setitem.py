import pytest
from data_table import DataTable
from pprint import pprint

COLUMNS = ("id", "name", "sex", "age")
RECORDS = [
    [1, "Alice", "F"],
    [2, "Bob", None, 22],
    [3, "Charlie", "M", None],
]

def test_getitem_no_column():
    """カラム名なし"""

    # カラム名の指定なし
    dt = DataTable(data=RECORDS)
    assert dt.columns == ("0", "1", "2", "3")
    assert dt.column_count == 4
    assert dt.row_count    == 3

    # 列追加（すべて同一値）
    dt["country"] = "England"
    rows = dt.rows(type="list")
    assert dt.columns == ("0", "1", "2", "3", "country")
    assert dt.column_count == 5
    assert dt.row_count    == 3
    assert rows[0] == [1, "Alice", "F", None, "England"]
    assert rows[1] == [2, "Bob", None, 22, "England"]
    assert rows[2] == [3, "Charlie", "M", None, "England"]

    # 列追加（個別）
    dt[-1] = ["AAA", "BBB", "CCC"]
    rows = dt.rows(type="list")
    assert dt.columns == ("0", "1", "2", "3", "country", "-1")
    assert dt.column_count == 6
    assert dt.row_count    == 3
    assert rows[0] == [1, "Alice", "F", None, "England", "AAA"]
    assert rows[1] == [2, "Bob", None, 22, "England", "BBB"]
    assert rows[2] == [3, "Charlie", "M", None, "England", "CCC"]


    # 列更新（すべて同一値）
    dt["2"] = "Unknown"
    rows = dt.rows(type="list")
    assert dt.columns == ("0", "1", "2", "3", "country", "-1")
    assert dt.column_count == 6
    assert dt.row_count    == 3
    assert rows[0] == [1, "Alice", "Unknown", None, "England", "AAA"]
    assert rows[1] == [2, "Bob", "Unknown", 22, "England", "BBB"]
    assert rows[2] == [3, "Charlie", "Unknown", None, "England", "CCC"]

    # # 列更新（個別）
    dt["country"] = ["USA", None, "ENG"]
    rows = dt.rows(type="list")
    assert dt.columns == ("0", "1", "2", "3", "country", "-1")
    assert dt.column_count == 6
    assert dt.row_count    == 3
    assert rows[0] == [1, "Alice", "Unknown", None, "USA", "AAA"]
    assert rows[1] == [2, "Bob", "Unknown", 22, None, "BBB"]
    assert rows[2] == [3, "Charlie", "Unknown", None, "ENG", "CCC"]


    # データ数不一致
    with pytest.raises(ValueError) as e:
        dt["country"] = ["USA", None]
    assert "Length of values does not match row-count" in str(e.value)

    with pytest.raises(ValueError) as e:
        dt["country"] = ["USA", None, "ENG", "AUS"]
    assert "Length of values does not match row-count" in str(e.value)



def test_getitem_no_column_zero():
    """カラム名なし／0件"""

    # カラム名の指定なし
    dt = DataTable(data=[])
    assert dt.columns == ()
    assert dt.column_count == 0
    assert dt.row_count    == 0

    # カラム定義のみ追加される
    dt["country"] = "England"
    assert dt.columns == ("country", )
    assert dt.column_count == 1
    assert dt.row_count    == 0 # 追加されない

    with pytest.raises(ValueError) as e:
        # 配列の場合は数が一致しているべきであるためエラー
        dt["country"] = ["England"]
    assert "Length of values does not match row-count" in str(e.value)






def test_getitem_column():
    """カラム名あり"""

    # # カラム名あり
    dt = DataTable(data=RECORDS, columns=COLUMNS)
    assert dt.columns == ("id", "name", "sex", "age")
    assert dt.column_count == 4
    assert dt.row_count    == 3

    # 列追加（すべて同一値）
    dt["country"] = "England"
    rows = dt.rows(type="list")
    assert dt.columns == ("id", "name", "sex", "age", "country")
    assert dt.column_count == 5
    assert dt.row_count    == 3
    assert rows[0] == [1, "Alice", "F", None, "England"]
    assert rows[1] == [2, "Bob", None, 22, "England"]
    assert rows[2] == [3, "Charlie", "M", None, "England"]

    # 列追加（個別）
    dt[-1] = ["AAA", "BBB", "CCC"]
    rows = dt.rows(type="list")
    assert dt.columns == ("id", "name", "sex", "age", "country", "-1")
    assert dt.column_count == 6
    assert dt.row_count    == 3
    assert rows[0] == [1, "Alice", "F", None, "England", "AAA"]
    assert rows[1] == [2, "Bob", None, 22, "England", "BBB"]
    assert rows[2] == [3, "Charlie", "M", None, "England", "CCC"]


    # 列更新（すべて同一値）
    dt["sex"] = "Unknown"
    rows = dt.rows(type="list")
    assert dt.columns == ("id", "name", "sex", "age", "country", "-1")
    assert dt.column_count == 6
    assert dt.row_count    == 3
    assert rows[0] == [1, "Alice", "Unknown", None, "England", "AAA"]
    assert rows[1] == [2, "Bob", "Unknown", 22, "England", "BBB"]
    assert rows[2] == [3, "Charlie", "Unknown", None, "England", "CCC"]

    # # 列更新（個別）
    dt["country"] = ["USA", None, "ENG"]
    rows = dt.rows(type="list")
    assert dt.columns == ("id", "name", "sex", "age", "country", "-1")
    assert dt.column_count == 6
    assert dt.row_count    == 3
    assert rows[0] == [1, "Alice", "Unknown", None, "USA", "AAA"]
    assert rows[1] == [2, "Bob", "Unknown", 22, None, "BBB"]
    assert rows[2] == [3, "Charlie", "Unknown", None, "ENG", "CCC"]


    with pytest.raises(ValueError) as e:
        dt["country"] = ["USA", None]
    assert "Length of values does not match row-count" in str(e.value)

    with pytest.raises(ValueError) as e:
        dt["country"] = ["USA", None, "ENG", "AUS"]
    assert "Length of values does not match row-count" in str(e.value)


def test_setitem_column_zero():
    """カラム名あり／0件"""

    # カラム名の指定なし
    dt = DataTable(data=[], columns=COLUMNS)
    assert dt.columns == ("id", "name", "sex", "age")
    assert dt.column_count == 4
    assert dt.row_count    == 0

    # 列追加
    dt["country"] = "England"
    assert dt.columns == ("id", "name", "sex", "age", "country")
    assert dt.column_count == 5
    assert dt.row_count    == 0 # 追加されない

    with pytest.raises(ValueError) as e:
        # 配列の場合は数が一致しているべきであるためエラー
        dt["country"] = ["England"]
    assert "Length of values does not match row-count" in str(e.value)






