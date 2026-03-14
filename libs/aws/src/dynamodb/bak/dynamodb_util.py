from typing import List, Dict, Any, Union, Optional, Tuple, Self, overload
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer, Binary
import boto3
import boto3.session
from collections.abc import Iterator
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from boto3.dynamodb.conditions import AttributeBase, Key, Attr, Or, And, Not
from botocore.exceptions import ClientError
from enum import Enum


# boto3.dynamodb.types.Binary -> bytes
def __convert_binary_to_bytes(item:Union[Binary, List, Dict, Any]):
    if isinstance(item, list):
        return [ __convert_binary_to_bytes(x) for x in item ]
    if isinstance(item, dict):
        return { k:__convert_binary_to_bytes(v) for k,v in item.items() }
    if isinstance(item, Binary):
        return item.value
    else:
        return item


def type_serialize(item: Dict):
    return {k: TypeSerializer().serialize(value=v) for k, v in item.items()}


def type_deserialize(item: Dict):
    return __convert_binary_to_bytes({k: TypeDeserializer().deserialize(value=v) for k, v in item.items()})


def make_update_expression(
        set_attrs:Dict[str, Any]=None,
        add_attrs:Dict[str, Any]=None,
        remove_attrs:List[str]=None
    ):

    # INPUTパラメータの調整
    set_attrs    = set_attrs or {}
    add_attrs    = add_attrs or {}
    remove_attrs = remove_attrs or []

    # 更新情報の生成
    update_expressions:List[str] = []

    set_expressions:List    = [ f"#{k} = :{k}" for k in set_attrs.keys()]
    set_attr_names:dict     = { f"#{k}":k for k in set_attrs.keys() }
    set_attr_values:dict    = { f":{k}":v for k,v in set_attrs.items() }
    if len(set_expressions) > 0:
        update_expressions.append("SET " + ', '.join(set_expressions))

    remove_expressions:List = [ f"#{k}" for k in remove_attrs]
    remove_attr_names:dict   = { f"#{k}":k for k in remove_attrs }
    if len(remove_expressions) > 0:
        update_expressions.append("REMOVE " + ', '.join(remove_expressions))

    add_expressions:List    = [ f"#{k} = :{k}" for k in add_attrs.keys()]
    add_attr_names:dict     = { f"#{k}":k for k in add_attrs.keys() }
    add_attr_values:dict    = { f":{k}":v for k,v in add_attrs.items() }
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




class IndexTypes(Enum):
    Primary = "PrimaryIndex"
    LSI = "LocalSecondaryIndex"
    GSI = "GlobalSecondaryIndex"

