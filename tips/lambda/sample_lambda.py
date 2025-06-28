

# -----------------------------------------
# その場で function 定義
# -----------------------------------------
func: callable = lambda x, y: x + y
ret = func(2, 4)    # ret = 6
print(ret)

# -----------------------------------------
# args, kwargs その１
# -----------------------------------------
func: callable = lambda *args, **kwargs: print(args, kwargs)
ret = func("a", "b", 1, 2, k1="v1", k2="v2")


# -----------------------------------------
# args, kwargs その２
# -----------------------------------------
def argfunc(p1, p2, p3, p4):
    return {
        "param1": p1,
        "param2": p2,
        "param3": p3,
        "param4": p4,
    }


func: callable = lambda *args, **kwargs: argfunc("X", *args, **kwargs)
ret = func("b", **{"p4": "4", "p3": "3"})
print(ret)
