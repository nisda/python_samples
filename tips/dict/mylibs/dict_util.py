from typing import Any, Callable, List, Dict, Union
from collections import OrderedDict
import re
import copy

"""
▼済
ソート
マップ（全要素処理）
Noneの項目を取り除く（remove_null）
含んでいるかチェック
dictのlistから任意条件のデータを抽出する。
データマッピング for list（指定の構造に変換）
データマッピング for dict（指定の構造に変換）
パスの一覧を取得

▼作りたい
クレンジング → map + func でイケる。
DIFF or compare?

"""

def differ(data_left:Dict, data_right:Dict):
    """差分取得／未実装"""
    pass


def get_by_path(data:Any, path:Union[list, str], str_path_separator='.') -> Any:
    """パス指定で要素を取得"""

    def __get_by_path(data:Any, path:list) -> Any:
        if len(path) == 0:
            return data

        idx = path.pop(0)
        if isinstance(data, list) or isinstance(data, tuple):
            node = data[int(idx)]
        elif isinstance(data, dict):
            node = data.get(idx)

        if len(path) > 0:
            return __get_by_path(data=node, path=path)
        else:
            return node

    path_copy = copy.deepcopy(path)
    if isinstance(path_copy, str):
        path_copy = path_copy.split(str_path_separator)
    return __get_by_path(data=data, path=path_copy)



def paths(data:dict) -> List[List[Any]]:
    """パスのリストを取得。"""

    # set型は非対応。
    # list化すれば処理は可能だが、順番が保証されないためpathとして利用が困難。

    def __get_paths(data) -> list:
        def __merge_names(current_name, child_names) -> list:
            if len(child_names) == 0:
                return [[current_name]]
            else:
                for name in child_names:
                    name.insert(0, current_name)
                return child_names

        if isinstance(data, dict) and len(data) > 0:
            paths = []
            for k, v in data.items():
                child_paths = __get_paths(v)
                paths.extend(__merge_names(k, child_paths))
            return paths
        elif isinstance(data, list):
            paths = []
            for i in range(0, len(data)):
                child_paths = __get_paths(data[i])
                paths.extend(__merge_names(i, child_paths))
            return paths
        else:
            return []
    return __get_paths(data=data)


def dict_mapping(data_dict:Dict[str,Any], mapping_dict:Dict, key_path_separator=".") -> Dict:
    """dictの値を指定のdict構造にマッピング"""

    def __get_dict_value(data_dict:Dict[str,Any], key_path:List[str]) -> Any:
        if len(key_path) == 0:
            return None
        else:
            key = key_path.pop(0)
            if len(key_path) > 0:
                node = data_dict.get(key, {})
                return __get_dict_value(data_dict=node, key_path=key_path)
            else:
                return data_dict.get(key, None)

    def __dict_mapping(data_dict:Dict[str,Any], mapping_dict:Dict, key_path_separator=".") -> Dict:
        temp:Dict = {}
        for k, v in mapping_dict.items():
            if isinstance(v, dict):
                temp[k] = __dict_mapping(data_dict=data_dict, mapping_dict=v, key_path_separator=key_path_separator)
            elif v is None:
                temp[k] = None
            else:
                key_path = list(v) if isinstance(v, (list, tuple)) else v.split(key_path_separator)
                temp[k] = __get_dict_value(data_dict=data_dict, key_path=key_path)
        return temp

    return __dict_mapping(data_dict=data_dict, mapping_dict=mapping_dict, key_path_separator=key_path_separator)


