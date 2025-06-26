# coding: utf-8

"""
jsonライブラリ拡張
  ver : 1.0.0
  date: 2025/6/14
"""

import functools
from json import *
import json as origin_json
# from json import dumps as origin_dumps

from typing import Dict, Any, List, Tuple, Union

import datetime
import decimal
import uuid

import os
import glob

# dump時のシリアライズで使用するエンコードの定義
# map(type: lambda)
__ENCODE_DEFINITION = {
    # datetime, date
    (datetime.datetime, datetime.date): lambda x: x.isoformat(),
    # time
    datetime.time: lambda x: x.isoformat(),
    # decimal
    decimal.Decimal: lambda x: float(x) if '.' in str(x) else int(x),
    # bytes
    bytes: lambda x: x.decode(),
    # uuid
    uuid.UUID: lambda x: str(x),
}


def default_json_encoder(obj, encoder_definition: dict = __ENCODE_DEFINITION):
    # Encoder定義を利用して変換
    for type, func in encoder_definition.items():
        if isinstance(obj, type):
            return func(obj)
    # 上記以外はサポート対象外.
    raise TypeError("Type %s not serializable" % type(obj))


# Parameter Overwrite
dumps = functools.partial(origin_json.dumps, default=default_json_encoder)
dump = functools.partial(origin_json.dump, default=default_json_encoder)


def batch_dump(dir_path: Union[str, List[str], Tuple[str]], data: Dict[str, Any], dir_exist_ok: bool = True, indent: int = 2):
    '''
    一括ファイル出力
    指定フォルダ内に key ごとに json ファイル出力する。
    フォルダ内の既存ファイルはすべて削除する。
    '''

    # パスを整形
    if isinstance(dir_path, (List, Tuple)):
        dir_path = os.path.join(*dir_path)

    # フォルダ作成
    os.makedirs(name=dir_path, exist_ok=dir_exist_ok)

    # フォルダ内をクリーンアップ
    path_pattern: str = os.path.join(dir_path, "*")
    for file_path in glob.glob(path_pattern):
        os.remove(file_path)

    # キーごとに出力
    for k, v in data.items():
        file_path: str = os.path.join(dir_path, f"{k}.json")
        with open(file_path, 'w') as f:
            dump(v, f, indent=indent)


def batch_load(dir_path: Union[str, List[str], Tuple[str]]) -> Dict[str, Any]:
    '''
    一括ファイル読込
    指定フォルダ内にある *.json をすべて読み込む。
    ファイル名を key とした dict を返却する。
    '''

    # パスを整形
    if isinstance(dir_path, (List, Tuple)):
        dir_path = os.path.join(*dir_path)

    # 読み込み
    ret: Dict[str, Any] = {}
    path_pattern: str = os.path.join(dir_path, "*.json")
    for file_path in glob.glob(path_pattern):
        file_name = os.path.basename(file_path)
        key_name = os.path.splitext(file_name)[0]
        with open(file_path, 'r') as f:
            ret[key_name] = origin_json.load(f)

    # 返却
    return ret
