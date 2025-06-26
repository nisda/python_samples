# coding: utf-8
import datetime
from typing import Any

class SimpleCache:

    def __init__(self):
        self.__storehouse:dict = {}

    # キャッシュ処理
    def cache(self, key:str, value:Any, expiration_seconds:int = 60):
        '''
        キャッシュ処理
        [param] value ... 値 or 関数(lambda式)
        '''

        # 期限内であればキャッシュ値を返却
        if key in self.__storehouse:
            now = datetime.datetime.now()
            if self.__storehouse[key]["ttl"] >= now:
                return self.__storehouse[key]["value"]

        # キャッシュ更新
        if callable(value):
            result  = value()
        else:
            result  = value

        now = datetime.datetime.now()
        ttl = now + datetime.timedelta(seconds=expiration_seconds)
        self.__storehouse[key]  =   {
            "updated"   : now,
            "ttl"       : ttl,
            "value"     : result
        }

        # キャッシュされている値を返却
        return result

    # キャッシュ削除
    def remove(self, key:str):
        if key in self.__storehouse.keys():
            del self.__storehouse[key]
        return

    # 現在保存されているキーを取得。
    def keys(self, key:str):
        return self.__storehouse.keys()



