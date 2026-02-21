from typing import List, Dict, Any
from .libs.local_mem_cache import CacheContainer, Const



class User():

    __CACHE_KEY:str = "User"
    __INIT_VALUES = [
        # {"id" : "u1", "name" : "xxx@xxx.xxx"},
        {"id" : "u2", "name" : "yyy@yyy.yyy"},
        {"id" : "u3", "name" : "zzz@zzz.zzz"},
    ]
    __add_str: str = ""


    def __init__(self, add_str:str):
        self.__add_str = add_str
 

    def converter(self, value, **kwargs):
        # None は何もしない
        if value is None: return None

        # データを取得（キャッシュ利用）
        cache_key:str = self.__CACHE_KEY
        items:List[Dict[str, Any]] = CacheContainer.set(key=cache_key, value=lambda:self.__get_items())
        items_by_name:Dict[str, Dict[str, Any]] = {x["name"]:x for x in items}
        matched_data:Dict = items_by_name.get(value, None)

        if matched_data:
            # キャッシュあり
            return matched_data["id"] + self.__add_str
        else:
            # キャッシュなし -> エラー
            # raise KeyError(f" convert-type:User name=`{value}` is not found.")
            raise ValueError(f"ユーザー `{value}` はプロジェクトに登録されていません。")


    def __get_items(self) -> List[Dict[str, Any]]:
        print(" -- get_list() --")
        return self.__INIT_VALUES
