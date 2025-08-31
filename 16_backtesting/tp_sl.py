

from backtesting import Backtest,Strategy
import yfinance as yf
import pandas as pd
import numpy as np

#yfinance
data=yf.download('AMZN',period='5y',multi_level_index=False)
print(data)

import pandas_ta as ta

s=ta.supertrend(data['High'],data['Low'],data['Close'])
print(s)


def supertrend(high, low, close, length=10, multiplier=3):
    """
    Supertrend function that matches pandas_ta.supertrend output.
    
    Args:
        high (pd.Series): Series of high prices
        low (pd.Series): Series of low prices
        close (pd.Series): Series of close prices
        length (int): The ATR period. Default: 7
        multiplier (float): The ATR multiplier. Default: 3.0
    
    Returns:
        pd.DataFrame: DataFrame with columns:
            SUPERT - The trend value
            SUPERTd - The direction (1 for long, -1 for short)
            SUPERTl - The long values
            SUPERTs - The short values
    """
    # Calculate ATR using the pandas_ta method (RMA - Rolling Moving Average)
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = true_range.ewm(alpha=1/length, adjust=False).mean()

    # Calculate basic bands
    hl2 = (high + low) / 2
    upperband = hl2 + (multiplier * atr)
    lowerband = hl2 - (multiplier * atr)

    # Initialize direction and trend
    direction = [1]  # Start with long
    trend = [lowerband.iloc[0]]  # Start with lowerband
    long = [lowerband.iloc[0]]
    short = [np.nan]

    # Iterate through the data to calculate the Supertrend
    for i in range(1, len(close)):
        if close.iloc[i] > upperband.iloc[i - 1]:
            direction.append(1)
        elif close.iloc[i] < lowerband.iloc[i - 1]:
            direction.append(-1)
        else:
            direction.append(direction[i - 1])
            if direction[i] == 1 and lowerband.iloc[i] < lowerband.iloc[i - 1]:
                lowerband.iloc[i] = lowerband.iloc[i - 1]
            if direction[i] == -1 and upperband.iloc[i] > upperband.iloc[i - 1]:
                upperband.iloc[i] = upperband.iloc[i - 1]

        if direction[i] == 1:
            trend.append(lowerband.iloc[i])
            long.append(lowerband.iloc[i])
            short.append(np.nan)
        else:
            trend.append(upperband.iloc[i])
            long.append(np.nan)
            short.append(upperband.iloc[i])

    # Create DataFrame to return
    df = pd.DataFrame({
        "SUPERT": trend,
        "SUPERTd": direction,
        "SUPERTl": long,
        "SUPERTs": short,
    }, index=close.index)

    return df

s=supertrend(data['High'],data['Low'],data['Close'])
print(s)

def super1(high,low,close,l=10,m=3):
    s=supertrend(high,low,close,l,m)
    # return (s[f'SUPERT_{l}_{m}.0'])
    return s['SUPERT']

def trend(high,low,close,l=10,m=3):
    s=supertrend(high,low,close,l,m)
    # return (s[f'SUPERTd_{l}_{m}.0'])
    return s['SUPERTd']

class Superstrategy(Strategy):
    l=5
    m=2
    sl1=0.05
    def init(self):
        self.super=self.I(super1,self.data.High.s,self.data.Low.s,self.data.Close.s,self.l,self.m)
        self.trend=self.I(trend,self.data.High.s,self.data.Low.s,self.data.Close.s,self.l,self.m)

    def next(self):
        

        if self.trend[-1]==1 and ((not self.position) or (self.position.is_short)):
            self.position.close()
            buy_price=self.data.Close[-1]
            self.buy(sl=buy_price*(1-self.sl1))
        elif self.trend[-1]==-1 and ((not self.position) or (self.position.is_long)):
            self.position.close()
            buy_price=self.data.Close[-1]
            self.sell(sl=buy_price*(1+self.sl1))


print(super1(data['High'],data['Low'],data['Close']))
print(trend(data['High'],data['Low'],data['Close']))

bt=Backtest(data,Superstrategy,cash=10_000)
output=bt.run()
print(output)
bt.plot()



output=bt.optimize(sl1=[0.01,0.02,0.03,0.04,0.05,0.06,0.07],maximize='Return [%]')
print(output)
print(output['_strategy'])
bt.plot()