def list_mapping(data_list:List[Any], mapping_dict:dict, auto_order:bool=True) -> Dict:
    """listの値を指定のdict構造にマッピング"""

    def __mapping_auto_order(data_list:List[Any], mapping_dict:dict) -> Dict:
        """上から順に割り当てる"""
        ret:Dict = {}
        for k,v in mapping_dict.items():
            if isinstance(v, dict):
                ret[k] = __mapping_auto_order(data_list=data_list, mapping_dict=v)
            else:
                if len(data_list) > 0:
                    ret[k] = data_list.pop(0)
                else:
                    ret[k] = None
        return ret


    def __mapping_specify_order(data_list:List[Any], mapping_dict:dict) -> Dict:
        """上から順に割り当てる"""
        ret:Dict = {}
        for k,v in mapping_dict.items():
            if isinstance(v, dict):
                ret[k] = __mapping_specify_order(data_list=data_list, mapping_dict=v)
            elif v is None:
                ret[k] = None
            else:
                if len(data_list) > v:
                    ret[k] = data_list[v]
                else:
                    ret[k] = None
        return ret

    if auto_order:
        # 元のデータが編集されないようにコピーして処理開始
        data_list_copy = copy.deepcopy(data_list)
        return __mapping_auto_order(data_list=data_list_copy, mapping_dict=mapping_dict)
    else:
        return __mapping_specify_order(data_list=data_list, mapping_dict=mapping_dict)


def search(data_list:List[dict], condition:dict) -> List[Dict]:
    """dictのlistを検索"""
    return [
        x for x in data_list
        if is_contains(data=x, condition=condition)
    ]


def is_contains(data:dict, condition:dict) -> bool:
    """dictの比較"""

    if isinstance(condition, dict):
        # dict の場合は子要素を比較

        # 両方dictでなかったらNG
        if not isinstance(data, dict):
            return False

        # conditionで指定されたkeyがすべて含まれていなかったらNG
        if ( (data.keys() & condition.keys()) ^ condition.keys() ):
            return False

        # 再帰呼び出しで下層を比較
        for k in condition.keys():
            if not is_contains(data=data[k], condition=condition[k]):
                return False

        # 再帰呼び出しがすべて通ったらTrue
        return True

    elif isinstance(condition, list):
        # 条件が list の場合は指定の方法で比較

        # 処理の共通化のためlistに変換
        if not isinstance(data, list):
            data = [data]

        # データが存在しない場合は必ず False
        if len(data) == 0: return False


        # いずれか１つを含む
        for d in data:
            for c in condition:
                if is_contains(data=d, condition=c):
                    return True
        return False


    elif isinstance(condition, re.Pattern):
        # condition が正規表現の場合、それにマッチしたらOK
        return bool(condition.match(data))

    elif isinstance(condition, Callable):
        # condition が Callable のときはデータをパラメータにしてコール
        return bool(condition(data))

    else:
        # それ以外のパターンは値として比較
        return bool(data == condition)


def map(data:Any, func:Callable) -> dict:
    """dictに再帰的map処理"""

    def __map(data:Any, func:Callable, current_key) -> dict:
        # すべての要素で func を実行。
        # dictやlistでも実行
        data = func(current_key, data)

        if isinstance(data, dict):
            # dict 再帰処理。
            return {
                k : __map(data=v, func=func, current_key=k)
                for k,v in data.items()
            }
        elif isinstance(data, list):
            # list 再帰処理。
            return [
                __map(data=v, func=func, current_key=current_key)
                for v in data
            ]
        else:
            # 最初の処理で変換済みのデータを返却
            return data

    return __map(data=data, func=func, current_key=None)


def remove_null(data:dict) -> dict:
    """dictからnull(None)要素を削除"""

    def __dict_converter(key, value):
        # dict 以外は何もしない
        if not isinstance(value, dict): return value
        return { k:v for k,v in value.items() if v is not None }

    return map(
        data=data,
        func=lambda k,v : __dict_converter(key=k, value=v)
    )


def sort(data:dict) -> OrderedDict:
    """dictの再帰的ソート"""
    def __sort(data:Any):
        if isinstance(data, dict):
            data = {k:sort(v) for k,v in data.items()}
        else:
            return data
        # return {k:data[k] for k in sorted(data.keys())}
        return OrderedDict(sorted(data.items()))

    return __sort(data=data)