class Index:

    @property
    def table(self) -> object:
        return self._table

    @property
    def name(self) -> str|None:
        return self._name

    @property
    def type(self) -> IndexTypes:
        return self._type

    @property
    def hash_keys(self) -> List[str]:
        return self._hash_keys

    @property
    def range_keys(self) -> List[str]:
        return self._range_keys

    @property
    def all_keys(self) -> List[str]:
        return self._hash_keys + self._range_keys

    def __init__(self:Self, table:object, name:str|None, type:IndexTypes, hash_keys:List[str], range_keys:List[str]):
        self._table:object          = table
        self._name:str|None         = name
        self._type:IndexTypes       = type
        self._hash_keys:List[str]    = hash_keys
        self._range_keys:List[str]   = range_keys

    def containing_keys(self, search_keys:List[str], range_compare_key:str=None) -> None|Dict[str, List[str]]:
        """含有キー取得（キー項目一致判定）"""

        # HASH キーは全て含まれている必要あり
        if not all(k in search_keys for k in self.hash_keys):
            return None

        if range_compare_key:
            # range_key が指定されている場合は
            # range_key とそれより前方のキーをすべて含む必要あり。

            # range_key を含んでいないときは不一致
            if not range_compare_key in self.range_keys:
                return None

            # INDEXの RANGE-KEY を、指定 range_key の前方と後方に分割
            range_key_idx:int = self.range_keys.index(range_compare_key)
            keys_left:List[str] = self._range_keys[:range_key_idx]

            if all(k in search_keys for k in keys_left):
                # 前方のキーをすべて含んでいればOK
                return {
                    "HASH" : self.hash_keys,
                    "RANGE" : [*keys_left, range_compare_key],
                }
            else:
                # 含んでいなければNG       
                return None

        else:
            # range_key が指定されていない場合は
            # RANGE-KEY を前から順に走査し、検索キーに含まれている分だけ取得

            keys_left:List[str] = []
            for k in self.range_keys:
                if k in search_keys:
                    keys_left.append(k)
                else:
                    # 非含有キーに達したら終了
                    break
            return {
                "HASH"  : self.hash_keys,
                "RANGE" : keys_left,
            }

    @overload
    def query(self, items:Dict[str, Any], primary_attr_only:bool=False, **kwargs:Dict[str, Any]) -> Iterator[Dict[str, Any]]:
        ...

    @overload
    def query(self, items:List[Dict[str, Any]], primary_attr_only:bool=False, **kwargs:Dict[str, Any]) -> Iterator[Dict[str, Any]]:
        ...

    def query(self, items:Union[Dict[str, Any], List[Dict[str, Any]]], primary_attr_only:bool=False,  **kwargs:Dict[str, Any]) -> Iterator[List[Dict[str, Any]]]:
        #-----------------------------------------
        #   パラメータチェック＆調整
        #-----------------------------------------
        if not items:
            raise ValueError("Argument `items` is empty")

        # 条件をリストに変換
        if isinstance(items, dict):
            items = [items]

        # ユニーク化
        items = self.__uniqueness_dict(dicts=items)

        #-----------------------------------------
        #   query条件生成
        #-----------------------------------------

        # 全条件に共通するキーを取得
        common_keys:List[str] = self.__extract_dict_common_keys(dicts=items)


        # 共通キーをもとに検索キー項目を取得
        search_keys = self.containing_keys(search_keys=common_keys, range_compare_key=None)
        if not search_keys:
            raise ValueError(f"No match on INDEX. {common_keys}")


        # 検索キー項目を平坦化（一次元リスト化）
        search_keys_flat: List[str] = [ y for x in search_keys.values() for y in x ]


        # 指定された検索条件を Key/Filter に振り分け
        query_items:List[Dict[str, Dict[str, Any]]]= [
            {
                "key_items" :  { k:v for k,v in item.items() if k in search_keys_flat },
                "filter_items" :  { k:v for k,v in item.items() if k not in search_keys_flat },
            }
            for item in items
        ]

        # key_items でグループ化＆ソート
        temp_items: Dict[Tuple, List] = {}
        for x in query_items:
            hash = self.__make_hashable(x["key_items"])
            if hash in temp_items.keys():
                temp_items[hash]["filter_items"].append(x["filter_items"])
            else:
                temp_items[hash] = {
                    "key_items" : x["key_items"],
                    "filter_items" : [ x["filter_items"] ],
                }
        grouped_items: List[Dict[str, List]] = [
            temp_items[k] for k in sorted(temp_items.keys())
        ]

        #-----------------------------------------
        #   query実行
        #-----------------------------------------
        for tmp_item in grouped_items:
            ret_items = self.__query_one(key_item=tmp_item["key_items"], filter_items=tmp_item["filter_items"], primary_attr_only=primary_attr_only, **kwargs)
            yield from ret_items

        return




    def __query_one(self, key_item:Dict[str, Any], filter_items:List[Dict[str, Any]], primary_attr_only:bool, **kwargs:Dict[str, Any]) -> Iterator[List[Dict[str, Any]]]:
        """
        query実行(1条件)
        """

        #---------------------
        # filter 調整
        #---------------------

        # 空の条件が含まれている場合は None にして条件を排除する。
        # 他のfilter条件にも必ず合致することになり、それらが無意味になるため。
        if {} in filter_items:
            filter_items = []

        #---------------------
        # Conditionオブジェクトに変換
        #---------------------

        # Conditionオブジェクトに変換
        key_condition       = self.__make_condition_eq(keys=key_item, type=Key, operator=And)

        ## 最後に自力でfilterをかけるため不使用（コメントアウト）
        # filter_conditsion   = self.__join_conditions(
        #     operator=Or,
        #     conditions=[
        #         self.__make_condition_eq(keys=x, type=Attr, operator=And)
        #         for x in filter_items
        #     ]
        # )

        #-----------------------------------------
        #   検索実行
        #-----------------------------------------
        # パラメータ調整
        primary_attr_names = [ x["AttributeName"] for x in self.table.key_schema ]
        params: Dict = {
            k:v
            for k,v in {
                "IndexName" : self.name,
                "KeyConditionExpression" : key_condition,
                "ProjectionExpression" : ",".join(primary_attr_names) if primary_attr_only else None
                # "FilterExpression" : filter_conditsion,
            }.items()
            if v
        }

        # 実行（iterator）
        while True:
            response = self._table.query(**kwargs, **params)
            for item in response['Items']:
                if filter_items:
                    for filter_item in filter_items:
                        if filter_item.items() <= item.items():
                            yield item
                            break
                else:
                    yield item

            if 'LastEvaluatedKey' not in response:
                break
            kwargs.update(ExclusiveStartKey=response['LastEvaluatedKey'])

        return


    def __make_condition_eq(self, keys:Dict[str, Any], type:Key|Attr, operator:And|Or=And) -> AttributeBase:
        """
        Key/Filterの条件リソースインタフェースを生成  
        """

        ret = None
        for k,v in keys.items():
            if ret is None:
                ret = type(k).eq(v)
            else:
                # ret = ret & type(k).eq(v)
                ret = operator(ret, type(k).eq(v))
        return ret


    def __join_conditions(self, conditions: List[AttributeBase|None], operator:And|Or) -> AttributeBase|None:
        """
        conditionを指定の結合子で連結
        """

        # 連結処理
        ret:None|AttributeBase = None
        for condition in [ x for x in conditions if x is not None]:
            # conditionを指定演算子で連結
            ret = condition if ret is None else operator(ret, condition)

        # 返却
        return ret


    def __make_hashable(self, obj) -> Tuple[Any]:
        """
        dict/list をhash化
        """

        if isinstance(obj, dict):
            return tuple(sorted((k, self.__make_hashable(v)) for k, v in obj.items()))
        elif isinstance(obj, list):
            return tuple(self.__make_hashable(i) for i in obj)
        else:
            return obj


    def __extract_dict_common_keys(self, dicts:List[Dict]) -> List:
        """
        List[Dict] から共通する dict キーを抽出
        """

        if len(dicts) == 0:
            return []
        results: List = list(dicts[0].keys())
        for d in dicts:
            results = [ k for k in d.keys() if k in results ]
        return results

    def __uniqueness_dict(self, dicts:List[Dict]) -> List[Dict]:
        """
        List[Dict] をユニーク化
        """

        ret:List[Dict] = []
        for d in dicts:
            if d not in ret:
                ret.append(d)
        return ret



