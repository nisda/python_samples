
#*********************************************
# 三項演算子的なもの。
# NULL以外でも使える（NULL_IFに限らない）
#*********************************************

val = "X"
ret = "alt" if val is None else val
print(f"A-1: {ret}")    # -> X

val = None
ret = "alt" if val is None else val
print(f"A-2: {ret}")    # -> alt


#*********************************************
# or 
# 最初の空値以外を返す。
# SQL の coalesce に該当する記述方法
#*********************************************

val = "X"
ret = val or "alt"
print(f"B-1: {ret}")    # -> X

val = None
ret = val or "alt"
print(f"B-2: {ret}")    # -> alt

val = ""
ret = val or "alt"
print(f"B-3: {ret}")    # -> alt

val = 0
ret = val or "alt"
print(f"B-4: {ret}")    # -> alt

val = {}
ret = val or "alt"
print(f"B-5: {ret}")    # -> alt

val = {}
ret = None or '' or b'' or {} or 0 or [] or False or "A" or "B" or "C"
print(f"B-6: {ret}")    # -> A


