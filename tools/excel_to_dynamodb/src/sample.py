
import os
import logging
from io import BytesIO
from excel_to_dynamodb.workflow import workflow

from converter import ABC



logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=None,
    level=logging.DEBUG,
    # format="[%(levelname)s] %(name)s:%(message)s",
    style='{', format='{asctime} [{levelname:.5}] {name} | {message}',   # styleで書式変更できる
    )


INPUT_EXCEL_PATH = "./sample.xlsx"
CONFIG_PATH = "./sample-config"
VARIAVLES = {
    "prefix" : os.getenv("PREFIX", "dev-xxx"),
    "tenant_id" : "000001-001",
}


def lambda_handler(event, context):
    logger.info(f"event = {event}")

    #---------------------------------
    # Conveters
    #---------------------------------
    converters = {
        "ABC.Category": ABC.Category(add_str="@conv", auto_register=True).converter,
        "ABC.User": ABC.User(add_str="@conv", auto_register=False).converter,
        "ABC.Status": ABC.Status(add_str="@conv", auto_register=True).converter,
        "ABC.Priority": ABC.Priority(add_str="@conv", auto_register=False).converter,
        "ABC.Type": ABC.Type(add_str="@conv", auto_register=True).converter,
    }

    #---------------------------------
    # Excelファイル
    #---------------------------------

    # 入力パターンA
    excel_path = INPUT_EXCEL_PATH

    # 入力パターンB
    with open(INPUT_EXCEL_PATH, 'rb') as f:
        bytes_io_obj = BytesIO(f.read())


    #---------------------------------
    # 実行
    #---------------------------------
    ret = workflow(
        # excel_path=excel_path,
        excel_path=bytes_io_obj,
        config_path=CONFIG_PATH,
        variables=VARIAVLES,
        converters=converters,
    )

    # 結果
    logger.info(f"ret = {ret}")
    return ret


if __name__ == '__main__':
    event = {
        "system" : "abc-system",
        "tenant_id" : "000001-001",
    }

    ret = lambda_handler(event=event, context=None)

