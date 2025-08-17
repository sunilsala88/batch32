import pendulum as dt
import pandas as pd
from datetime import datetime,timedelta

import time
import logging
import pandas_ta as ta


from alpaca.trading.requests import GetOrdersRequest,MarketOrderRequest
from alpaca.trading.enums import OrderSide, QueryOrderStatus,TimeInForce
from zoneinfo import ZoneInfo
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.trading.client import TradingClient


api_key='PKCGQ99MC5FQA1P8ZSRE'
secret_key='rkWLI1F2poiTbuERdzozfOLgVV6mrFKTH27Ugvb1'
trading_client = TradingClient(api_key, secret_key, paper=True)
list_of_tickers=["TSLA","AMZN","AAPL",'JPM']
time_zone='America/New_York'
strategy_name='stock_sma'
logging.basicConfig(level=logging.INFO, filename=f'{strategy_name}_{dt.now(tz=time_zone).date()}.log',filemode='a',format="%(asctime)s - %(message)s")
logging.info(f'starting {strategy_name} strategy file')
print(f'starting {strategy_name} strategy file')


def get_historical_stock_data(ticker,duration,time_frame_unit):
    # setup stock historical data client
    stock_historical_data_client = StockHistoricalDataClient(api_key, secret_key)
    current_time=dt.now(tz=time_zone)
   
    req = StockBarsRequest(
        symbol_or_symbols = ticker,
        timeframe=TimeFrame(amount = 1, unit = time_frame_unit), # specify timeframe
        start = current_time-dt.duration(days=duration),                          # specify start datetime, default=the beginning of the current day.
        # end_date=current_time-dt.duration(days=10),                                        # specify end datetime, default=now
        # limit = 2,                                               # specify limit
    )

    history_df1=stock_historical_data_client.get_stock_bars(req).df
    sdata=history_df1.reset_index().drop('symbol',axis=1)
    sdata['timestamp']=sdata['timestamp'].dt.tz_convert('America/New_York')
    sdata=sdata.set_index('timestamp')
    sdata['sma_20']=ta.sma(sdata['close'],length=20)
    sdata['sma_50']=ta.sma(sdata['close'],length=50)
    return sdata


def get_all_position():

    pos=trading_client.get_all_positions()
    new_pos=[]
    for elem in pos:
        new_pos.append(dict(elem))

    pos_df=pd.DataFrame(new_pos)
    # pos_df.to_csv('pos.csv')
    pos_df=pos_df[pos_df['symbol'].isin(list_of_tickers)]
    return pos_df

def get_all_open_orders():
    # params to filter orders by
    request_params = GetOrdersRequest(
                        status=QueryOrderStatus.OPEN
                    )

    # orders that satisfy params
    orders = trading_client.get_orders(filter=request_params)
    new_order=[]
    for elem in orders:
        new_order.append(dict(elem))

    order_df=pd.DataFrame(new_order)
    # order_df.to_csv('orders.csv')
    l=[i for i in list_of_tickers]
    order_df=order_df[order_df['symbol'].isin(l)]
    return order_df


def main_strategy_code():
    #fetch current pos
    pos_df=get_all_position()
    print(pos_df)
    ord_df=get_all_open_orders()
    print(ord_df)


    for ticker in list_of_tickers:
        print(ticker)
        #fetch historical data and indicators
        hist_df=get_historical_stock_data(ticker,5,TimeFrameUnit.Minute)
        print(hist_df)



current_time=dt.now(tz=time_zone)
print(current_time)

start_hour,start_min=7,35
end_hour,end_min=7,38

start_time=dt.datetime(current_time.year,current_time.month,current_time.day,start_hour,start_min,tz=time_zone)
end_time=dt.datetime(current_time.year,current_time.month,current_time.day,end_hour,end_min,tz=time_zone)

print(start_time)
print(end_time)


#this code will execute before the start time
while dt.now(tz=time_zone)<start_time:
    print(dt.now(tz=time_zone))
    time.sleep(1)
print('we have reached start time')


main_strategy_code()

while True:
    if dt.now(tz=time_zone)>end_time:
        break
    ct=dt.now(tz=time_zone)
    print(ct)
    
    if ct.second==1: #and ct.minute in range(0,60,5):#[0,5,10,15..55]
        main_strategy_code()
    time.sleep(1)
print('strategy stopped')