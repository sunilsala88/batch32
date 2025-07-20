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

# f='%d-%m-%Y'
# df['Date Joined']=pd.to_datetime(df['Date Joined'],format=f)
# print(df.info())


data2=pd.read_html('https://en.wikipedia.org/wiki/NIFTY_50')
data2=data2[1]
data2

list2=[]
for i in data2['Date added[16]']:
    if i[-3]=='[':
        list2.append(i[:-3])
    else:
        list2.append(i)
data2['Date added[16]']=list2
print(data2)
# print(data2.info())


data2['Date added[16]']=pd.to_datetime(data2['Date added[16]'])
print(data2.info())
print(data2)

# import datetime as dt
# dt1=dt.datetime.now()
# print(dt1.year)
# data3=data2[data2['Date added[16]'].dt.year>2023]
# l1=data3['Symbol'].to_list()
# print(l1)

print(data2[data2['Date added[16]'].dt.weekday==2]['Symbol'].to_list())

# import yfinance as yf
# data=yf.download('TSLA',interval='1m',period='3d')
# print(data.to_csv('data.csv'))