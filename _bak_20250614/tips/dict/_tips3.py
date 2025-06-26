
keys1 = [
    ["a", "b", "c"],
    [1, 2, 3],
    ["a", "b", "c", "d"],
    ["A", "B", "C"],
]

keys2 = [
    [1, 2, 3],
    ["あ", "い", "う"],
    ["a", "b", "c"],
]

# ▼ set で TypeError: unhashable type: 'list'。ハッシュ化できない。
# keyset_b = sorted(set(keys1) & set(keys2), key=keys1.index) # 両方に存在
# keyset_1 = sorted(set(keys1) - set(keys2), key=keys1.index) # 1のみに存在
# keyset_2 = sorted(set(keys2) - set(keys1), key=keys2.index) # 2のみに存在

from pprint import pformat

list = sorted([ pformat(x) for x in keys1 ], key=keys1.index)
print(list)
