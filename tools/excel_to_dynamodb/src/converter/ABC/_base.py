from typing import Any, Dict, List
from abc import ABC, abstractmethod

from .libs.local_mem_cache import CacheContainer, Const



class ABCConverterBase(ABC):
    _cache_key:str
    _auto_register:bool
    _add_str:str


    def __init__(self, auto_register:bool=False, add_str:str=""):
        self._cache_key = f"ABCConverter::{self.__class__.__name__}"
        self._auto_register = auto_register
        self._add_str = add_str


    def converter(self, value:str, **kwargs):
        # None は何もしない
        if value is None: return None

        # データを取得（キャッシュ利用）
        cache_key:str = self._cache_key
        items:Dict[str, Any] = CacheContainer.set(key=cache_key, value=lambda:self._get_items())
        matched_data:Any = items.get(value, None)

        # キャッシュあり -> 返却
        if matched_data:
            return str(matched_data) + self._add_str
        
        # キャッシュなし
        if self._auto_register:
            # 登録＆キャッシュ追加
            new_item:Dict[str, Any] = self._put_item(value=value)
            items.update(items)
            CacheContainer.set(key=cache_key, value=items, force=True)
            return str(new_item[value]) + self._add_str
        else:
            # raise ValueError(f"ユーザー `{value}` はプロジェクトに登録されていません。")
            raise ValueError(self._unregistered_message(value=value))


    @abstractmethod
    def _get_items(self) -> Dict[str, Any]:
        pass

    @abstractmethod
    def _put_item(self, value:str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def _unregistered_message(self, value:Any) -> str:
        pass

