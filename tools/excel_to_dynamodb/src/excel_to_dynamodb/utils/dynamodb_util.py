from typing import List, Dict, Any, Tuple
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer, Binary
import boto3
import boto3.session
from boto3.dynamodb.conditions import AttributeBase, Key, Attr, Or
from collections.abc import Generator, Iterator
from enum import Enum, auto
from datetime import datetime

class IndexType(Enum):
    ALL = auto()
    Primary = auto()
    GSI = auto()
    LSI = auto()


class KeyConditionType(Enum):
    Key = auto()
    Attr = auto()


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


    def put_items(self, Items:List[dict]):
        """データ追加（複数）"""

        # データ追加
        with self.__table.batch_writer() as batch:
            for item in Items:
                batch.put_item(Item = item)
        return 0


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


    def delete_items(self, Items:List[dict]):
        """データ削除（複数）"""

        # キー項目を抽出
        key_names:str = [ x["AttributeName"] for x in self.__table.key_schema ]

        # キー値のリストを生成
        delete_keys:dict = [ { k:v for k,v in x.items() if k in key_names } for x in Items ]

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


    def indexes(self, Type:IndexType=IndexType.ALL) -> List[Dict[str,Any]]:
        result:List = []

        # Table Index
        if Type in [IndexType.ALL, IndexType.Primary]:
            idx:List = self.__table.key_schema
            if idx is not None:
                result.append({"Type" : "Primary", "KeySchema" : idx})

        # Global Secondary Index
        if Type in [IndexType.ALL, IndexType.GSI]:
            gsis:List = self.__table.global_secondary_indexes
            if gsis is not None:
                result.extend([{ "Type" : "GSI", **x } for x in gsis])

        # Local Secondary Index
        if Type in [IndexType.ALL, IndexType.LSI]:
            lsis:List = self.__table.local_secondary_indexes
            if lsis is not None:
                result.extend([ { "Type" : "GSI", **x } for x in lsis])

        return result


    def index(self, IndexName:str=None) -> Dict|None:
        """
        Docstring for index
        
        :param IndexName: 取得するIndex名。PrimaryIndexの場合はNULLを指定。
        :type IndexName: str
        """

        if IndexName is None:
            indexes:List[Dict[str,Any]] = self.indexes(Type=IndexType.Primary)
            return indexes[0]
        else:
            indexes:List[Dict[str,Any]] = self.indexes(Type=IndexType.ALL)
            match_idx:List[Dict] = [x for x in indexes if x.get("IndexName", None) == IndexName ]
            return match_idx[0] if len(match_idx) == 1 else None


    def delete_upsert(self, UpdateItems:List[Dict], IndexName:str=None, KeyNames:List[str]=None, updated_at:str="_updated_at") -> Dict:
        """
        データの洗い替え(DELETE/INSERT/UPDATE)
        ---
        データを洗い替える。
        更新データの比較キー項目と一致する既存データを削除/更新対象とする。

        :param keys: UpdateItems 更新データのリスト
        :type type: List[Dict]
        :param type: IndexName 検索に使用するINDEX。Null時はプライマリーINDEXを使用。
        :type type: str
        :param keys: KeyNames 比較キー項目名。INDEXキー以外の項目も指定可。PKは必須。Null時は指定INDEXの全項目を適用。
        :type type: List[Dict]
        :param keys: updated_at 更新日時を自動追加する場合に項目名を指定。None または 空文字で追加しない。
        :type type: str
        """

        #-----------------------------------------
        #   事前処理
        #-----------------------------------------
        # 処理要否チェック: UpdateItems が空の場合は何もしない
        if not UpdateItems:
            return {}


        #-----------------------------------------
        #   INDEX の情報を取得
        #-----------------------------------------

        # プライマリINDEX
        primary_index_defs: Dict[str, str] = self.index(IndexName=None)
        primary_index_defs = { x["KeyType"]:x["AttributeName"] for x in primary_index_defs["KeySchema"] }

        # 検索INDEX
        search_index_defs: Dict[str,str]
        if IndexName is None:
            # IndexName指定がない場合はプライマリを使用。
            search_index_defs = pri_index_keys
        else:
            # INDEX情報を取得。INDEX非存在時はエラー
            index_temp: Dict[str, Any] = self.index(IndexName=IndexName)
            if index_temp is None:
                raise NameError(f"Index `{IndexName}` does not exist.")
            search_index_defs   = { x["KeyType"]:x["AttributeName"] for x in index_temp["KeySchema"] }

        #-----------------------------------------
        #   更新前チェック
        #-----------------------------------------

        # 更新データのプライマリーキー項目に未設定のものがあればエラーとする。
        # 登録処理の途中でエラーとしないために、事前に落とす。
        for update_item in UpdateItems:
            for key_type, key_name in primary_index_defs.items():
                if update_item.get(key_name, None) is None:
                    raise ValueError(f"{key_type}-KEY `{key_name}` is not set in UpdateItem.")


        #-----------------------------------------
        #   比較キーの生成
        #-----------------------------------------
        # KeyNames の振り分け
        index_key_names:List[str] = []   # KeyCondition用
        filter_key_names:List[str] = []  # Filter用
        if KeyNames is None:
            # 指定なしの場合はINDEX項目すべてを採用する。
            index_key_names = [ v for v in search_index_defs.values() ]
            filter_key_names = []
        else:
            # Hashキーが含まれていなかったらエラー
            if search_index_defs["HASH"] not in KeyNames:
                raise ValueError(f"HASH-KEY `{index_keys["HASH"]}` is required for KeyNames.")
            index_key_names  = [ x for x in KeyNames if x in search_index_defs.values() ]
            filter_key_names = [ x for x in KeyNames if x not in search_index_defs.values() ]


        #-----------------------------------------
        #   検索条件リストを生成
        #-----------------------------------------

        # 全アイテムの検索キー部分のみを抽出してリスト化
        search_keys: List[Dict] = [
            {
                "index_keys"  : { k: item.get(k, None) for k in index_key_names},
                "filter_keys" : { k: item.get(k, None) for k in filter_key_names},
            }
            for item in UpdateItems
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
                "IndexName" : IndexName,
                "KeyConditionExpression" : index_keys,
            }
            if filter_keys is not None:
                params.update(FilterExpression=filter_keys)


            temp:List[Dict] = self.query(**params)
            before_items.extend(temp)



        #-----------------------------------------
        #   削除/更新判定
        #-----------------------------------------

        # 削除対象データを抽出。
        # 登録済みデータと更新アイテムをプライマリーキーで比較。
        delete_items: List[Dict] = []
        for before_item in before_items:
            # 更新データとの比較
            for update_item in UpdateItems:
                # キー項目ごとに比較
                for key_type, key_name in primary_index_defs.items():
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
        update_items = UpdateItems
        result: Dict[str,List[Dict]] = {
            "before" : before_items,
            "delete" : delete_items,
            "upsert" : update_items,
        }


        # 追加更新アイテムをPUT
        if updated_at:
            dt_now_str:str = datetime.now().strftime('%Y/%m/%d %H:%M:%S.%f')[:-3]
            update_items:List[Dict] = [
                {
                    **item,
                    f"{updated_at}": dt_now_str,
                }
                for item in UpdateItems
            ]

        # アイテムを登録
        self.put_items(Items=update_items)

        # アイテムを削除
        self.delete_items(Items=delete_items)


        # 正常終了
        return result



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
            type:Key|Attr) -> AttributeBase:
        """
        Docstring for __make_key_condition  
        Key/Filterの条件リソースインタフェースを生成  
        AND条件のみ対応

        :param keys: Description
        :type keys: Dict[str, Any]
        :param type: Description
        :type type: KeyConditionType
        """


        # condition_if: AttributeBase = None
        # if type == KeyConditionType.Key:
        #     condition_if = Key
        # if type == KeyConditionType.Attr:
        #     condition_if = Attr

        ret = None
        for k,v in keys.items():
            if ret is None:
                ret = type(k).eq(v)
            else:
                ret = ret & type(k).eq(v)
        return ret


    def __make_hashable(self, obj) -> Tuple[Any]:
        if isinstance(obj, dict):
            return tuple(sorted((k, self.__make_hashable(v)) for k, v in obj.items()))
        elif isinstance(obj, list):
            return tuple(self.__make_hashable(i) for i in obj)
        else:
            return obj

