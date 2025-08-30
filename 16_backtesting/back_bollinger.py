from backtesting import Backtest, Strategy
# import indicators as ta
import pandas_ta as ta 

def upper1(close,length):
    return ta.bbands(close,length)[f'BBU_{length}_2.0']

def lower1(close,length):
    return ta.bbands(close,length)[f'BBL_{length}_2.0']


class Bollinger_s(Strategy):
    n1 = 10


    def init(self):
        close = self.data.Close.s
        self.upper = self.I(upper1, close, self.n1)
        self.lower = self.I(lower1, close, self.n1)


    def next(self):
        close_price=self.data.Close[-1]
        current_upper=self.upper[-1]
        current_lower=self.lower[-1]
        if close_price<current_lower:
            self.position.close()
            self.buy()
        elif close_price>current_upper:
            self.position.close()
            self.sell()




import yfinance as yf
data=yf.download('GOOG',period='5y',multi_level_index=False)
print(data)

b1=ta.bbands(data['Close'],10)
print(b1)


bt = Backtest(data, Bollinger_s,
              cash=10000, commission=.002,
              exclusive_orders=True,trade_on_close=True,finalize_trades=True)

output = bt.run()
bt.plot()
print(output)

# # output['_trades'].to_csv('trades.csv')

# #optimize


def custom_optimization(stats):
    return stats['Return [%]']


stats=bt.optimize(n1=range(5,50,2),maximize=custom_optimization)
print(stats)
print(stats['_strategy'])
bt.plot()
stats['_trades'].to_csv('trades.csv')