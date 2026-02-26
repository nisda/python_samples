from typing import Dict, Any

from ._base import ABCConverterBase


_INIT_VALUES = [
    # {"id" : "u1", "name" : "xxx@xxx.xxx"},
    {"id" : "u2", "name" : "yyy@yyy.yyy"},
    {"id" : "u3", "name" : "zzz@zzz.zzz"},
]


class User(ABCConverterBase):

    def _get_items(self) -> Dict[str, Any]:
        return {
            x["name"]:x["id"] for x in _INIT_VALUES
        }

    def _put_item(self, value:str) -> Dict[str, Any]:
        pass

    def _unregistered_message(self, value:Any) -> str:
        return f"ユーザー `{value}` は未登録です。"

