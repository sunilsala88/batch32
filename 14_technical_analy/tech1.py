
import yfinance as yf
data=yf.download('NVDA',interval='1m',start='2025-07-25',end='2025-07-27',multi_level_index=False)
print(data)

# import talib
# import pandas_ta