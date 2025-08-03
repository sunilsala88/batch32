
import yfinance as yf
data=yf.download('NVDA',interval='1h',start='2025-01-25',end='2025-07-27',multi_level_index=False)
print(data)

#resample to daily data
d={'Open':'first','High':'max','Low':'min','Close':'last','Volume':'sum'}
data=data.resample('D').agg(d)
data.dropna(inplace=True)
print(data)
import pandas_ta as ta
macd=ta.macd(data['Close'])
print(macd)

import pandas as pd

def macd(close, fast=None, slow=None, signal=None, offset=None, **kwargs):
    """Indicator: Moving Average, Convergence/Divergence (MACD)"""
    
    # Validate arguments
    fast = int(fast) if fast and fast > 0 else 12
    slow = int(slow) if slow and slow > 0 else 26
    signal = int(signal) if signal and signal > 0 else 9
    if slow < fast:
        fast, slow = slow, fast

    # Calculate Exponential Moving Averages (EMA)
    def ema(series, length):
        return series.ewm(span=length, adjust=False).mean()

    # Calculate MACD
    fastma = ema(close, fast)
    slowma = ema(close, slow)
    macd = fastma - slowma
    signalma = ema(macd, signal)
    histogram = macd - signalma

    # Offset
    if offset is not None and offset != 0:
        macd = macd.shift(offset)
        signalma = signalma.shift(offset)
        histogram = histogram.shift(offset)

    # Handle fills
    if "fillna" in kwargs:
        macd.fillna(kwargs["fillna"], inplace=True)
        signalma.fillna(kwargs["fillna"], inplace=True)
        histogram.fillna(kwargs["fillna"], inplace=True)
    if "fill_method" in kwargs:
        macd.fillna(method=kwargs["fill_method"], inplace=True)
        signalma.fillna(method=kwargs["fill_method"], inplace=True)
        histogram.fillna(method=kwargs["fill_method"], inplace=True)

    # Prepare DataFrame to return
    data = {
        'MACD': macd,
        'Signal': signalma,
        'Histogram': histogram
    }
    df = pd.DataFrame(data)

    return df


macd=macd(data['Close'])
print(macd)

# import mplfinance as mpf
# a=mpf.make_addplot(macd['MACD_12_26_9'],color='black',panel=1)
# b=mpf.make_addplot(macd['MACDs_12_26_9'],color='blue',panel=1)
# c=mpf.make_addplot(macd['MACDh_12_26_9'],color='red',panel=1,type='bar')

# mpf.plot(data,type='candle',style='yahoo',addplot=[a,b,c])

# #macd

adx=ta.adx(data['High'], data['Low'], data['Close'])
print(adx)

# import mplfinance as mpf
# a=mpf.make_addplot(adx['ADX_14'],color='black',panel=1)

# mpf.plot(data,type='candle',style='yahoo',addplot=[a])

#atr
#rsi

atr=ta.atr(data['High'], data['Low'], data['Close'])
print(atr)

import mplfinance as mpf
a=mpf.make_addplot(atr,color='black',panel=1)

mpf.plot(data,type='candle',style='yahoo',addplot=[a])