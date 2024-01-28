import datetime
import time

#---------------------------------
# DIFF
#---------------------------------

print("-- diff")

dt_1 = datetime.datetime.now()
time.sleep(1)
dt_2 = datetime.datetime.now()

dt_diff = dt_2 - dt_1
print(type(dt_diff))    # <class 'datetime.timedelta'>
print(dt_diff)          # 0:00:01.xxxxxx
print(dt_diff.seconds)  # 1


#---------------------------------
# 日時の加算・減算 (timedelta)
#---------------------------------
print("-- add/sub (timedelta)")

dt_base = datetime.datetime.now()

dt_add = dt_base + datetime.timedelta(days=1)       
print(dt_add)

dt_sub1 = dt_base + datetime.timedelta(hours=-1)
print(dt_sub1)

dt_sub2 = dt_base - datetime.timedelta(hours=2)
print(dt_sub2)

### ↓ これはエラーになる。timedeltaの最大単位がdays
# dt_sub1 = dt_org + datetime.timedelta(months=-1) 
# print(dt_sub1)



#---------------------------------
# 日時の加算・減算 (timedelta)
#---------------------------------
print("-- add/sub (relativedelta)")
from dateutil.relativedelta import relativedelta    # 標準ライブラリのはず

dt_base = datetime.datetime.now()

dt_add = dt_base + relativedelta(years=1)     
print(dt_add)

dt_sub1 = dt_base + relativedelta(years=-1)  
print(dt_sub1)


