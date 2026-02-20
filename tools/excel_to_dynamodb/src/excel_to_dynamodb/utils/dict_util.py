from typing import Dict,List,Any,Union,Tuple,Self

def from_flatten(flattened_dict: Union[Dict[Tuple, Any], Dict[str, Any]], separator=".") -> dict:
    """ 平坦化 dict から、階層化 dict を再構築"""

    def __dict_from_flatten(pairs: List[Tuple[List, Any]]) -> Dict[Any, Any]:

        # 1階層目のキーで子階層をグルーピング
        pairs_dict: Dict[Any, List] = {}
        last_data: Any = None
        for (path, data) in pairs:
            if len(path) == 0:
                # 最終階層の要素を仮置き（子階層があれば上書きされる）
                last_data = data
            else:
                # 子階層をグルーピング
                current_key = path.pop(0)
                if current_key not in pairs_dict.keys():
                    pairs_dict[current_key] = []
                pairs_dict[current_key].append((path, data))

        # 子階層が存在しない場合は最終階層のデータを
        if len(pairs_dict) == 0:
            return last_data

        # 子階層を再帰処理
        result = {}
        for k, p in pairs_dict.items():
            result[k] = __dict_from_flatten(pairs=p)
        return result

    # 空データの場合はそのまま返却
    if flattened_dict == {}:
        return {}

    # (path, data) の list of tuple に変換
    pairs: List[Tuple[List, Any]] = []
    for path, v in flattened_dict.items():
        path = path.split(separator) if isinstance(path, str) else path
        path = list(path) if isinstance(path, tuple) else path
        path = [path] if not isinstance(path, list) else path
        pairs.append((path, v))


    result: Dict[Any, Any] = __dict_from_flatten(pairs=pairs)
    return result



def map_recursive(data:dict, func:callable):
    """全要素にfunction実行（再起処理）"""
    if isinstance(data, dict):
        return {
            k: map_recursive(v, func)
            for k,v in data.items()
        }
    else:
        return func(data)





class ChainableDict(dict):
    """
    子要素をChain指定可能な拡張 dict
    ---
    階層構造のチェーン表現が可能。
    example)
      data = ChainableDict({"a", {"aa": "XX"}})
      print(f"{data.a}")                      ... {'aa': 'xx'}
      print(f"{data.a.aa}")                   ... xx
      print("{data.a.aa}".format(data=data))  ... xx
    """

    def __init__(self, data:dict):
        # ベースのdictを設定
        super().__init__(data)

        # 階層構造化
        for k,v in data.items():
            if isinstance(v, dict):
                setattr(self, k, ChainableDict(data=v))
            else:
                setattr(self, k, v)

    def __getitem__(self, key:str):
        keys:List[str] = key.split(".")
        ret:Any = getattr(self, keys[0])
        if len(keys) == 1:
            return ret
        else:
            return ret[".".join(keys[1:])]



