
from typing import Dict, Any, List

input_dicts:List[Dict[str, Any]] = [
    {"a": 1, "b": 2, "c": 3, "d": 4},
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5},
    {"a": 1, "b": 2, "c": 3},
    {"c": 3, "b": 2},
]


def extract_dict_common_keys(dicts:List[Dict]) -> List:
    if len(dicts) == 0:
        return []
    results: List = list(dicts[0].keys())
    for d in dicts:
        results = [ k for k in d.keys() if k in results ]
    return results


ret = extract_dict_common_keys(dicts=input_dicts)

print(ret)
