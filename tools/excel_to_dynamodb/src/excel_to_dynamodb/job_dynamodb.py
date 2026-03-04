from typing import Any, List,Dict, Callable
import logging
import json
import re

from .utils import dict_util as dict_util
from .utils.dict_util import ChainableDict
from .utils.format_ex import format_ex
from .models.ExcelTable.ExcelTable import DataTables, DataTable, DataRecord

from . import job_common
from .utils.dynamodb_util import Table


logger = logging.getLogger(__name__)




def make_dynamodb_data(config_path:str, tables:DataTables, variables:Dict):

    #-------------------------------------
    #   設定読み込み
    #-------------------------------------

    # dynamodb 設定を取得
    dynamodb_configs:List[Dict] = job_common.import_config_attr(config_name=config_path, attr_name="dynamodb_configs")


    #-------------------------------------
    #   DynamoDB登録用データを生成
    #-------------------------------------

    # テーブル別にデータをまとめる。
    grouped_tables:Dict[str, List[DataTable]] = _grouping_tables(tables=tables)
    logger.debug(f"tables@grouping: counts={({k:len(v) for k,v in grouped_tables.items()})}")


    # dynamodb設定別にレコードを調整
    for dynamodb_config in dynamodb_configs:
        # dynamodb用レコード群を作成
        records:List[Dict] = _make_records_for_dynamodb(
            dynamodb_config=dynamodb_config,
            grouped_tables=grouped_tables,
            variables=variables,
        )
        dynamodb_config["records"] = records
        dynamodb_config["table_name"] = format_ex(
            format=dynamodb_config["table_name"],
            **{"var": ChainableDict(variables)},
        )
        dynamodb_config["table_region"] = format_ex(
            format=dynamodb_config.get("table_region", None),
            **{"var": ChainableDict(variables)},
        )

    return {
        "dynamodb_infos": dynamodb_configs,
    }


def _grouping_tables(tables:DataTables) -> Dict[str, List[DataTable]]:
    """tables を拡張dictに変換"""

    # tablename 別の records(階層化dict)を生成
    records_by_table:Dict[str, List[Dict[str, Any]]] = {}
    for tablename in tables.tablenames():
        records_by_table[tablename] = tables.filter(tablename=tablename)

    # 返却
    return records_by_table


def _make_records_for_dynamodb(
        dynamodb_config:Dict,
        grouped_tables:Dict[str, List[DataTable]],
        variables:Dict,
    ):

    # 設定情報を取得
    source_name:str                 = dynamodb_config["source"]
    data_function:str|Callable      = dynamodb_config.get("function", None)
    data_template:Dict[str, Any]    = dynamodb_config["template"]

    # ソーステーブルを取得
    source_tables: List[DataTable] = grouped_tables[source_name]
    logger.debug(f"tables@source: counts={len(source_tables)}")

    # 全テーブルのレコードをマージして１つのリストにする。
    source_records: List[DataRecord] = []
    for table in source_tables:
        source_records.extend(table.records)
    logger.debug(f"records@source: counts={len(source_records)}")

    # 加工後レコードの入れ物を用意（型アノテーションのためだけに）
    work_records: List[Dict[str, Any]] = []

    # dict に変換する。
    work_records = [ x.to_dict() for x in source_records ]
    logger.debug(f"records@dict: counts={len(work_records)}")
    logger.debug(f"records@dict: {json.dumps(work_records, indent=2, ensure_ascii=False)}")

    # custom_function で調整する。（指定時のみ）
    if data_function:
        # カスタムファンクション実行
        work_records = data_function(records=work_records, variables=variables)
    logger.debug(f"records@custom: counts={len(work_records)}")
    if len(work_records) > 0:
        logger.debug(f"records@custom: [0] = {json.dumps(work_records[0], indent=2, ensure_ascii=False)}")

    # テーブルを階層化＆ ChainabledDict に変換
    records_for_assign = [
        ChainableDict(dict_util.from_flatten(record))
        for record in work_records
    ]
    logger.debug(f"records@chained: counts={len(work_records)}")
    if len(work_records) > 0:
        logger.debug(f"records@chained: [0] = {json.dumps(work_records[0], indent=2, ensure_ascii=False)}")

    # 変数を ChainabledDict に変換
    variables_for_assign:ChainableDict = ChainableDict(variables)

    # template に割り当て
    work_records = [
        dict_util.map_recursive(
            data = data_template,
            func = lambda x: format_ex(format=x, **{"source": record, "var": variables_for_assign, })
        )
        for record in records_for_assign
    ]
    logger.debug(f"records@templated: counts={len(work_records)}")

    # 返却
    return work_records




def register_to_dynamodb(dynamodb_infos:List[Dict], variables:Dict) -> Dict[str, List[Dict]]:
    logger.debug(f"dynamodb_records: {len(dynamodb_infos)}")

    results = []
    for dynamodb_info in dynamodb_infos:
        table_name:str = dynamodb_info["table_name"]
        table_region:str = dynamodb_info.get("table_region", None)
        pre_delete:Dict = dynamodb_info.get("pre-delete", {})
        records:List[Dict] = dynamodb_info["records"]
        logger.debug(f"table_name: {table_name}")
        logger.debug(f"table_region: {table_region}")
        logger.debug(f"pre_delete: {pre_delete}")
        logger.debug(f"records: count={len(records)}")


        # 更新処理
        pre_delete_index:str = pre_delete.get("index", None)
        pre_delete_keys:Dict = pre_delete.get("keys", None)
        table_handler:Table = Table(table_name=table_name, region_name=table_region)

        # レコード0件時は変数のみの条件で削除実行
        if len(records) == 0:
            pre_delete_keys = {
                k: format_ex(v, var=variables)
                for k,v in pre_delete_keys.items()
            }
            table_handler.delete_items(Items=pre_delete_keys)
            return {}

        # テストのため更新処理スキップ
        continue

        # 更新処理
        ret = table_handler.delete_upsert(
            UpdateItems=records,
            IndexName=pre_delete.get("index",None),
            KeyNames=pre_delete.get("keys", None),
        )
        results.append(table_handler)

    return results


