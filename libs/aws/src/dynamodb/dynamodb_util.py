from typing import List, Dict, Any, Union, Optional, Tuple
import boto3.dynamodb
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer, Binary
import boto3
import boto3.session
from collections.abc import Generator, Iterator
from datetime import datetime, timedelta
from boto3.dynamodb.conditions import AttributeBase, Key, Attr, Or, And, Not
from botocore.exceptions import ClientError

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


class Table:
    _table = None
    _pk_schema:Dict[str, str] = None
    _gsi_schemas:Dict[str, Dict[str, str]] = None
    _lsi_schemas:Dict[str, Dict[str, str]] = None
    _ttl_name:Optional[str] = None
    _ttl_default:int = 0
    _updated_at:Optional[str] = None

    @property
    def pk_schema(self) -> Dict[str, str]:
        return self._pk_schema

    @property
    def gsi_schemas(self) -> Dict[str, Dict[str, str]]:
        return self._gsi_schemas

    @property
    def lsi_schemas(self) -> Dict[str, Dict[str, str]]:
        return self._lsi_schemas

    @property
    def ttl_name(self) -> Optional[str]:
        return self._ttl_name

    @property
    def ttl_default(self) -> int|datetime:
        return self._ttl_default

    @property
    def updated_at(self) -> Optional[str]:
        return self._updated_at



    def __init__(
            self,table_name:str,
            region_name:str = None,
            session:boto3.session.Session = None,
            ttl_default:int|datetime = 0,
            updated_at:Optional[str] = "_updated_at",
        ):
        """コンストラクタ"""

        # session 取得
        if session is None:
            session = boto3.Session(region_name=region_name)

        # client/resource 取得
        dynamodb_cli = session.client('dynamodb', region_name=region_name)
        dynamodb_rsc = session.resource('dynamodb', region_name=region_name)
        self._table = dynamodb_rsc.Table(table_name)


        # PrimaryKey
        self._pk_schema = { x["KeyType"]:x["AttributeName"] for x in self._table.key_schema }

        # GlobalSecondaryIndex
        self._gsi_schemas = {}
        for idx_info in self._table.global_secondary_indexes or []:
            idx_name:str = idx_info["IndexName"]
            self._gsi_schemas[idx_name] = {
                x["KeyType"]:x["AttributeName"]
                for x in idx_info["KeySchema"]
            }

        # LocalSecondaryIndex
        self._lsi_schemas = {}
        for idx_info in self._table.local_secondary_indexes or []:
            idx_name:str = idx_info["IndexName"]
            self._lsi_schemas[idx_name] = {
                x["KeyType"]:x["AttributeName"]
                for x in idx_info["KeySchema"]
            }


        # ttl
        response = dynamodb_cli.describe_time_to_live(
            TableName=table_name
        )
        self._ttl_name = response.get("TimeToLiveDescription", {}).get("AttributeName", None)
        self._ttl_default = ttl_default

        # 更新日時name
        self._updated_at = updated_at



    def scan(self, **kwargs) -> Iterator:
        while True:
            response = self._table.scan(**kwargs)
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
            response = self._table.query(**kwargs)
            for item in response['Items']:
                yield item
            if 'LastEvaluatedKey' not in response:
                break
            kwargs.update(ExclusiveStartKey=response['LastEvaluatedKey'])


    def query2(self, key:Dict[str, Any], index_name:str=None, **kwargs) -> Iterator:

        #-----------------------------------------
        #   INDEX の情報を取得
        #-----------------------------------------
        search_index_defs: Dict[str,str]
        if index_name is None:
            # IndexName指定がない場合はプライマリを使用。
            search_index_defs = self.pk_schema
        else:
            # INDEX情報を取得。INDEX非存在時はエラー
            search_index_defs: Dict[str, Any] = \
                self.gsi_schemas.get(index_name, None) or \
                self.lsi_schemas.get(index_name, None)
            if search_index_defs is None:
                raise NameError(f"Index `{index_name}` does not exist.")

        #-----------------------------------------
        #   比較キーの生成
        #-----------------------------------------
        # KeyNames の振り分け
        key_names:List[str] = key.keys()
        index_key_names:List[str] = []   # KeyCondition用
        filter_key_names:List[str] = []  # Filter用

        # Hashキーが含まれていなかったらエラー
        if search_index_defs["HASH"] not in key_names:
            raise ValueError(f"HASH-KEY `{index_keys['HASH']}` is required for 'key'.")
        index_key_names  = [ x for x in key_names if x in search_index_defs.values() ]
        filter_key_names = [ x for x in key_names if x not in search_index_defs.values() ]


        #-----------------------------------------
        #   検索条件を生成
        #-----------------------------------------

        # 検索キーを index と filter に振り分け
        search_keys: Dict =  {
            "index_keys"  : { k: key.get(k, None) for k in index_key_names},
            "filter_keys" : { k: key.get(k, None) for k in filter_key_names},
        }

        # Conditionオブジェクトに変換
        index_keys :AttributeBase = self.__make_key_condition(keys=search_keys["index_keys"], type=Key)
        filter_keys:AttributeBase = self.__make_key_condition(keys=search_keys["filter_keys"], type=Attr)

        #-----------------------------------------
        #   検索実行
        #-----------------------------------------

        # パラメータ調整
        params: Dict = {
            k:v
            for k,v in {
                "IndexName" : index_name,
                "KeyConditionExpression" : index_keys,
                "FilterExpression" : filter_keys,
            }.items()
            if v
        }

        # 実行（iterator）
        while True:
            response = self._table.query(**kwargs, **params)
            for item in response['Items']:
                yield item
            if 'LastEvaluatedKey' not in response:
                break
            kwargs.update(ExclusiveStartKey=response['LastEvaluatedKey'])



    def get_item(self, key:Dict[str,Any], **kwargs):
        # キーのみ抽出
        key_names:str = self._pk_schema.values()
        get_key:Dict[str, Any] = { k:v for k,v in key.items() if k in key_names }

        response = self._table.get_item(
            Key=get_key,
            **kwargs
        )
        ret = response["Item"]
        return ret


    def put_item(self, item, ttl:int|datetime|None=None, overwrite:bool=True, **kwargs:Dict[str, Any]):
        """データ追加/更新"""
        # 追加属性セット
        temp_item:Dict[str, Any] = self._set_additional_attr(item=item, ttl=ttl)

        # キーを抽出
        key_names:str = self._pk_schema.values()
        upsert_key:Dict[str, Any] = { k:v for k,v in item.items() if k in key_names }

        # データ非存在を条件に追加（返却値の分岐のため）
        if not overwrite:
            # データ非存在条件を生成
            condition_new = Not(self.__make_key_condition(keys=upsert_key, type=Key, operator=And))
            # 既存条件に追加
            condition_org = kwargs.pop("ConditionExpression", None)
            if condition_org:
                condition_new = And(condition_new, condition_org)
            kwargs["ConditionExpression"] = condition_new


        # 削除実行
        try:
            # PUT実行
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
        key_names:str = self._pk_schema.values()
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
        key_names:str = self._pk_schema.values

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
        key_names:str = self._pk_schema.values
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


    def delete_upsert(
            self,
            items:List[Dict[str, Any]],
            index_name:str=None,
            key_names:List[str]=None,
            ttl:int|datetime|None=None,
        ) -> Dict:
        """
        データの洗い替え(DELETE/INSERT/UPDATE)
        ---
        データを洗い替える。
        更新データの比較キー項目と一致する既存データを削除/更新対象とする。

        :param keys: items 更新データのリスト
        :type type: Dict[str, Any]
        :param type: index_name 検索に使用するINDEX。None時はプライマリーINDEXを使用。
        :type type: str
        :param keys: key_names 比較キー項目名。INDEXキー以外の項目も指定可。PKは必須。None時は指定INDEXの全項目を適用。
        :type type: List[Dict]
        """

        #-----------------------------------------
        #   事前処理
        #-----------------------------------------
        # 処理要否チェック: UpdateItems が空の場合は何もしない
        if not items:
            return {}


        #-----------------------------------------
        #   INDEX の情報を取得
        #-----------------------------------------

        # 検索INDEX
        search_index_defs: Dict[str,str]
        if index_name is None:
            # IndexName指定がない場合はプライマリを使用。
            search_index_defs = self.pk_schema
        else:
            # INDEX情報を取得。INDEX非存在時はエラー
            search_index_defs: Dict[str, Any] = \
                self.gsi_schemas.get(index_name, None) or \
                self.lsi_schemas.get(index_name, None)
            if search_index_defs is None:
                raise NameError(f"Index `{index_name}` does not exist.")

        #-----------------------------------------
        #   更新前チェック
        #-----------------------------------------

        # 更新データのプライマリーキー項目に未設定のものがあればエラーとする。
        # 登録処理の途中でエラーとしないために、事前に落とす。
        for update_item in items:
            for key_type, key_name in self.pk_schema.items():
                if update_item.get(key_name, None) is None:
                    raise ValueError(f"{key_type}-KEY `{key_name}` is not set in items.")


        #-----------------------------------------
        #   比較キーの生成
        #-----------------------------------------
        # KeyNames の振り分け
        index_key_names:List[str] = []   # KeyCondition用
        filter_key_names:List[str] = []  # Filter用
        if key_names is None:
            # 指定なしの場合はINDEX項目すべてを採用する。
            index_key_names = [ v for v in search_index_defs.values() ]
            filter_key_names = []
        else:
            # Hashキーが含まれていなかったらエラー
            if search_index_defs["HASH"] not in key_names:
                raise ValueError(f"HASH-KEY `{index_keys['HASH']}` is required for KeyNames.")
            index_key_names  = [ x for x in key_names if x in search_index_defs.values() ]
            filter_key_names = [ x for x in key_names if x not in search_index_defs.values() ]

        #-----------------------------------------
        #   検索条件リストを生成
        #-----------------------------------------

        # 全アイテムの検索キー部分のみを抽出してリスト化
        search_keys: List[Dict] = [
            {
                "index_keys"  : { k: item.get(k, None) for k in index_key_names},
                "filter_keys" : { k: item.get(k, None) for k in filter_key_names},
            }
            for item in items
        ]
        # index_key に Null(未設定) が含まれているデータは除外。
        # index での検索対象ではない（論理的にNG）＆ 実行エラーになるため（物理的にNG）
        search_keys = [
            x for x in search_keys
            if None not in x["index_keys"].values()
        ]

        # ユニーク化。重複処理を回避のため。
        search_keys_unique:List[Dict] = []
        for d in search_keys:
            if d not in search_keys_unique:
                search_keys_unique.append(d)

        # index_keys でグループ化
        grouped_keys: Dict[Tuple, List] = {}
        for x in search_keys_unique:
            hash = self.__make_hashable(x["index_keys"])
            if hash in grouped_keys.keys():
                grouped_keys[hash]["filter_keys"].append(x["filter_keys"])
            else:
                grouped_keys[hash] = {
                    "index_keys" : x["index_keys"],
                    "filter_keys" : [x["filter_keys"]]
                }

        # Conditionオブジェクトに変換
        key_conditions: Dict[Tuple, List] = {}
        for hash, grouped_key_info in grouped_keys.items():
            key_conditions[hash] = {
                "index_keys" : self.__make_key_condition(grouped_key_info["index_keys"], type=Key),
                "filter_keys": self.__join_key_conditions_or(key_conditions=[
                    self.__make_key_condition(keys=x, type=Attr)
                    for x in grouped_key_info["filter_keys"]
                ]),
            }



        #-----------------------------------------
        #   登録済みアイテムを検索
        #-----------------------------------------
        # 削除/更新対象となる登録済みアイテムをリストアップ。
        before_items:List[Dict] = []
        for key_condition in key_conditions.values():
            index_keys = key_condition["index_keys"]
            filter_keys = key_condition["filter_keys"]
            
            params: Dict = {
                "IndexName" : index_name,
                "KeyConditionExpression" : index_keys,
            }
            if filter_keys is not None:
                params.update(FilterExpression=filter_keys)


            temp:List[Dict] = list(self.query(**params))
            before_items.extend(temp)



        #-----------------------------------------
        #   削除/更新判定
        #-----------------------------------------

        # 削除対象データを抽出。
        # 登録済みデータと更新アイテムをプライマリーキーで比較。
        delete_items: List[Dict] = []
        for before_item in before_items:
            # 更新データとの比較
            for update_item in items:
                # キー項目ごとに比較
                for key_type, key_name in self.pk_schema.items():
                    before_value:Any = before_item.get(key_name)
                    update_value:Any = update_item.get(key_name)
                    if before_value != update_value:
                        break
                else:
                    # すべてのキーが合致 = 削除対象ではない。
                    break
            else:
                # キーが合致するものがなかった = 削除対象である
                delete_items.append(before_item)


        #-----------------------------------------
        #   データ更新/削除
        #-----------------------------------------

        # 返却データを生成
        key_names_all = [ *index_key_names, *filter_key_names ]
        update_items = items
        result: Dict[str,List[Dict]] = {
            "before" : [ { k:v for k,v in x.items() if k in key_names_all } for x in before_items ] ,
            "delete" : [ { k:v for k,v in x.items() if k in key_names_all } for x in delete_items ] ,
            "upsert" : [ { k:v for k,v in x.items() if k in key_names_all } for x in update_items ] ,
        }


        # アイテムを登録
        self.put_items(Items=update_items, ttl=ttl)

        # アイテムを削除
        self.delete_items(Items=delete_items)


        # 正常終了
        return result


    def truncate(self):
        """データ全削除"""

        # キー項目を抽出
        key_names:str = self._pk_schema.values

        # キー値のリストを生成
        delete_keys:dict = [ { k:v for k,v in x.items() if k in key_names } for x in self.scan() ]

        # データ削除
        with self._table.batch_writer() as batch:
            for key in delete_keys:
                batch.delete_item(Key = key)
        return 0


    def _set_additional_attr(self, item:Dict, ttl:int|datetime|None) -> Dict:
        """オプション属性追加"""

        def __add_ttl(item:Dict, ttl:int|datetime|None) -> Dict:

            # 名称未設定はそのまま返却
            if not self._ttl_name:
                return item

            # item に設定済みの場合はそのまま返却
            if self._ttl_name in item.keys():
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
                ttl_dt = datetime.now() + timedelta(seconds=ttl_tmp)        
            item[self._ttl_name] = int(ttl_dt.timestamp())
            return item


        def __add_updated_at(item:Dict) -> Dict:

            # 名所未設定の場合はそのまま返却
            if not (self._updated_at):
                return item

            # item に設定済みの場合はそのまま返却
            if self._updated_at in item.keys():
                return item

            # 追加して返却
            item[self._updated_at] = datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')
            return item

        # セットして返却
        ret = __add_updated_at(item=item)
        ret = __add_ttl(item=item, ttl=ttl)
        return ret


    def __join_key_conditions_or(self, key_conditions: List[Key|Attr]) -> Or:
        ret = None
        for cond in key_conditions:
            if ret is None:
                ret = cond
            else:
                ret = ret | cond
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
        AND条件のみ対応
        
        :param self: Description
        :param keys: Description
        :type keys: Dict[str, Any]
        :param type: Description
        :type type: Key | Attr
        :param operator: Description
        :type operator: And | Or
        :return: Description
        :rtype: AttributeBase
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

