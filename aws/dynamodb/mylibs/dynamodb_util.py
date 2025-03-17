from typing import List, Dict, Any
import boto3.dynamodb
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer, Binary
import boto3
import boto3.session
from collections.abc import Generator, Iterator


# boto3.dynamodb.types.Binary -> bytes
def __convert_binary_to_bytes(item):
    if isinstance(item, list):
        return [ __convert_binary_to_bytes(x) for x in item ]
    if isinstance(item, dict):
        return { k:__convert_binary_to_bytes(v) for k,v in item.items() }
    if isinstance(item, Binary):
        return item.value
    else:
        return item


def type_serialize(item: dict):
    return {k: TypeSerializer().serialize(value=v) for k, v in item.items()}


def type_deserialize(item: dict):
    return __convert_binary_to_bytes({k: TypeDeserializer().deserialize(value=v) for k, v in item.items()})


def make_update_expression(
        set_items:Dict[str, Any]=None,
        add_items:Dict[str, Any]=None,
        remove_items:List[str]=None
    ):

    # INPUTパラメータの調整
    set_items    = set_items or {}
    add_items    = add_items or {}
    remove_items = remove_items or []

    # 更新情報の生成
    update_expressions:List[str] = []

    set_expressions:List    = [ f"#{k} = :{k}" for k in set_items.keys()]
    set_attr_names:dict     = { f"#{k}":k for k in set_items.keys() }
    set_attr_values:dict    = { f":{k}":v for k,v in set_items.items() }
    if len(set_expressions) > 0:
        update_expressions.append("SET " + ', '.join(set_expressions))

    remove_expressions:List = [ f"#{k}" for k in remove_items]
    remove_attr_names:dict   = { f"#{k}":k for k in remove_items }
    if len(remove_expressions) > 0:
        update_expressions.append("REMOVE " + ', '.join(remove_expressions))

    add_expressions:List    = [ f"#{k} = :{k}" for k in add_items.keys()]
    add_attr_names:dict     = { f"#{k}":k for k in add_items.keys() }
    add_attr_values:dict    = { f":{k}":v for k,v in add_items.items() }
    if len(add_expressions) > 0:
        update_expressions.append("ADD " + ', '.join(add_expressions))

    # 返却
    return {
        "UpdateExpression": " ".join(update_expressions),
        "ExpressionAttributeNames": {
            **set_attr_names,
            **remove_attr_names,
            **add_attr_names,
        },
        "ExpressionAttributeValues": {
            **set_attr_values,
            **add_attr_values,
        },
    }


class Table:
    __table = None


    def __init__(self, table_name:str, region_name:str = None, session:boto3.session.Session = None):
        if session is None:
            session = boto3.Session(region_name=region_name)

        dynamodb = session.resource('dynamodb', region_name=region_name)
        self.__table = dynamodb.Table(table_name)


    def scan(self, **kwargs) -> Iterator:
        while True:
            response = self.__table.scan(**kwargs)
            for item in response['Items']:
                yield item
            if 'LastEvaluatedKey' not in response:
                break
            kwargs.update(ExclusiveStartKey=response['LastEvaluatedKey'])


    def query(self, KeyConditionExpression, IndexName:str=None, **kwargs) -> Iterator:

        # required
        kwargs.update(KeyConditionExpression=KeyConditionExpression)

        # optional
        if IndexName is not None: kwargs.update(IndexName=IndexName)

        # exec
        while True:
            response = self.__table.query(**kwargs)
            for item in response['Items']:
                yield item
            if 'LastEvaluatedKey' not in response:
                break
            kwargs.update(ExclusiveStartKey=response['LastEvaluatedKey'])


    def get_item(self, Key, **kwargs):
        self.__table.put_item(
            Key=Key,
            **kwargs
        )

    def put_item(self, Item, **kwargs):
        """データを追加"""
        self.__table.put_item(
            Item=Item,
            # ConditionExpression='attribute_not_exists(xxx)'   # 後で考える
        )


    def update_item(self, 
        Key,
        set_items:Dict[str, Any]=None,
        add_items:Dict[str, Any]=None,
        remove_items:List[str]=None,
        **kwargs
    ):
        update_params:dict = make_update_expression(
            set_items=set_items,
            add_items=add_items,
            remove_items=remove_items
        )

        self.__table.update_item(
            Key=Key,
            **update_params,
            **kwargs,
        )


    def delete_item(self, Key:dict, **kwargs):
        """データ削除"""
        self.__table.delete_item(Key, **kwargs,)


    def delete_items(self, items:List[dict]):
        """データ削除（複数）"""

        # キー項目を抽出
        key_names:str = [ x["AttributeName"] for x in self.__table.key_schema ]

        # キー値のリストを生成
        delete_keys:dict = [ { k:v for k,v in x.items() if k in key_names } for x in items ]

        # データ削除
        with self.__table.batch_writer() as batch:
            for key in delete_keys:
                batch.delete_item(Key = key)
        return 0


    def truncate(self):
        """データ全削除"""

        # キー項目を抽出
        key_names:str = [ x["AttributeName"] for x in self.__table.key_schema ]

        # キー値のリストを生成
        delete_keys:dict = [ { k:v for k,v in x.items() if k in key_names } for x in self.scan() ]

        # データ削除
        with self.__table.batch_writer() as batch:
            for key in delete_keys:
                batch.delete_item(Key = key)
        return 0




