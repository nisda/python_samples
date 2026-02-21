from typing import Dict, Any
import logging
from . import job_excel
from . import job_error
from . import job_dynamodb
from io import BytesIO
import re

logger = logging.getLogger(__name__)


def workflow(excel_path:str|BytesIO, config_path:str, variables:Dict[str, Any]={}, converters:Dict[str, callable]={}):
    # データ調整
    config_lib_path:str = re.sub(pattern=r'/|\\', repl=".",string=config_path).lstrip(".")

    #---------------------------------
    # Excel からデータをロード
    #---------------------------------
    logger.info("[job_excel.load_and_convert]")
    ret = job_excel.load_and_convert(
        config_path=config_lib_path,
        excel_file=excel_path,
        converters=converters,
    )
    logger.debug(ret)

    # エラー処理
    if ret.get("error", None) is not None:
        error_info:Dict = ret["error"]
        logger.error(error_info)
        error_info_md:str = job_error.formatting_to_markdown(error_info=error_info)
        return {
            "error_info" : error_info,
            "error_info_md": error_info_md,
        }

    #---------------------------------
    # DynamoDBに登録
    #---------------------------------

    # DynamoDB登録データを生成
    logger.info("[job_dynamodb.make_dynamodb_data]")
    ret = job_dynamodb.make_dynamodb_data(
        config_path=config_lib_path,
        tables=ret["tables"],
        variables=variables,
    )
    logger.debug(ret)

    # 登録
    logger.info("[job_dynamodb.register_to_dynamodb]")
    ret = job_dynamodb.register_to_dynamodb(
        dynamodb_infos=ret["dynamodb_infos"]
    )
    logger.debug(ret)

    return ret


