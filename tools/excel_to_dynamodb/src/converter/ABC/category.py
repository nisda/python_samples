from typing import Dict, Any

from ._base import ABCConverterBase


_INIT_VALUES = [
    # {"id" : "c1", "name" : "カテ１"},
    {"id" : "c2", "name" : "カテ２"},
    {"id" : "c3", "name" : "カテ３"},
]


class Category(ABCConverterBase):

    def _get_items(self) -> Dict[str, Any]:
        return {
            x["name"]:x["id"] for x in _INIT_VALUES
        }

    def _put_item(self, value:str) -> Dict[str, Any]:
        return {
            value: "c901"
        }

    def _unregistered_message(self, value:Any) -> str:
        return f"カテゴリー `{value}` は未登録です。"

