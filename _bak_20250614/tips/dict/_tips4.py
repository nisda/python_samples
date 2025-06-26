from typing import Dict, List, Any
import json
import copy

# merge
def deep_merge(d1:Dict, d2:Dict) -> Dict:
    acc = d1.copy()
    for k, v in d2.items():
        if isinstance(v, dict) and isinstance(acc[k], dict):
            acc[k] = deep_merge(acc[k], v)
        else:
            acc[k] = v
    return acc


if __name__ == '__main__':
    d1 = {
        "a" : "A",
        "b" : "B",
        "c" : {
            "ca" : "CA",
            "cb" : "CB",
        },
    }
    d2 = {
        "b" : "BBB",
        "c" : {
            "cb" : "CCCBBB",
            "cc" : "CCCCCC",
        },
        "d" : "DDD"
    }

    ret = deep_merge(d1=d1, d2=d2)
    print(json.dumps(ret, indent=2))
