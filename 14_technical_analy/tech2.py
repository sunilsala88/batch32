
import yfinance as yf
data=yf.download('NVDA',interval='1h',start='2025-01-25',end='2025-07-27',multi_level_index=False)
print(data)

import pandas_ta as ta
super=ta.supertrend(data['High'],data['Low'],data['Close'])
print(super.tail(20))



import mplfinance as mpf
a=mpf.make_addplot(super['SUPERTl_7_3.0'],color='black')
b=mpf.make_addplot(super['SUPERTs_7_3.0'],color='blue')

mpf.plot(data,type='candle',style='yahoo',addplot=[a,b])