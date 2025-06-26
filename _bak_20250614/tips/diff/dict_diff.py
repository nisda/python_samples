#********************************************
# dict を比較してくれるようなものは無さそう。
# dict->str->list に変換する。
#********************************************

import difflib
import json


d1 = {
    "a": 1,
    "b": 2,
    "c": [123, "vslrkjn", 7498327, None],
    "d": {
        "da": 124,
        "db": "DBDBDBD",
        "dc": "dcdc",
        "dx": "DXDXDX",
    },
    "x": "XXX",
    "y": "YYY",
}
d2 = {
    "a": 1,
    "b": 222,
    "x": "XXX",
    "y": "YYY",
    "c": ["vslrkjn", 7498327, None, 999],
    "d": {
        "dx": "DXDXDX",
        "db": "bd",
        "dc": "dcdc",
        "da": 124,
    },
}

s1 = json.dumps(d1, sort_keys=True, indent=2).split("\n")
s2 = json.dumps(d2, sort_keys=True, indent=2).split("\n")

print(s1)
print(s2)

print()
print("===========================================")
print("ndiff")
print("===========================================")
res = difflib.ndiff(s1, s2)
print('\n'.join(res))

print()
print("===========================================")
print("context_diff")
print("===========================================")
res = difflib.context_diff(s1, s2)
print('\n'.join(res))

print()
print("===========================================")
print("unified_diff")
print("===========================================")
res = difflib.unified_diff(s1, s2)
print('\n'.join(res))

