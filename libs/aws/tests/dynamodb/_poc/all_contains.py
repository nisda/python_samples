

targets = ["a", "b", "d", "x"]
wholes = ["a", "b", "c", "d", "e"]


ret = all(item in wholes for item in targets)
print(ret)