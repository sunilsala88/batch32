import yfinance as yf

data=yf.download('^NSEI',start='2025-07-20',end='2025-07-25',interval='1m',multi_level_index=False,ignore_tz=True)
print(data)

name='NVDA'
ticker1=yf.Ticker(name)
# print(ticker1.get_info())

import pandas as pd
d=pd.Series(ticker1.get_info())
# d.to_csv('data.csv')

d1=ticker1.get_info()
b1=d1.get('beta')
print(b1)