from typing import List, Dict, Any
from .libs.local_mem_cache import CacheContainer, Const



class Type():

    __CACHE_KEY:str = "Type"
    __INIT_VALUES = [
        {"id" : "t1", "name" : "タスク"},
        {"id" : "t2", "name" : "バグ"},
        {"id" : "t3", "name" : "課題"},
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
            # キャッシュなし -> 取得＆キャッシュ追加
            new_item:Dict = self.__put_item(name=value)
            items.append(new_item)
            CacheContainer.set(key=cache_key, value=items, force=True)
            return new_item["id"] + self.__add_str


    def __get_items(self) -> List[Dict[str, Any]]:
        print(" -- get_list() --")
        return self.__INIT_VALUES

    def __put_item(self, name:str) -> Dict[str, Any]:
        print(" -- put_item() --")
        return {"id": f"NEWID-{name}", "name": name}


