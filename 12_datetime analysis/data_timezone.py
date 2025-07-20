
# import datetime as dt

# import pytz
# kolkata_tz = pytz.timezone('Asia/Kolkata')

# d1=dt.datetime.now(tz=kolkata_tz)
# print(d1)

#pendulum
#pip3 install pendulum
import pendulum as dt

time_zone1='Asia/Kolkata'
time_zone='America/New_York'
dt1=dt.datetime(2025,7,20)

# print(dt1)
# print(dt.now(tz=time_zone))


start_hour,start_min=7,35
end_hour,end_min=7,40


current_time=dt.now(tz=time_zone)

start_time=dt.datetime(current_time.year,current_time.month,current_time.day,start_hour,start_min,tz=time_zone)
end_time=dt.datetime(current_time.year,current_time.month,current_time.day,end_hour,end_min,tz=time_zone)

print(current_time)
print(start_time)
print(end_time)

print(end_time.in_timezone(time_zone1))


# #before time
# while True:
#     if dt.now(tz=time_zone)>start_time:
#         break
#     print('waiting for start time to reach',dt.now(tz=time_zone))




# def main_strategy():
#     print('running main strategy')



# import time
# while True:

#     dt1=dt.now(tz=time_zone)
#     print(dt1)
#     if dt1>end_time:
#         break


#     #every 5 min
#     if dt1.second==1 and dt1.minute in range(0,50,1):
#         main_strategy()


    
#     time.sleep(1)


# print('we have reach end time so closing program')