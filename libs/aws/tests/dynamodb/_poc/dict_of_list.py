from typing import List, Dict, Any

input:List[Dict[str, Any]] = [
    1,
    {"id": 1, "name": "alan"},
    {"id": 2, "name": "bob"},
    {"id": 1, "name": "alan"},
    {"id": 2, "name": "bob", "parents": {"dad": "john", "mam": "mary"}},
]



def uniq(input:List) -> List:
    ret = []
    for x in input:
        if x not in ret:
            ret.append(x)
    return ret

ret = uniq(input=input)

print(ret)

