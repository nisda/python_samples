import datetime

dt_now = datetime.datetime.now()

print("-- now:")


#---------------------------------
# unix time
#---------------------------------

print("-- unix-time:")

# datetime -> unixtime
unixtime = dt_now.timestamp()
print(type(unixtime))   # <class 'float'>
print(unixtime)      

# unixtime -> datetime
str_unixtime = datetime.datetime.fromtimestamp(unixtime)
print(str_unixtime)
