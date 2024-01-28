import datetime

dt_now = datetime.datetime.now()

print("-- now:")
# print(dir(dt_now))


#---------------------------------
# iso-format
#---------------------------------

print("-- iso-format:")

# datetime -> str
str_iso = dt_now.isoformat()
print(str_iso)      

# str -> datetime
dt_iso = datetime.datetime.fromisoformat(str_iso)
print(dt_iso)

#---------------------------------
# Custom format
#---------------------------------
# 書式はこちらを参照
#   https://docs.python.org/ja/3/library/datetime.html#strftime-and-strptime-format-codes
#---------------------------------

print("-- custom-format:")
format = '%Y/%m/%d %H:%M:%S.%f'

str_custom = dt_now.strftime(format=format)
print(str_custom)

dt_custom = datetime.datetime.strptime(str_custom, format)
print(dt_custom)
