import pandas as pd
import pandas_ta as ta
import yfinance as yf
from backtesting import Backtest,Strategy
import numpy as np

# file_name='NIFTY 50_minute'
# file_path=r"D:\NIFTY 50_minute.csv"

# df=pd.read_csv(file_path)
# df=df.drop('volume', axis=1)
# df=df.rename(columns={'date':'Datetime','open':'Open','high':'High','low':'Low','close':'Close'})
# data=df.set_index('Datetime')
# print(data)

def getsma1(close, l):
    sma14=ta.sma(close,l)
    return sma14

def getsma2(close, l):
    sma29=ta.sma(close, l)
    return sma29

def getsma3(close, l):
    sma100=ta.sma(close, l)
    return sma100

class SMA_CROSSOVER(Strategy):
    l1=14
    l2=29
    l3=100

    def init(self):
        Close=self.data.Close.s

        self.sma1=self.I(getsma1,Close,self.l1)
        self.sma2=self.I(getsma2,Close,self.l2)
        self.sma3=self.I(getsma3,Close,self.l3)

    def next(self):
        price=self.data.Close[-1]
        if price>self.sma1[-1]>self.sma2[-1]>self.sma3[-1]:
            BSL=price - 20
            BTGT=price + 20
            self.buy(sl=BSL, tp=BTGT)

        elif price<self.sma1[-1]<self.sma2[-1]<self.sma3[-1]:
            SSL=price + 20
            STGT=price - 20
            self.sell(sl=SSL, tp=STGT)

import yfinance as yf
data=yf.download('^NSEI',period='700d',interval='1h',multi_level_index=False)
data.index = data.index.tz_convert('Asia/Kolkata')

bt=Backtest(data,SMA_CROSSOVER, cash=100000)
output=bt.run()
print(output)
bt.plot()