class BatchUpdater():

    __stack_items:Dict[str, Dict[Tuple, Dict[str, Any]]] = {}
    """ __stack_items データ構造
        __stack_items = {
            "table_name" : {
                "(pk, sk)" : {
                    "operation" : "Put|Delete",
                    "key"  : { key },
                    "item" : { item },
                }
            }
        }
    """


    def __init__(self,
            region_name:str = None,
            session:boto3.session.Session = None,
        ):
        self.__stack_items = {}

        # session 取得
        session = session if session else boto3.Session(region_name=region_name)

        # client/resource 取得
        self.__client = session.client('dynamodb', region_name=region_name)
        self.__resource = session.resource('dynamodb', region_name=region_name)


    def put_items(self, table_name:str, items:List[Dict[str, Any]]) -> Dict[str, Dict[Tuple, Dict[str, Any]]]:
        if table_name not in self.__stack_items:
            self.__stack_items[table_name] = {}

        for item in items:
            key:Dict = self.__get_primary_keys(table_name=table_name, item=item)
            key_hash:Tuple = self.__make_hashable(key)
            self.__stack_items[table_name][key_hash] = {
                "operation" : "Put",
                "key"  : key,
                "item" : item,
            }

        return self.get_stack()


    def delete_items(self, table_name:str, items:List[Dict[str, Any]]) -> Dict[str, Dict[Tuple, Dict[str, Any]]]:
        if table_name not in self.__stack_items:
            self.__stack_items[table_name] = {}

        for item in items:
            key:Dict = self.__get_primary_keys(table_name=table_name, item=item)
            key_hash:Tuple = self.__make_hashable(key)
            self.__stack_items[table_name][key_hash] = {
                "operation" : "Delete",
                "key"  : key,
                "item" : None,
            }

        return self.get_stack()

    def get_stack(self) -> Dict[str, Dict[Tuple, Dict[str, Any]]]:
        """スタックデータを取得"""
        return self.__stack_items


    def commit(self, transaction:bool=True) -> Dict[str, Dict[Tuple, Dict[str, Any]]]:
        # 実行前スタックデータを退避
        stack_items = self.get_stack()

        # 実行
        if transaction:
            self.__commit_transaction()
        else:
            self.__commit_batch_writer()

        # スタックデータ初期化
        self.__stack_items = {}

        return stack_items


    def __commit_batch_writer(self) -> None:
 
        for table_name, commands in self.__stack_items.items():

            # データ振り分け
            delete_keys: List[Dict] = []
            put_items: List[Dict] = []
            for idx in sorted(commands.keys()):
                command:Dict = commands[idx]
                operation:str = command["operation"].lower()

                if operation == "delete":
                    delete_keys.append(command["key"])
                elif operation == "put":
                    put_items.append(command["item"])

            # 実行
            table = self.__resource.Table(table_name)
            with table.batch_writer() as batch:
                for item in put_items:
                    batch.put_item(Item=item)
                for key in delete_keys:
                    batch.delete_item(Key=key)

            # # データ削除実行
            # with table.batch_writer() as batch:
            #     for key in delete_keys:
            #         batch.delete_item(Key=key)

        # 終了
        return None



    def __commit_transaction(self) -> None:

        # コマンドパラメータ生成
        transact_items: List[Dict] = []
        for table_name, commands in self.__stack_items.items():
            for idx in sorted(commands.keys()):
                command:Dict = commands[idx]
                operation:str = command["operation"].lower()

                if operation == "delete":
                    transact_items.append({
                        "Delete" : {
                            "TableName" : table_name,
                            "Key" : type_serialize(item=command["key"]),
                        }
                    })
                elif operation == "put":
                    transact_items.append({
                        "Put" : {
                            "TableName" : table_name,
                            "Item" : type_serialize(item=command["item"]),
                        }
                    })

        # コマンド実行
        response = self.__client.transact_write_items(TransactItems=transact_items)

        return





    def __get_primary_keys(self, table_name:str, item:Dict[str, Any]) -> Dict[str, Any]:
        """テーブルの PrimaryKey（PK+SK)のリストを取得"""

        table = self.__resource.Table(table_name)
        primary_keys:List[str] = [
            schema["AttributeName"]
            for schema in table.key_schema
        ]
        item_keys:Dict[str, Any] = { k: item[k] for k in primary_keys }
        return item_keys 


    def __make_hashable(self, obj) -> Tuple[Any]:
        """ lidt|dict のハッシュ化"""

        if isinstance(obj, dict):
            return tuple(sorted((k, self.__make_hashable(v)) for k, v in obj.items()))
        elif isinstance(obj, list):
            return tuple(self.__make_hashable(i) for i in obj)
        else:
            return obj



