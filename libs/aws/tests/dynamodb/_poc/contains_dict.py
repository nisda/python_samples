

source_dict = {"a": 1, "b": 2, "c": 3, "d": 4, "e": [1, 2], "f": {"AA":"AA", "BB": "BB"} }
compare_dict = {"a": 1, "b": 2, "c": 3, "d": 4, "e": [1, 2], "f": {"BB": "BB", "AA":"AA"} }

ret = compare_dict.items() <= source_dict.items()
print(ret)

