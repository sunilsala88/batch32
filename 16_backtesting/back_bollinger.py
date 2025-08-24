
from backtesting import Strategy,Backtest
import pandas_ta as ta
import yfinance as yf
data=yf.download('GOOG',period='3y',interval='1d',multi_level_index=False)
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
    bl=30
    def init(self):
        self.upper=self.I(upper,self.data.df.Close,self.bl)
        self.lower=self.I(lower,self.data.df.Close,self.bl)
        self.middle=self.I(middle,self.data.df.Close,self.bl)

    def next(self):
        
        # if not self.position:
            if self.lower[-1]>self.data.Close[-1] and not  self.position:
                self.buy()
            elif self.upper[-1]<self.data.Close[-1] and not self.position:
                self.sell()
            
            if self.position.is_long and self.upper[-1]<self.data.Close[-1]:
                 self.position.close()
            elif self.position.is_short and self.lower[-1]>self.data.Close[-1]:
                 self.position.close()        
        # if self.position.is_long and self.data.Close[-1]>self.middle[-1]:
        #     self.position.close()
        # elif self.position.is_short and self.data.Close[-1]<self.middle[-1]:
        #     self.position.close()


bt=Backtest(data,Bollinger,cash=1000000,commission=0.01)
result=bt.run()
print(result)
# bt.plot()

output=bt.optimize(bl=range(10,100,5),maximize='Return [%]')
print(output)
print(output['_strategy'])
bt.plot()