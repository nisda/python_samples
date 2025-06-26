import mylibs.dict_util as dict_util


def test_sort_1():

  # ソート前のデータ
  original_dict = {
    'banana': {
        "bb" : "casc79",
        "aaaa" : "2523",
        "c" : 1234,
        "aa" : [987,654,"000",321,[],123,"789",456],
        "aaa" : {
          "x" : "6798",
          99  : "ABC",
          "z" : 852,
          111 : "DEF",
          "y" : "exg",
        },
    },
    'apple': 2,
    'cherry': 1
  }

  # ソート実行
  ret = dict_util.sort(original_dict)

  # キーでソートされている。
  assert list(ret.keys())                   == list(sorted(original_dict.keys()))
  assert list(ret["banana"].keys())         == list(sorted(original_dict["banana"].keys()))
  assert list(ret["banana"]["aaa"].keys())  == [99, 111, "x", "y", "z"]

  # オリジナルとは一致しない
  assert list(ret.keys())                   != list(original_dict.keys())
  assert list(ret["banana"].keys())         != list(original_dict["banana"].keys())
  assert list(ret["banana"]["aaa"].keys())  != list(original_dict["banana"]["aaa"].keys())

  # 中のデータには影響なし
  assert ret["banana"]["aa"]  == original_dict["banana"]["aa"]
  assert ret["apple"]         == original_dict["apple"]


