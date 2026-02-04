from typing import Dict, Any
import os
import logging
import job_excel
import job_error
import job_dynamodb


logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=None,
    level=logging.DEBUG,
    # format="[%(levelname)s] %(name)s:%(message)s",
    style='{', format='{asctime} [{levelname:.5}] {name} | {message}',   # styleで書式変更できる
    )


INPUT_EXCEL_PATH = "./__input/sample.xlsx"

ENV_INFO = {
    "PREFIX" : os.getenv("PREFIX", "dev-xxx")
}



def lambda_handler(event, context):
    logger.info(f"event = {event}")
    ret = workflow(event=event)
    logger.info(f"ret = {ret}")
    return ret


def workflow(event):
    # 共通設定
    system_name:str = event["system"]
    variables:Dict[str, Any] = {
        "prefix" : ENV_INFO["PREFIX"],
    }


    #---------------------------------
    # Excel からデータをロード
    #---------------------------------
    logger.info("[job_excel.load_and_convert]")
    ret = job_excel.load_and_convert(
        system_name=system_name,
        excel_file=INPUT_EXCEL_PATH,
    )
    logger.debug(ret)

    # エラー処理
    if ret.get("error", None) is not None:
        error_info:Dict = ret["error"]
        logger.error(error_info)
        error_info_md:str = job_error.formatting_to_markdown(error_info=error_info)
        return {
            **event,
            **{ "error_info_md": error_info_md }
        }

    #---------------------------------
    # DynamoDBに登録
    #---------------------------------

    # DynamoDB登録データを生成
    logger.info("[job_dynamodb.make_dynamodb_data]")
    ret = job_dynamodb.make_dynamodb_data(
        system_name=system_name,
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

    return {
        **event,
        **{}    # ここに必要な情報を追加
    }



if __name__ == '__main__':
    event = {
        "system" : "abc-system",
        "tenant_id" : "000001-001",
    }

    ret = lambda_handler(event=event, context=None)
