from typing import List,Dict

MASTER_DATA = {
    "ABC.Category" : [
        {"id" : "c1", "name" : "カテ１"},
        {"id" : "c2", "name" : "カテ２"},
        {"id" : "c3", "name" : "カテ３"},
    ],
    "ABC.Type" : [
        {"id" : "t1", "name" : "タスク"},
        {"id" : "t2", "name" : "バグ"},
        {"id" : "t3", "name" : "課題"},
    ],
    "ABC.User" : [
        {"id" : "u1", "name" : "xxx@xxx.xxx"},
        {"id" : "u2", "name" : "yyy@yyy.yyy"},
        {"id" : "u3", "name" : "zzz@zzz.zzz"},
    ],
}

def get_id(convert_type:str, value:str):
    compare_key:str = "name"
    master_data:List[Dict] = MASTER_DATA[convert_type]
    matched_recs = [x for x in master_data if x[compare_key] == value]
    # 存在チェック
    if len(matched_recs) == 0:
        raise KeyError(f" convert-ype:{convert_type} {compare_key}=`{value}` is not found")
    else:
        return matched_recs[0]["id"]


