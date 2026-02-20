from typing import Any, Dict
import unicodedata
import re
import datetime
import logging
import json

from .utils import master_data as MasterData
from .models.ExcelTable.ExcelTable import DataTables

from . import job_common
from . import job_error


logger = logging.getLogger(__name__)



def load_and_convert(config_path:str, excel_file:str):

    #-------------------------------------
    #   データ読み込み
    #-------------------------------------

    # Excelからデータを読み込み
    load_configs:dict = job_common.import_config_attr(config_name=config_path, attr_name="load_configs")
    tables:DataTables = DataTables(
        file=excel_file,
        load_configs=load_configs,
    )
    logger.debug(f"tables@load:\n{json.dumps(tables.serialize(), indent=2, ensure_ascii=False)}")


    #-------------------------------------
    #   データ調整
    #-------------------------------------

    # データクレンジング
    tables.map(func=_data_cleansing)
    logger.debug(f"tables@cleansing:\n{json.dumps(tables.serialize(), indent=2, ensure_ascii=False)}")

    # エラー処理
    error_info = job_error.make_error_info_from_tables(tables=tables)
    if error_info:
        return error_info


    # コンバート処理
    tables.map(func=_data_convert)
    logger.debug(f"tables@convert:\n{json.dumps(tables.serialize(), indent=2, ensure_ascii=False)}")

    # エラー処理
    error_info = job_error.make_error_info_from_tables(tables=tables)
    if error_info:
        return error_info

    #-------------------------------------
    #   正常終了
    #-------------------------------------
    return {
        "tables" : tables
    }




def _data_cleansing(value, type, required, **kwargs) -> Any:
    def __replace_hyphen(text, replace_to="-"):
        """ハイフンを統一"""
        hyphens = '-˗ᅳ᭸‐‑‒–—―⁃⁻−▬─━➖ーㅡ﹘﹣－ｰ𐄐𐆑 '
        hyphens = '|'.join(hyphens)
        return re.sub(hyphens, replace_to, text)

    # type未定義は無変換
    if type is None:
        return value

    # 必須チェック
    if value is None:
        if required:
            raise ValueError("入力必須です。")
        else:
            return None

    # データ補正
    value = str(value).strip()
    type = type.lower()


    # タイプ別
    if type == "str":
        return value

    if type == "int":
        try:
            return int(unicodedata.normalize('NFKC', value))
        except:
            raise ValueError("数値を入力してください。")

    if type == "mail":
        if not re.fullmatch(r'(.+)@(.+)\.(.+)', value.strip()):
            raise ValueError("メールアドレスを入力してください。")
        return value

    if type == "bool":
        return not bool(value.lower() in ("", "0", "false", "no"))

    if type == "time-range":
        # 半角変換
        value = unicodedata.normalize('NFKC', value)
        value = __replace_hyphen(value)

        # データ分割＆要素数チェック
        times = [ x.strip() for x in value.split("-") ]
        if len(times) != 2:
            raise ValueError("時刻の範囲を入力してください")
            
        # データ型チェック
        try:
            times[0] = datetime.datetime.strptime(times[0], "%H:%M").strftime(format="%H:%M")
            times[1] = datetime.datetime.strptime(times[1], "%H:%M").strftime(format="%H:%M")
        except:
            raise ValueError("時刻を入力してください。（00:00-23:59）")

        # データ範囲チェック
        if times[0] > times[1]:
            raise ValueError("時刻の順番が正しくありません。")

        # OK
        return times

    # タイプ未定義
    return value


def _data_convert(value:Any, convert:Dict = {}, **kwargs) -> Any:
    # convert が empty であったら何もしない
    if not bool(convert):
        return value

    # value が empty であったら何もしない
    if not bool(value):
        return value

    # 変換処理
    ret =  MasterData.get_id(convert_type=convert["type"], value=value)

    # 返却
    return ret
