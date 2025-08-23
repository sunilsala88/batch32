
#backtrader diff charting is not good
#vectorbt (limitation) (paid library good) (difficult)
#backtesting py 
#good things -easy,good charting ,free,beginner friendly




#fech data

import yfinance as yf
import pandas_ta as ta
from backtesting import Backtest,Strategy
data=yf.download('TSLA',period='5y',multi_level_index=False)
print(data)


def get_sma(close_price,lengtht):
    sma=ta.sma(close_price,lengtht)
    return sma

class sma_strategy(Strategy):
    s1=20
    s2=50
    def init(self):
        self.sma1=self.I(get_sma,self.data.df.Close,self.s1)
        self.sma2=self.I(get_sma,self.data.df.Close,self.s2)

    def next(self):
        if self.sma1[-1]>self.sma2[-1] and self.sma1[-2]<self.sma2[-2]:
            if self.position.is_short:
                self.position.close()
            self.buy()
        elif self.sma1[-1]<self.sma2[-1] and self.sma1[-2]>self.sma2[-2]:
            if self.position.is_long:
                self.position.close()
            self.sell()

bt=Backtest(data,sma_strategy,cash=1000)
result=bt.run()
bt.plot()
print(result)

result['_trades'].to_csv('trades.csv')


