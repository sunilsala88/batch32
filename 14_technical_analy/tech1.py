
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

import pandas as pd
import numpy as np

def bbands(close, length=None, std=None, ddof=0, mamode=None, talib=None, offset=None, **kwargs):
    # Validate arguments
    if length is not None and length > 0:
        length = int(length)
    else:
        length = 5
    
    if std is not None and std > 0:
        std = float(std)
    else:
        std = 2.0
    
    if mamode is not None and isinstance(mamode, str):
        mamode = mamode.lower()
    else:
        mamode = 'sma'
    
    if ddof >= 0 and ddof < length:
        ddof = int(ddof)
    else:
        ddof = 1
    
    if close is None:
        return None
    
    if offset is not None and offset != 0:
        offset = int(offset)
    else:
        offset = 0
    
    # Calculate the moving average (mid band)
    if mamode == 'ema':
        mid = close.ewm(span=length, adjust=False).mean()
    else:  # Default to SMA
        mid = close.rolling(window=length).mean()
    
    # Calculate the standard deviation
    stdev = close.rolling(window=length).std(ddof=ddof)
    
    # Calculate upper and lower bands
    deviations = std * stdev
    upper = mid + deviations
    lower = mid - deviations
    
    # Calculate bandwidth and percent (%b)
    ulr = upper - lower
    ulr = ulr.replace(0, 1e-7)  # Avoid division by zero
    
    bandwidth = 100 * ulr / mid
    percent = (close - lower) / ulr
    
    # Apply offset
    if offset != 0:
        upper = upper.shift(offset)
        mid = mid.shift(offset)
        lower = lower.shift(offset)
        bandwidth = bandwidth.shift(offset)
        percent = percent.shift(offset)
    
    # Handle NaNs
    fillna = kwargs.get('fillna', None)
    if fillna is not None:
        upper.fillna(fillna, inplace=True)
        mid.fillna(fillna, inplace=True)
        lower.fillna(fillna, inplace=True)
        bandwidth.fillna(fillna, inplace=True)
        percent.fillna(fillna, inplace=True)
    
    fill_method = kwargs.get('fill_method', None)
    if fill_method is not None:
        upper.fillna(method=fill_method, inplace=True)
        mid.fillna(method=fill_method, inplace=True)
        lower.fillna(method=fill_method, inplace=True)
        bandwidth.fillna(method=fill_method, inplace=True)
        percent.fillna(method=fill_method, inplace=True)
    
    # Name the series
    suffix = f"{length}_{std}"
    lower.name = f"BBL_{suffix}"
    mid.name = f"BBM_{suffix}"
    upper.name = f"BBU_{suffix}"
    bandwidth.name = f"BBB_{suffix}"
    percent.name = f"BBP_{suffix}"
    
    # Prepare DataFrame
    data = {
        lower.name: lower,
        mid.name: mid,
        upper.name: upper,
        bandwidth.name: bandwidth,
        percent.name: percent
    }
    df = pd.DataFrame(data)
    df.name = f"BBANDS_{suffix}"
    
    return df

d=bbands(data['Close'],30)
print(d)




#atr
atr1=ta.atr(data['High'],data['Low'],data['Close'],10)
print(atr1)

import mplfinance as mpf
a=mpf.make_addplot(d['BBL_30_2.0'],color='black')
b=mpf.make_addplot(d['BBM_30_2.0'],color='blue')
c=mpf.make_addplot(d['BBU_30_2.0'],color='green')
d=mpf.make_addplot(atr1,color='red',panel=1)
mpf.plot(data,type='candle',style='yahoo',addplot=[a,b,c,d])