

import datetime


#---------------------------------
# weekday (int)
#---------------------------------
print("-- weekday")

dt_mon = datetime.datetime(year=2024, month=1, day=22)
dt_tue = datetime.datetime(year=2024, month=1, day=23)
dt_wed = datetime.datetime(year=2024, month=1, day=24)
dt_thu = datetime.datetime(year=2024, month=1, day=25)
dt_fri = datetime.datetime(year=2024, month=1, day=26)
dt_sat = datetime.datetime(year=2024, month=1, day=27)
dt_sun = datetime.datetime(year=2024, month=1, day=28)

print(dt_mon.weekday()) # 0
print(dt_tue.weekday()) # 1
print(dt_wed.weekday()) # 2
print(dt_thu.weekday()) # 3
print(dt_fri.weekday()) # 4
print(dt_sat.weekday()) # 5
print(dt_sun.weekday()) # 6

#---------------------------------
# strftime
#---------------------------------
print("-- strftime")
print(dt_thu.strftime(format="%a")) # Thu
print(dt_thu.strftime(format="%A")) # Thursday


#---------------------------------
# 日本語で
#---------------------------------
print("-- 日本語の曜日を表示")

jp_week_words = ['月', '火', '水', '木', '金', '土', '日']
jp_week = jp_week_words[dt_thu.weekday()]
print(jp_week)
