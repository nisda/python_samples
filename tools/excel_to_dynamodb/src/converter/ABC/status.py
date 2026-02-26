from typing import Dict, Any

from ._base import ABCConverterBase




class Status(ABCConverterBase):
    pass

    def _get_items(self) -> Dict[str, Any]:
        return {
            "未処理": 1 ,
            "処理中": 2,
            "処理済み": 3,
            "完了": 4,
        }

    def _put_item(self, value:str) -> Dict[str, Any]:
        pass

    def _unregistered_message(self, value:Any) -> str:
        return f"状態 `{value}` は未登録です。"

