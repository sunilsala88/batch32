
from backtesting import Strategy,Backtest
import pandas_ta as ta
import yfinance as yf
data=yf.download('GOOG',period='1y',interval='1h',multi_level_index=False)
print(data)

def upper(close,l):
    d=ta.bbands(close,l)
    print(d)
    return d[f'BBU_{l}_2.0']

def lower(close,l):
    d=ta.bbands(close,l)
    print(d)
    return d[f'BBL_{l}_2.0']

def middle(close,l):
    d=ta.bbands(close,l)
    print(d)
    return d[f'BBM_{l}_2.0']


class Bollinger(Strategy):
    bl=10
    def init(self):
        self.upper=self.I(upper,self.data.df.Close,self.bl)
        self.lower=self.I(lower,self.data.df.Close,self.bl)
        self.middle=self.I(middle,self.data.df.Close,self.bl)

    def next(self):
        
        if self.lower[-1]>self.data.Close[-1]:
            # if self.position.is_short:
            #     self.position.close()
            self.buy()
        elif self.upper[-1]<self.data.Close[-1]:
            # if self.position.is_long:
            #     self.position.close()
            self.sell()
        
        if self.position.is_long and self.data.Close[-1]>self.middle[-1]:
            self.position.close()
        elif self.position.is_short and self.data.Close[-1]<self.middle[-1]:
            self.position.close()


bt=Backtest(data,Bollinger,cash=1000,commission=0.01)
result=bt.run()
print(result)
bt.plot()