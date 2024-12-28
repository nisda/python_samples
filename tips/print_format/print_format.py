
# 参考
#  https://note.nkmk.me/python-print-basic/#_5
#  https://note.nkmk.me/python-f-strings/#f_1


import datetime

val_str = "abcdef"
val_int = 123
val_float = 12345.6789
val_datetime = datetime.datetime.now()


# printf 形式の書き方。推奨されていない。
print("A=%s" % val_str)                                 # 'A=abcdef'
print("A=%10.10s, B=%08.010f" % (val_str, val_float))   # 'A=    abcdef, B=12345.6789000000'

# 変数を割り当てる。シンプル
print(f"str={val_str}")
print(f"datetime={val_datetime}")

# 書式指定も可能
print(f"str={val_str:>20}")
print(f"float={val_float:^010.08}")
print(f"datetime={val_datetime:%Y%m%d.%H%M%S.%f}")


# format



print('left   : {:<20}'.format(val_float))
print('center : {:^20}'.format(val_float))
print('right  : {:>20}'.format(val_float))
print('zero   : {:020}'.format(val_float))
# print('bin    : {:b}'.format(val_float))
# print('oct    : {:o}'.format(val_float))
# print('hex    : {:x}'.format(val_float))

