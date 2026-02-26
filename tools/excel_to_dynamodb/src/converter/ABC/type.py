from typing import Dict, Any

from ._base import ABCConverterBase


_INIT_VALUES = [
    {"id" : "t1", "name" : "タスク"},
    {"id" : "t2", "name" : "バグ"},
    {"id" : "t3", "name" : "課題"},
]


class Type(ABCConverterBase):

    def _get_items(self) -> Dict[str, Any]:
        return {
            x["name"]:x["id"] for x in _INIT_VALUES
        }

    def _put_item(self, value:str) -> Dict[str, Any]:
        return {
            value: "t901"
        }

    def _unregistered_message(self, value:Any) -> str:
        return f"種別 `{value}` は未登録です。"

