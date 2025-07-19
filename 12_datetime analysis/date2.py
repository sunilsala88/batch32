import pandas as pd

df=pd.read_csv('/Users/new algo trading/batch32/11_data_analysis/Unicorn_companies.csv')
print(df)
print(df.info())


# import datetime as dt
# l1=[]
# for i in df['Date Joined']:
#     # print(i)
#     f='%d-%m-%Y'
#     d=(dt.datetime.strptime(i,f))
#     # print(d)
#     l1.append(d)
# df['Date Joined']=l1
# print(df)
# print(df.info())

f='%d-%m-%Y'
df['Date Joined']=pd.to_datetime(df['Date Joined'],format=f)
print(df.info())