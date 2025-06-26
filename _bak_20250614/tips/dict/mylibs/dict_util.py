from typing import Any, Callable, List, Dict, Union
from collections import OrderedDict
import re
import copy
from . import list_util




def compare(dict_left:Dict, dict_right:Dict, compare_paths:List[Union[str, List[Any]]], path_separator=".") -> bool:
    """２つのdictを指定パスの値で比較"""

    # 両方のデータから比較項目を抜き出し
    compare_data_left:List[Any]  = {
        i: get_by_path(data=dict_left, path=compare_paths[i], path_separator=path_separator)
        for i in range(0, len(compare_paths))
    }
    compare_data_right:List[Any] = {
        i: get_by_path(data=dict_right, path=compare_paths[i], path_separator=path_separator)
        for i in range(0, len(compare_paths))
    }

    # 比較
    return bool(compare_data_left == compare_data_right)



def differ(dict_left:Dict, dict_right:Dict, include_same=False):
    """差分取得／未実装"""

    # dictのパスを取得
    paths_left:List[str] = paths(data=dict_left)
    paths_right:List[str] = paths(data=dict_right)

    # パスをマージしてソート
    paths_all = list_util.list_list_sort([*paths_left, *paths_right])

    # 全パスの要素を比較
    differ = []
    prev_path = None
    for path in paths_all:
        # 同一パスは処理しない。
        if prev_path == path: continue
        prev_path = path

        value_left:Any = None
        value_right:Any = None


        # 左の値を取得。存在しなかったら「右のみ」
        try:
            value_left = get_by_path(data=dict_left, path=path)
        except (IndexError, KeyError) as e:
            value_right = get_by_path(data=dict_right, path=path)
            differ.append(('right', path, None, value_right))
            continue

        # 右の値を取得。存在しなかったら「左のみ」
        try:
            value_right = get_by_path(data=dict_right, path=path)
        except (IndexError, KeyError) as e:
            value_left = get_by_path(data=dict_left, path=path)
            differ.append(('left', path, value_left, None))
            continue

        # 両方にパスあり。比較。
        if value_left != value_right:
            differ.append(('diff', path, value_left, value_right))
        elif include_same: 
            differ.append(('same', path, value_left, value_right))
        else:
            pass

    # 正常終了。差分リストを返却。
    return differ


# def extract(dict_data:Dict, paths:List[Union[str, List[Any]]], path_separator=".") -> Dict:
#     pass


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



def get_by_path(data:Any, path:Union[list, str], path_separator='.') -> Any:
    """パス指定で要素を取得"""

    def __get_by_path(data:Any, path:list) -> Any:
        if len(path) == 0:
            return data

        idx = path.pop(0)

        if isinstance(data, list) or isinstance(data, tuple):
            # list/tuple の場合はintに変換
            try:
                node = data[int(idx)]
            except TypeError as e:
                # raise IndexError(f"{e.__class__.__name__}: {e}", idx) 
                raise IndexError(repr(e), idx)

        elif isinstance(data, dict):
            # dict の場合、まずはそのまま取得
            try:
                node = data[idx]
            except KeyError as e:
                try:
                    # NG時、数値型に変換可能な場合は変換して試行
                    idx = float(idx)
                    node = data[idx]
                except TypeError as e:
                    # raise IndexError(f"{e.__class__.__name__}: {e}", idx) 
                    raise KeyError(repr(e), idx)

        if len(path) > 0:
            return __get_by_path(data=node, path=path)
        else:
            return node

    path_copy = copy.deepcopy(path)
    if isinstance(path_copy, str):
        path_copy = path_copy.split(path_separator)

    return __get_by_path(data=data, path=path_copy)



def dict_from_paths(paths:List[List[Any]], values:List[Any]=[], path_separator=".") -> dict:
    """ パス群を dict に変換"""

    def __dict_from_path(path, values, parent_data) -> None:
        """パスを dict に変換"""
        if len(path) == 0: return

        key = path.pop(0)
        if len(path) == 0:
            if len(values) > 0:
                value = values.pop(0)
            else:
                value = None
            if key not in parent_data.keys():
                parent_data[key] = value
        else:
            if key not in parent_data.keys() or not isinstance(parent_data[key], dict):
                parent_data[key] = {}
            __dict_from_path(path, values, parent_data[key])

        return

    paths_copy = copy.deepcopy(paths)
    values_copy = copy.deepcopy(values)
    ret = {}
    for path in paths_copy:
        if isinstance(path, str): path = path.split(sep=path_separator)

        __dict_from_path(
            path=path,
            values=values_copy,
            parent_data=ret)

    return ret




def dict_mapping(data_dict:Dict[str,Any], mapping_dict:Dict, path_separator=".") -> Dict:
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

    def __dict_mapping(data_dict:Dict[str,Any], mapping_dict:Dict, path_separator=".") -> Dict:
        temp:Dict = {}
        for k, v in mapping_dict.items():
            if isinstance(v, dict):
                temp[k] = __dict_mapping(data_dict=data_dict, mapping_dict=v, path_separator=path_separator)
            elif v is None:
                temp[k] = None
            else:
                key_path = list(v) if isinstance(v, (list, tuple)) else v.split(path_separator)
                temp[k] = __get_dict_value(data_dict=data_dict, key_path=key_path)
        return temp

    return __dict_mapping(data_dict=data_dict, mapping_dict=mapping_dict, path_separator=path_separator)


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
        """指定番号の要素を割り当てる"""
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
            return OrderedDict({
                k:sort(data[k])
                for k in list_util.list_sort(data=data.keys())
            })
        else:
            return data
        # return {k:data[k] for k in sorted(data.keys())}

    return __sort(data=data)

