import pandas as pd

data=pd.read_csv('data.csv')
print(data)
print(data.columns)
data.drop(['symbol','trade_count','vwap'],axis=1,inplace=True)

data.rename(columns={'timestamp':'Datetime','open':'Open','high':'High','low':'Low','close':'Close'},inplace=True)

data['Datetime']=pd.to_datetime(data['Datetime'])
# data['Datetime']=data['Datetime'].dt.tz_convert('US/Eastern')

data.set_index('Datetime',inplace=True)
print(data)
print(data.info())
csv_data=data.copy()

import yfinance as yf
import pandas_ta as ta
from backtesting import Backtest,Strategy
data=yf.download('ETH-USD',start='2025-01-01',end='2025-08-20',interval='1h',multi_level_index=False)
print(data)
print(data.info())


def get_sma(close_price,lengtht):
    sma=ta.sma(close_price,lengtht)
    return sma

class sma_strategy(Strategy):
    s1=30
    s2=60
    def init(self):
        self.sma1=self.I(get_sma,self.data.df.Close,self.s1)
        self.sma2=self.I(get_sma,self.data.df.Close,self.s2)

    def next(self):
        if self.sma1[-1]>self.sma2[-1] and self.sma1[-2]<self.sma2[-2]:
            if self.position.is_short:
                self.position.close()
            self.buy(size=0.95)
         
        elif self.sma1[-1]<self.sma2[-1] and self.sma1[-2]>self.sma2[-2]:
            if self.position.is_long:
                self.position.close()
            self.sell(size=0.95)

# csv_data=csv_data.iloc[:5000]
bt=Backtest(csv_data,sma_strategy,cash=1000_000,commission=0.01,finalize_trades=True)
result=bt.run()
bt.plot()
print(result)

# result['_trades'].to_csv('trades.csv')

