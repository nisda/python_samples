from typing import Dict, Any

from ._base import ABCConverterBase



class Priority(ABCConverterBase):
    pass

    def _get_items(self) -> Dict[str, Any]:
        return {
            "高": 2,
            "中": 3,
            "低": 4,
        }

    def _put_item(self, value:str) -> Dict[str, Any]:
        pass

    def _unregistered_message(self, value:Any) -> str:
        return f"優先度 `{value}` は未登録です。"