class Table:
    _table = None
    _batch_updater:BatchUpdater = None
    _pk:Index = None
    _gsi:Dict[str, Index] = None
    _lsi:Dict[str, Index] = None
    _ttl_name:Optional[str] = None
    _ttl_default:int = 0
    _updated_at_attr:Optional[str] = None
    _time_zone:str = None

    @property
    def table_name(self) -> str:
        return self._table.table_name


    @property
    def pk(self) -> Index:
        return self._pk

    @property
    def gsi(self) -> Dict[str, Index]:
        return self._gsi

    @property
    def lsi(self) -> Dict[str, Index]:
        return self._lsi

    @property
    def ttl_name(self) -> Optional[str]:
        return self._ttl_name

    @property
    def ttl_default(self) -> int|datetime:
        return self._ttl_default

    @property
    def updated_at_attr(self) -> Optional[str]:
        return self._updated_at_attr

    @property
    def time_zone(self) -> Optional[str]:
        return self._time_zone


    def __init__(
            self,
            table_name:str,
            region_name:str = None,
            session:boto3.session.Session = None,
            ttl_default:int|datetime = 0,
            updated_at_attr:Optional[str] = "_updated_at",
            time_zone:str = "Asia/Tokyo"
        ):
        """コンストラクタ"""

        def __divide_key_schemas(schemas) -> Dict[str, List[str]]:
            """スキーマ定義を HASH と RANGE に分離"""
            hash_keys:List[str] = []
            range_keys:List[str] = []
            for schema in schemas:
                key_type:str = schema["KeyType"]
                attr_name:str = schema["AttributeName"]
                if key_type.upper() == "HASH":
                    hash_keys.append(attr_name)
                elif key_type.upper() == "RANGE":
                    range_keys.append(attr_name)
            return {
                "HASH": hash_keys,
                "RANGE": range_keys
            }

        # session 取得
        session = session if session else boto3.Session(region_name=region_name)

        # client/resource 取得
        dynamodb_cli = session.client('dynamodb', region_name=region_name)
        dynamodb_rsc = session.resource('dynamodb', region_name=region_name)

        # Tableリソース取得
        self._table = dynamodb_rsc.Table(table_name)

        # BatchUpdater
        self._batch_updater = BatchUpdater(region_name=region_name, session=session)


        # PrimaryKey
        pk_schemas = __divide_key_schemas(schemas=self._table.key_schema)
        self._pk = Index(
            table = self._table,
            name = None,
            type = IndexTypes.Primary,
            hash_keys  = pk_schemas["HASH"],
            range_keys = pk_schemas["RANGE"],
        )

        # GlobalSecondaryIndex
        self._gsi = {}
        for idx_info in sorted(self._table.global_secondary_indexes, key=lambda x: x["IndexName"]):
            idx_name:str = idx_info["IndexName"]
            idx_schemas:Dict = __divide_key_schemas(schemas=idx_info["KeySchema"])
            self._gsi[idx_name] = Index(
                table=self._table,
                name=idx_name,
                type=IndexTypes.GSI,
                hash_keys  = idx_schemas["HASH"],
                range_keys = idx_schemas["RANGE"],
            )

        # LocalSecondaryIndex
        self._lsi = {}
        for idx_info in sorted(self._table.local_secondary_indexes, key=lambda x: x["IndexName"]):
            idx_name:str = idx_info["IndexName"]
            idx_schemas:Dict = __divide_key_schemas(schemas=idx_info["KeySchema"])
            self._lsi[idx_name] = Index(
                table=self._table,
                name=idx_name,
                type=IndexTypes.LSI,
                hash_keys  = idx_schemas["HASH"],
                range_keys = idx_schemas["RANGE"],
            )

        # ttl
        response = dynamodb_cli.describe_time_to_live(TableName=table_name)
        self._ttl_name = response.get("TimeToLiveDescription", {}).get("AttributeName", None)
        self._ttl_default = ttl_default

        # 更新日時name
        self._updated_at_attr = updated_at_attr.strip() or None
        self._time_zone       = time_zone or "Asia/Tokyo"


    def get_best_index(self, search_keys:List[str], range_compare_key:str=None) -> Index|None:
        """指定キー項目に適合するINDEXを取得"""

        def __calc_sort_priority(index_pair:Tuple[Index, Dict[str, List[str]]]) -> Tuple:
            """ソート優先度の算出関数"""
            idx:Index                    = index_pair[0]
            key_def:Dict[str, List[str]] = index_pair[1]
            return (
                len(key_def["HASH"]) * -1,
                len(key_def["RANGE"]) * -1,
                { IndexTypes.Primary: 1, IndexTypes.LSI: 2, IndexTypes.GSI: 3}[idx.type],
                str(idx.name),
            )

        # Check argument 
        if not search_keys:
            raise ValueError("arg:search_keys is empty.")

        # #----------------------------------
        # # Primary に合致するならそれが最優先
        # #----------------------------------
        # if self.pk.containing_keys(search_keys=search_keys, range_compare_key=range_compare_key):
        #     return self.pk

        #-------------------------------
        # LSI & GSIはマッチする RANGE-KEY の数が多いものを返却
        #-------------------------------

        # マッチするキー情報を取得
        matched_indexes:List[Tuple[Index, Dict[str, List[str]]]] = []
        for idx in [self.pk, *self.lsi.values(), *self.gsi.values()]:
            key_info = idx.containing_keys(search_keys=search_keys, range_compare_key=range_compare_key)
            if key_info:
                matched_indexes.append((idx, key_info))

        # マッチなしは None を返却
        if len(matched_indexes) == 0:
            return None

        # RANGE-KEYの数で逆順ソートして返却
        # sorted_indexes:List[Index] = sorted(matched_indexes, key=lambda tpl: len(tpl[1]["RANGE"]) * -1 )
        sorted_indexes:List[Index] = sorted(matched_indexes, key=__calc_sort_priority )
        return sorted_indexes[0][0]


    def scan(self, **kwargs) -> Iterator[Dict[str, Any]]:
        while True:
            response = self._table.scan(**kwargs)
            for item in response['Items']:
                yield item
            if 'LastEvaluatedKey' not in response:
                break
            kwargs.update(ExclusiveStartKey=response['LastEvaluatedKey'])


    def query(self, KeyConditionExpression, IndexName:str=None, **kwargs) -> Iterator[List[Dict[str, Any]]]:

        # required
        kwargs.update(KeyConditionExpression=KeyConditionExpression)

        # optional
        if IndexName is not None: kwargs.update(IndexName=IndexName)

        # exec
        while True:
            response = self._table.query(**kwargs)
            for item in response['Items']:
                yield item
            if 'LastEvaluatedKey' not in response:
                break
            kwargs.update(ExclusiveStartKey=response['LastEvaluatedKey'])


    def query2(self, key_items:Dict[str, Any], primary_attr_only:bool=False, **kwargs) -> Iterator[List[Dict[str, Any]]]:
        if isinstance(key_items, list) and len(key_items)== 0:
            # 条件が空の場合は空リストを返却
            yield []

        elif isinstance(key_items, dict):
            # dictの場合はリスト形式に変換して再帰実行
            yield from self.query2(key_items=[key_items], primary_attr_only=primary_attr_only, **kwargs)

        elif isinstance(key_items, list):
            # 共通するキーを抽出してindexを判別
            common_keys:List[str] = self.__extract_dict_common_keys(dicts=key_items)
            idx:Index = self.get_best_index(search_keys=common_keys, range_compare_key=None)
            if idx is None:
                raise ValueError(f"No index that matches the key_items. {common_keys}")
            # query実行
            yield from idx.query(items=key_items, primary_attr_only=primary_attr_only, **kwargs)


    def get_item(self, key:Dict[str,Any], **kwargs):
        # キーのみ抽出
        key_names:str = self.pk.hash_keys + self.pk.range_keys
        get_keys:Dict[str, Any] = { k:v for k,v in key.items() if k in key_names }

        response = self._table.get_item(
            Key=get_keys,
            **kwargs
        )
        ret = response["Item"]
        return ret


    def put_item(self, item, ttl:int|datetime|None=None, overwrite:bool=True, **kwargs:Dict[str, Any]):
        """データ追加/更新"""
        # 追加属性セット
        temp_item:Dict[str, Any] = self._set_additional_attr(item=item, ttl=ttl)

        # キーを抽出
        key_names:str = self.pk.hash_keys + self.pk.range_keys
        upsert_keys:Dict[str, Any] = { k:v for k,v in item.items() if k in key_names }

        # 上書き不可：データ非存在を条件に追加
        if not overwrite:
            # 既存条件
            condition_org = kwargs.pop("ConditionExpression", None)

            # データ非存在条件を生成
            # condition_exists= Not(self.__make_key_condition(keys=upsert_key, type=Key, operator=And))
            condition_exists = Not(self.__join_conditions(And, [Key(k).eq(v) for k,v in upsert_keys.items()]))

            # TTL条件を生成
            condition_ttl = None if self.ttl_name is None else (
                Key(self.ttl_name).lt(int(datetime.now().timestamp()))
            )

            # 連結して条件変数にセット
            kwargs["ConditionExpression"] = \
                self.__join_conditions(operator=And, conditions=[
                    condition_org,
                    self.__join_conditions(operator=Or, conditions=[condition_exists, condition_ttl]),
                ])

        # PUT実行
        try:
            response = self._table.put_item(
                Item=temp_item,
                **kwargs,
            )
            ret:Dict[str, Any] = temp_item
            return ret
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return None
            else:
                raise


    def put_items(self, items:List[Dict[str,Any]], ttl:int|datetime|None=None) -> List[Dict]:
        """データ追加/更新（一括）"""

        items_temp:List[Dict[str, Any]] = [
            self._set_additional_attr(item=item, ttl=ttl)
            for item in items
        ]

        # データ追加
        with self._table.batch_writer() as batch:
            for item in items_temp:
                batch.put_item(Item=item)
        return items_temp


    def delete_item(self, key:Dict[str, Any], **kwargs:Dict[str, Any]) -> Dict:
        """データ削除"""

        # キーのみ抽出
        key_names:str = self.pk.hash_keys + self.pk.range_keys
        delete_key:Dict[str, Any] = { k:v for k,v in key.items() if k in key_names }

        # データ存在を条件に追加（返却値の分岐のため）
        condition_org = kwargs.pop("ConditionExpression", None)
        condition = self.__make_key_condition(keys=delete_key, type=Key, operator=And)
        if condition_org:
            condition = And(condition, condition_org)

        # 削除実行
        try:
            ret = self._table.delete_item(Key=delete_key, ConditionExpression=condition, **kwargs)
            return delete_key
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return None
            else:
                raise


    def delete_items(self, keys:List[Dict[str, Any]]) -> bool:
        """データ削除（一括）"""

        # キー項目を抽出
        key_names:str = self.pk.hash_keys + self.pk.range_keys

        # キー値のリストを生成
        delete_keys:List[Dict[str, Any]] = [ { k:v for k,v in x.items() if k in key_names } for x in keys ]

        # データ削除
        with self._table.batch_writer() as batch:
            for key in delete_keys:
                batch.delete_item(Key = key)
        return True


    def update_item(self, 
        key:Dict[str, Any],
        set_attrs:Dict[str, Any]=None,
        add_attrs:Dict[str, Any]=None,
        remove_attrs:List[str]=None,
        ttl:int|datetime|None=None,
        **kwargs
    ):
        """データ更新"""

        # キー抽出
        key_names:str = self.pk.hash_keys + self.pk.range_keys
        update_key:Dict[str, Any] = { k:v for k,v in key.items() if k in key_names }

        # 追加属性をセット
        set_attrs_temp:Dict[str, Any] = self._set_additional_attr(item=set_attrs, ttl=ttl)

        # 更新パラメータ生成
        update_params:Dict = make_update_expression(
            set_attrs=set_attrs_temp,
            add_attrs=add_attrs,
            remove_attrs=remove_attrs,
        )

        response:Dict = self._table.update_item(
            Key=update_key,
            **update_params,
            **kwargs,
        )
        return response["Attributes"]

    @overload
    def delete_upsert(
            self,
            items:List[Dict[str, Any]],
            delete_key_names:List[str] = None,
            ttl:int|datetime|None=None,
        ) -> Dict:
        pass

    @overload
    def delete_upsert(
            self,
            items:List[Dict[str, Any]],
            delete_keys:Dict[str, Any] = None,
            ttl:int|datetime|None=None,
        ) -> Dict:
        pass

    @overload
    def delete_upsert(
            self,
            items:List[Dict[str, Any]],
            delete_keys:List[Dict[str, Any]] = None,
            ttl:int|datetime|None=None,
        ) -> Dict:
        pass

    ########################################
    ### いらないのでは！？ ###
    ### ただ、一括で
    ########################################
    def delete_upsert(
            self,
            items:List[Dict[str, Any]],
            delete_key_names:List[str] = None,
            delete_keys:List[Dict[str, Any]] = None,
            ttl:int|datetime|None=None,
        ) -> Dict:
        """
        データの洗い替え(DELETE/UPSERT)
        ---
        データを洗い替える。
        更新データの比較キー項目と一致する既存データを削除/更新対象とする。

        :param keys: items 更新データのリスト
        :type type: Dict[str, Any]
        :param keys: delete_key_names 削除キー名のリスト。更新データ(items)と同一の指定キーを持つデータを事前削除する。
        :type type: List[str]
        :param keys: delete_keys 削除キーのリスト。指定のキーで事前削除する。
        :type type: List[Dict[str, Any]]
        """

        #-----------------------------------------
        #   パラメータチェック
        #-----------------------------------------

        # 削除キー情報の両方指定アリはNG
        if all([delete_key_names, delete_keys]):
            raise ValueError("Only one of `delete_key_names` or `delete_keys` must be specified.")

        # 削除キー情報の両方emptyはNG
        if not (delete_key_names or delete_keys):
            raise ValueError("Only one of `delete_key_names` or `delete_keys` must be specified.")

        # 調整
        if delete_keys and isinstance(delete_keys, dict):
            delete_keys = [delete_keys]



        #-----------------------------------------
        #   入力データが０件の場合は対象の全削除＆処理終了
        #-----------------------------------------
        if len(items) == 0:
            if delete_keys:
                # delete_key が設定されていれば対象を削除して終了
                delete_items:List[Dict] = list(self.query2(key_items=delete_keys, primary_attr_only=True))
                self._batch_updater.delete_items(table_name=self.table_name, items=delete_items)
                ret:Dict = self._batch_updater.get_stack()
                self._batch_updater.commit(transaction=True)
                return ret
            else:
                # delete_key が設定されていない場合は何もできない。そのまま終了。
                return {}




        #-----------------------------------------
        #   更新前チェック
        #-----------------------------------------
        # 更新データにプライマリーキー項目が未設定のものがあればエラーとする。
        # 登録処理の途中でエラーとしないために、事前に落とす。
        for update_item in items:
            for key_name in self.pk.all_keys:
                if key_name not in update_item.keys():
                    raise ValueError(f"PrimaryKey `{key_name}` is not set in {update_item}.")


        #-----------------------------------------
        # 削除キー情報を調整
        #-----------------------------------------

        if not delete_key_names:
            # delete_key_names が未指定のときは delete_keys から キー名のリストを作成
            delete_key_names = list(delete_keys[0].keys())
            delete_keys      = None

        # items から削除キー情報を抽出。
        delete_keys = [
            { k: item[k] for k in delete_key_names }
            for item in items
        ]

        # 重複を排除
        temp_delete_key_names = []
        for x in delete_keys:
            if x not in temp_delete_key_names:
                temp_delete_key_names.append(x)
        delete_keys = temp_delete_key_names



        #-----------------------------------------
        #   登録済みアイテムを検索
        #-----------------------------------------

        # INDEX を取得
        best_index:Index = self.get_best_index(search_keys=delete_key_names)
        if not best_index:
            raise ValueError(f"No matching index found ({delete_key_names})")


        # 検索条件のリストを生成
        search_items:List[Dict] = [
            { k:v for k,v in item.items() if k in delete_key_names }
            for item in items
        ]

        # 検索
        before_items:List[Dict] = list(best_index.query(items=search_items, primary_attr_only=True))



        #-----------------------------------------
        #   削除/更新判定
        #-----------------------------------------

        # 削除対象データを抽出。
        # 登録済みデータと更新アイテムをプライマリーキーで比較。
        delete_items: List[Dict] = []
        for before_item in before_items:
            # 更新データとの比較
            for update_item in items:
                if before_item.items() <= update_item.items():
                    # キーが合致 = 更新対象である
                    break
            else:
                # キーが合致するものがなかった = 削除対象である
                delete_items.append(before_item)


        #-----------------------------------------
        #   データ更新/削除
        #-----------------------------------------

        # 返却データを生成
        update_items = items
        result: Dict[str,List[Dict]] = {
            "before" : before_items,
            "delete" : [ { k:v for k,v in x.items() if k in self.pk.all_keys } for x in delete_items ] ,
            "upsert" : [ { k:v for k,v in x.items() if k in self.pk.all_keys } for x in update_items ] ,
        }


        # アイテムを登録
        self.put_items(items=update_items, ttl=ttl)

        # アイテムを削除
        self.delete_items(keys=delete_items)


        # 正常終了
        return result


    def truncate(self):
        """データ全削除"""

        # キー項目を抽出
        key_names:str = self.pk.hash_keys + self.pk.range_keys

        # キー値のリストを生成
        delete_keys:dict = [ { k:v for k,v in x.items() if k in key_names } for x in self.scan() ]

        # データ削除
        with self._table.batch_writer() as batch:
            for key in delete_keys:
                batch.delete_item(Key = key)
        return 0


    def _set_additional_attr(self, item:Dict, ttl:int|datetime|None) -> Dict:
        """オプション属性追加"""

        def __add_updated_at(item:Dict, now_dt:datetime) -> Dict:

            # 名所未設定の場合はそのまま返却
            if not (self.updated_at_attr):
                return item

            # item に設定済みの場合はそのまま返却
            if self.updated_at_attr in item.keys():
                return item

            # 追加して返却
            item[self.updated_at_attr] = now_dt.isoformat()
            return item


        def __add_ttl(item:Dict, ttl:int|datetime|None, now_dt:datetime) -> Dict:

            # 名称未設定はそのまま返却
            if not self.ttl_name:
                return item

            # item に設定済みの場合はそのまま返却
            if self.ttl_name in item.keys():
                return item

            # 個別指定なし（None）の場合はデフォルト値を採用
            ttl_tmp:int|datetime = self.ttl_default
            if ttl is not None:
                ttl_tmp:int|datetime = ttl

            # None の場合はセットせず返却
            if ttl_tmp is None:
                return item

            # TTL が 0 以下の場合はセットせず返却
            if isinstance(ttl_tmp, int) and ttl_tmp <= 0:
                return item

            # 追加して返却
            ttl_dt:datetime = ttl_tmp
            if isinstance(ttl_tmp, int):
                ttl_dt = now_dt + timedelta(seconds=ttl_tmp)        
            item[self.ttl_name] = int(ttl_dt.timestamp())
            return item

        # 追加属性をセットして返却
        now_dt:datetime = datetime.now(ZoneInfo(self.time_zone))
        ret = __add_updated_at(item=item, now_dt=now_dt)
        ret = __add_ttl(item=item, ttl=ttl, now_dt=now_dt)
        return ret


    def __join_conditions(self, operator:And|Or, conditions: List[AttributeBase|None]) -> AttributeBase|None:
        # 連結処理
        ret:None|AttributeBase = None
        for condition in [ x for x in conditions if x is not None]:
            # conditionを指定演算子で連結
            ret = condition if ret is None else operator(ret, condition)

        # 返却
        return ret


    def __make_key_condition(
            self,
            keys:Dict[str, Any],
            type:Key|Attr,
            operator:And|Or=And,
        ) -> AttributeBase:
        """
        Docstring for __make_key_condition  
        Key/Filterの条件リソースインタフェースを生成  
        """

        ret = None
        for k,v in keys.items():
            if ret is None:
                ret = type(k).eq(v)
            else:
                # ret = ret & type(k).eq(v)
                ret = operator(ret, type(k).eq(v))
        return ret


    def __make_hashable(self, obj) -> Tuple[Any]:
        if isinstance(obj, dict):
            return tuple(sorted((k, self.__make_hashable(v)) for k, v in obj.items()))
        elif isinstance(obj, list):
            return tuple(self.__make_hashable(i) for i in obj)
        else:
            return obj


    def __extract_dict_common_keys(self, dicts:List[Dict]) -> List:
        """dict of list から共通する dict キーを抽出"""
        if len(dicts) == 0:
            return []
        results: List = list(dicts[0].keys())
        for d in dicts:
            results = [ k for k in d.keys() if k in results ]
        return results

