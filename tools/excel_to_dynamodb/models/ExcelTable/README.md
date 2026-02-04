# ExcelTable


## ざっくり仕様

* シート名のワイルドカード対応。
  1つの読み込み定義で複数シートを読み込める。
* １つのシートに複数のテーブルを含めることができる。
* 複数範囲を読み込んで１つのデータ（テーブル）にする。
  データ数は一致する前提で。
* 項目名は定義情報で指定する方法とExcelから読み込む方法の2通り。
    * 定義情報に書かれていたらそれを採用。Excelから読み込んだ範囲はすべて"データ"として扱う。
    * 定義情報の項目名が未指定またはNoneの場合は、読み込んだ範囲の１行目を項目名として扱う。
    * 項目名の id と value は必須。それ以外は attr 扱い。
* 読み込み定義（load_configs）イメージ↓

```py
load_configs:dict = [
    {
        "sheetname" : "縦並び複数件*",
        "tables" : {
            "TBL_A": {
                "data_ranges" : [
                    {
                        "name"   : "values",
                        "direction" : "horizonal",
                        "header" : ["Required_2", "Caption_2", "VALUE"],
                        "min_row": 4,
                        "min_col": 4,
                        "max_row": 0,
                        "max_col": 0,
                    },
                    {
                        "name"   : "attr",
                        "direction" : "horizonal",
                        "header" : None,
                        "min_row": 3,
                        "min_col": 2,
                        # "max_row": 0,
                        "max_col": 5,
                    },
                ]
            },
        },
    },
]
```

* 読み込み定義の構成は改善したい。わかりづらすぎる。
  * 複数範囲を読み込んで１つにする。
  * データ数は一致する前提で。（それは今も一緒）
  * 項目名は指定範囲に含めないようにする？ ⇒ 選択できるといいよね。
      * 定義にカラム名を書く。
      * 
      * id と value は必須。それ以外は attr 扱い。
        どちらの場合でも。



## 内部データ構造
* シート単位にデータを管理する。（内部構造）
* データ構成イメージ。load_config と nearly equal にする。

```py

class DataTables(List[DataTable]):

class DataTable():
    sheetname = "<sheetname>"
    tablename = "<tablename>"
    records   = List[DataRecord]

class DataRecord(List[DataField]):

class DataField:
    name:str = None
    value_org: Any = None
    value:Any = None
    attr:Dict = {}

```

```py
tables_list:List[DataTables]] = [
    { # <DataTables>
        "sheetname" : "ＸＸＸ_01",
        "tables" : {
            "<table_name_1>" : [ # <DataTable>
                # <DataRecords> = list(<DataField>)
                {"name": "col_01", "value": "A0001",    "type": "str", ...},
                {"name": "col_02", "value": "xx@xx.xx", "type": "mail", ...},
                {"name": "col_03", "value": 3,          "type": "int", ...},
            ],
        }
    }
]

```


