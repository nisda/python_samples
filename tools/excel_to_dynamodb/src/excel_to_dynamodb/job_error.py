from typing import Dict, List
from .models.ExcelTable.ExcelTable import DataTables


def make_error_info_from_tables(tables:DataTables) -> List[Dict]:
    error_records :List[Dict] = []
    for table in tables:
        sheetname:str = table.sheetname
        for i in range(0, len(table.records)):
            record = table.records[i]
            for field in record:
                if field.error:
                    error_records.append({
                        "sheetname" : sheetname,
                        "number" : i,
                        "name" : field.name,
                        "caption" : field.attr["caption"],
                        "value" : field.value_org,
                        "error" : field.error,
                    })

    if len(error_records) == 0:
        return None

    return {
        "error" : {
            "records": error_records
        }
    }





def formatting_to_markdown(error_info:Dict) -> str:
    """エラー情報をMarkDown形式に整形"""
    error_records:List[Dict] = error_info["records"]

    print(error_info)
    columns:Dict[str, str] = {
        "シート名" : "sheetname",
        "＃": "number",
        "項目名" : "caption",
        "入力値" : "value",
        "エラー内容": "error",
    }

    buf: List[List[str]] = []
    buf.append(f"| {" | ".join(columns.keys())} |")
    buf.append(f"| {" | ".join(["--"] * len(columns))} |")
    for err_rec in error_records:
        cell_values:List[str] = [
            str(err_rec[k]) for k in columns.values()
        ]
        buf.append(f"| {" | ".join(cell_values)} |")
    
    return "\n".join(buf)
