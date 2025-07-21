#crypto
#forex
#equity
#option
#futures

#instrument
#ticker

#pip install yfinance
import yfinance as yf

ticker1='NVDA'
# data=yf.download(ticker1,period='5d',multi_level_index=False)
# print(data)

# l1=[]
# for i in data.columns:
#     print(i)
#     l1.append(i[0])
# data.columns=l1

import datetime as dt
s=dt.datetime(2020,1,1)


# data=yf.download(ticker1,start='2021-01-01',end='2021-12-31',multi_level_index=False)
# print(data)
# data=yf.download(ticker1,start=s,end='2021-12-31',multi_level_index=False)
# print(data)

# data=yf.download(ticker1,start=s,end='2021-12-31',interval='1d',multi_level_index=False)
# print(data)

# data=yf.download(ticker1,start='2024-01-01',end='2025-07-11',interval='1h',multi_level_index=False)
# print(data)

# data=yf.download(ticker1,start='2025-06-01',end='2025-07-11',interval='30m',multi_level_index=False)
# print(data)

data=yf.download(ticker1,start='2025-07-14',end='2025-07-20',interval='1m',multi_level_index=False,ignore_tz=True)
print(data)

