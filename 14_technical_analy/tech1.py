
import yfinance as yf
data=yf.download('NVDA',interval='1m',start='2025-07-25',end='2025-07-27',multi_level_index=False)
print(data)

# import talib
# import pandas_ta


import pandas_ta as ta
data['sma']=ta.sma(data['Close'],length=10)
data


# import talib as ta
# data['sma2']=ta.SMA(data['Close'],10)
# print(data)


# data['ema']=ta.ema(data['Close'],10)
# print(data)

d=ta.bbands(data['Close'],20)
print(d)

import mplfinance as mpf
a=mpf.make_addplot(d['BBL_20_2.0'],color='black')
b=mpf.make_addplot(d['BBM_20_2.0'],color='blue')
c=mpf.make_addplot(d['BBU_20_2.0'],color='green')
mpf.plot(data,type='candle',style='yahoo',addplot=[a,b,c])

