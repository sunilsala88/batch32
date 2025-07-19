

data='2024-01-01'

import datetime as dt

#date
#time
#datetime

d1=dt.date(2025,1,1)
print(d1)

t1=dt.time(11,15,15)
print(t1)

dt1=dt.datetime(2025,7,13,11,15,15)
print(dt1)
#0 mon
#1 tue
#2 wed
#6 sun

i1=dt.timedelta(minutes=2)
print(dt1+i1)


#convert datetime to epoch
print(dt1.timestamp())

#epoch to datetime
n=1752409073
a=dt.datetime.fromtimestamp(n)
print(a)

#datetime to string

# Sunday, 13 July 2025 12:17:53

f='%A, %d %B %Y %H:%M:%S'
s1=dt1.strftime(f)
print(s1)
#string to datetime


s2="Sunday, 13 July 2025 12:17:53"
f='%A, %d %B %Y %H:%M:%S'

d5=dt.datetime.strptime(s2,f)
print(d5)




#all thur of year 2025

# start=dt.datetime(2025,1,1)
# for i in range(365):
    
#     if start.weekday()==3:
#         print(start)
#     start=start+dt.timedelta(days=1)

#creart a fun which shuld giver me current expiry
def get_nearest_expiry(d1):
    start=dt.datetime(2025,1,1)
    for i in range(365):
    
        if start.weekday()==3:
            print(start,(start-d1).days)
            if (start-d1).days>0:
                return start
        start=start+dt.timedelta(days=1)

# d1=dt.datetime.now()
d1=dt.datetime(2025,12,24)
print(d1)
ans=get_nearest_expiry(d1)
print(ans)