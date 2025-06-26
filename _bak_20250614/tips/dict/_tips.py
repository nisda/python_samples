## 参考: https://blog.yiwkr.work/2020-09-27-python-dict-diff

import difflib
from pprint import pformat


before = {
    'number': 1,
    'tuple': ('aaa', 'bbb', 'ccc'),
    'None': None,
    'dict': {
        'list': [
            'A',
            {'B': [1, 2, 3]},
            ['C'],
            ('F', 'G'),
        ],
    },
}

after = {
    'number': 1,
    'tuple': ('aaa', 'bdb', 'ccc'),
    'None': None,
    'dict': {
        'list': [
            'A',
            {'B': [1, 4, 3]},
            ['C', 'D'],
            ('F',),
        ],
    },
}


def to_string_lines(obj):
    # dictのオブジェクトを文字列に変換＆改行で分割したリストを返却
    return pformat(obj).split('\n')


def diff(obj1, obj2):
    # obj1、obj2を文字列のリストに変換
    lines1 = to_string_lines(obj1)
    lines2 = to_string_lines(obj2)

    # lines1、lines2を比較
    result = difflib.Differ().compare(lines1, lines2)

    # 比較結果を改行で結合して一つの文字列として返却
    return '\n'.join(result)


# 比較結果を表示
ret = diff(before, after)
print(ret)

# print(pformat(before))
# import json
# print(json.dumps(before))
