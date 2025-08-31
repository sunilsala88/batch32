
from backtesting import Strategy, Backtest
import yfinance as yf
import pandas_ta as ta
from backtesting.lib import resample_apply
import time

def supertrend1(high_data,low_data,close_data,l):
    o=ta.supertrend(high_data,low_data,close_data,length=l)
    # print(o)
    return o[f'SUPERTd_{l}_3.0']
def supertrend2(high_data,low_data,close_data,l):
    o=ta.supertrend(high_data,low_data,close_data,length=l)
    return o[f'SUPERT_{l}_3.0']

def ema(close_data,period=9):
    return ta.ema(close_data,length=period)


class supertrend_ema(Strategy):
    super_length=30
    ema_length=10


    def init(self):
        self.super1=self.I(supertrend1,self.data.High.s,self.data.Low.s,self.data.Close.s,self.super_length)
        self.super2=self.I(supertrend2,self.data.High.s,self.data.Low.s,self.data.Close.s,self.super_length)
        
        # self.ema_hour=self.I(ema,self.data.Close.s,self.n1)

        self.daily_ema = resample_apply('D', ema,self.data.Close.s,self.ema_length)

    def next(self):

      
        if self.super1[-1]>0 and self.data.Close[-1]> self.daily_ema[-1] :
            if self.position.is_short:
                self.position.close()
            if not self.position:
                self.buy(size=0.95)  # Using 95% of available cash

        elif self.super1[-1]<0 and self.data.Close[-1]<self.daily_ema[-1]:
            if self.position.is_long:
                self.position.close()
            if not self.position:
                self.sell(size=0.95)  # Using 95% of available cash




import yfinance as yf
data=yf.download('^NSEI',period='700d',interval='1h')
data.index = data.index.tz_convert('Asia/Kolkata')
#change timezone from utc to ist



data.columns=[c[0] for c in data.columns]
print(data)

s1=supertrend1(data.High,data.Low,data.Close,10)
s2=supertrend2(data.High,data.Low,data.Close,10)
e1=ema(data.Close,10)
print(s1)
print(s2)
print(e1)

bt=Backtest(data,supertrend_ema,cash=100000,trade_on_close=True,finalize_trades=True)
output=bt.run()
print(output)
print(output['_trades'].to_csv('trades.csv'))
# bt.plot()

def custom_optimization(stats):
    return  stats['Return [%]'] *stats['Win Rate [%]'] 


stats = bt.optimize(
    super_length=range(5,60,6),
    ema_length=range(5,60,6),
    maximize=custom_optimization,
    max_tries=100,  # Limit the number of optimization attempts
    random_state=42  # Set random seed for reproducibility
)
print(stats)
print(stats['_strategy'])
bt.plot()


#26,41