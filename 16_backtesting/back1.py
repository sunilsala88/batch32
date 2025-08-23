
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
    
    def init(self):
        pass

    def next(self):
        pass

bt=Backtest(data,sma_strategy,cash=1000)
result=bt.run()
bt.plot()
print(result)



