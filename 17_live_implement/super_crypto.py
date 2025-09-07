
# Supertrend and EMA Strategy
# Calculate the Supertrend on daily candles.
# Calculate the EMA (Exponential Moving Average) on hourly candles.
# Go Long:When the daily Supertrend gives a long signal and the closing price is greater than the daily EMA.
# Go Short:When the daily Supertrend gives a short signal.The closing price is less than the daily EMA.


import pendulum as dt
import pandas as pd
import numpy as np
import time
import logging


from datetime import datetime,timedelta
from zoneinfo import ZoneInfo

from alpaca.data.timeframe import TimeFrame, TimeFrameUnit

from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.requests import StopOrderRequest,StopLimitOrderRequest

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import OrderSide, QueryOrderStatus,TimeInForce

from alpaca.data.historical import CryptoHistoricalDataClient
crypto_historical_data_client = CryptoHistoricalDataClient()
from zoneinfo import ZoneInfo
from alpaca.data.requests import CryptoBarsRequest

api_key='PKCGQ99MC5FQA1P8ZSRE'
secret_key='rkWLI1F2poiTbuERdzozfOLgVV6mrFKTH27Ugvb1'
list_of_tickers=["AAVE/USD","ETH/USD",'SOL/USD']


#timframe is 1 min
time_frame=1
time_frame_unit=TimeFrameUnit.Minute
days=20
start_hour,start_min=13,31
end_hour,end_min=15,35
time_zone='America/New_York'
strategy_name='crypto_supertrend_ema_strategy'
stop_perc=2


#logging to file
logging.basicConfig(level=logging.INFO, filename=f'{strategy_name}_{dt.now(time_zone).date()}.log',filemode='a',format="%(asctime)s - %(message)s")


trading_client = TradingClient(api_key, secret_key, paper=True)

try:
    trades_info=pd.read_csv('trades.csv')  

except:
    trades_info=pd.DataFrame(columns=['Date','symbol','side','quantity','sl','tp'])

trades_info.set_index('Date',inplace=True)


def save_trade_info(symbol, side, quantity, sl=None, tp=None):
    """Save trade information to trades.csv file"""
    global trades_info
    current_time = dt.now(time_zone).strftime('%Y-%m-%d %H:%M:%S')
    
    new_trade = {
        'Date': current_time,
        'symbol': symbol,
        'side': side,
        'quantity': quantity,
        'sl': sl,
        'tp': tp
    }
    
    # Add new trade to the DataFrame
    new_trade_df = pd.DataFrame([new_trade])
    new_trade_df.set_index('Date', inplace=True)
    trades_info = pd.concat([trades_info, new_trade_df])
    
    # Save to CSV
    trades_info.to_csv('trades.csv')
    logging.info(f'Trade saved: {symbol} {side} {quantity} at {current_time}')
    print(f'Trade information saved to trades.csv')


def calculate_ema(data, length):
    """Calculate Exponential Moving Average"""
    return data.ewm(span=length, adjust=False).mean()


def calculate_atr(high, low, close, length=14):
    """Calculate Average True Range"""
    # True Range calculation
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    
    # True Range is the maximum of the three
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    # ATR is the EMA of True Range
    atr = calculate_ema(true_range, length)
    
    return atr


def calculate_supertrend(high, low, close, length=10, multiplier=3.0):
    """Calculate Supertrend indicator"""
    # Calculate ATR
    atr = calculate_atr(high, low, close, length)
    
    # Calculate basic upper and lower bands
    hl2 = (high + low) / 2
    upper_band = hl2 + (multiplier * atr)
    lower_band = hl2 - (multiplier * atr)
    
    # Initialize final upper and lower bands
    final_upper_band = pd.Series(index=close.index, dtype=float)
    final_lower_band = pd.Series(index=close.index, dtype=float)
    supertrend = pd.Series(index=close.index, dtype=float)
    direction = pd.Series(index=close.index, dtype=int)
    
    for i in range(len(close)):
        if i == 0:
            final_upper_band.iloc[i] = upper_band.iloc[i]
            final_lower_band.iloc[i] = lower_band.iloc[i]
            supertrend.iloc[i] = upper_band.iloc[i]
            direction.iloc[i] = -1
        else:
            # Calculate final upper band
            if upper_band.iloc[i] < final_upper_band.iloc[i-1] or close.iloc[i-1] > final_upper_band.iloc[i-1]:
                final_upper_band.iloc[i] = upper_band.iloc[i]
            else:
                final_upper_band.iloc[i] = final_upper_band.iloc[i-1]
            
            # Calculate final lower band
            if lower_band.iloc[i] > final_lower_band.iloc[i-1] or close.iloc[i-1] < final_lower_band.iloc[i-1]:
                final_lower_band.iloc[i] = lower_band.iloc[i]
            else:
                final_lower_band.iloc[i] = final_lower_band.iloc[i-1]
            
            # Calculate supertrend direction
            if close.iloc[i] <= final_lower_band.iloc[i]:
                direction.iloc[i] = -1
            elif close.iloc[i] >= final_upper_band.iloc[i]:
                direction.iloc[i] = 1
            else:
                direction.iloc[i] = direction.iloc[i-1]
            
            # Calculate supertrend value
            if direction.iloc[i] == 1:
                supertrend.iloc[i] = final_lower_band.iloc[i]
            else:
                supertrend.iloc[i] = final_upper_band.iloc[i]
    
    # Convert direction to signal (1 for bullish, -1 for bearish)
    signal = direction * -1  # Flip the direction for traditional supertrend signal
    
    return signal




def get_historical_crypto_data(ticker,duration,time_frame_unit):
    """extracts historical data and outputs in the form of dataframe"""
    now = datetime.now(ZoneInfo("America/New_York"))
    req = CryptoBarsRequest(
        symbol_or_symbols = ticker,
        timeframe=TimeFrame(amount = 1, unit = time_frame_unit), # specify timeframe
        start = now - timedelta(days = duration),                          # specify start datetime, default=the beginning of the current day.
        # end_date=None,                                        # specify end datetime, default=now
        # limit = 2,                                               # specify limit
    )
    history_df1=crypto_historical_data_client.get_crypto_bars(req).df
    sdata=history_df1.reset_index().drop('symbol',axis=1)
    sdata['timestamp']=sdata['timestamp'].dt.tz_convert('America/New_York')
    sdata=sdata.set_index('timestamp')
    
    # Use our custom indicator functions
    sdata['ema'] = calculate_ema(sdata['close'], length=10)
    sdata['super'] = calculate_supertrend(sdata['high'], sdata['low'], sdata['close'], length=10)
    sdata['atr'] = calculate_atr(sdata['high'], sdata['low'], sdata['close'], length=14)

    return sdata

df=get_historical_crypto_data('BTC/USD',30,TimeFrameUnit.Hour)
print(df)

def get_open_position():

    pos=trading_client.get_all_positions()
    new_pos=[]
    for elem in pos:
        new_pos.append(dict(elem))

    pos_df=pd.DataFrame(new_pos)
    print("All positions:")
    print(pos_df)
    
    if not pos_df.empty:
        #filter pos that are in list_of_tickers
        l=[i.replace("/","") for i in list_of_tickers]
        print(f"Looking for positions in: {l}")
        pos_df=pos_df[pos_df['symbol'].isin(l)]
        print("Filtered positions:")
        print(pos_df)
    
    return pos_df

def get_open_orders():
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
    #filter orders that are in list_of_tickers
    if not order_df.empty:
        order_df=order_df[order_df['symbol'].isin(list_of_tickers)]
    return order_df




def close_this_crypto_position(ticker_name):
    # Convert ticker format if needed (remove "/" for position symbol)
    position_symbol = ticker_name.replace('/', '') if '/' in ticker_name else ticker_name
    
    # First close all open orders for this instrument
    close_this_order_for_crypto(ticker_name)
    
    try:
        position = trading_client.get_open_position(position_symbol)
        print(f"Position found: {position}")
        logging.info(f'Closing position for {position_symbol}')
        
        # Get position details before closing
        quantity = abs(float(position.qty))
        # Get the original position side for logging purposes
        original_position_side = str(position.side).upper()  # 'LONG' or 'SHORT'
        
        # The closing order side (opposite of position side)
        closing_order_side = 'SELL' if str(position.side).lower() == 'long' else 'BUY'
        
        print(f"Closing {original_position_side} position of {quantity} {position_symbol} with {closing_order_side} order")
        
        c=trading_client.close_position(position_symbol)
        print(f"Position close response: {c}")
        print('position closed')
        
        # Save trade information for position close - record as "CLOSE_LONG" or "CLOSE_SHORT"
        trade_side = f"CLOSE_{original_position_side}"
        save_trade_info(ticker_name, trade_side, quantity)
        
    except Exception as e:
        print(f'position does not exist for {ticker_name}: {e}')
        logging.info(f'Could not close position for {ticker_name}: {e}')

def close_this_order_for_crypto(ticker_name):
    # Handle both formats: "ETH/USD" and "ETHUSD" 
    # Orders are stored in the format without "/" so convert if needed
    order_symbol = ticker_name.replace('/', '') if '/' in ticker_name else ticker_name
    
    order_df=get_open_orders()
    if not order_df.empty:
        # Check for orders with both the original ticker format and without "/"
        matching_orders = order_df[
            (order_df['symbol'] == ticker_name) | 
            (order_df['symbol'] == order_symbol)
        ]
        print(f"Found orders for {ticker_name}:")
        print(matching_orders)
        
        if not matching_orders.empty:
            for id in matching_orders['id'].to_list():
                try:
                    logging.info(f'Closing order for {ticker_name}')
                    response = trading_client.cancel_order_by_id(id)
                    print(response)
                    print(f'Order {id} cancelled for {ticker_name}')
                except Exception as e:
                    print(f'order does not exist {ticker_name}: {e}')
                    logging.info(f'Could not cancel order {id} for {ticker_name}: {e}')
        else:
            print(f'No orders found for {ticker_name}')
    else:
        print('No open orders found')
                

def check_market_order_placed(ticker):
    order_df=get_open_orders()
    if not order_df.empty:
        order_df=order_df[order_df['order_type']=='market']
        if not order_df.empty and (ticker in order_df['symbol'].to_list()):
            return 0
        else:
            return 1
    else:
        return 1



def trade_sell_stocks(symbol,stock_price,stop_price,quantity=1):
    logging.info(f'Selling {quantity} of {symbol} at {stock_price}')
    if check_market_order_placed(symbol):

        market_order_data = MarketOrderRequest(
                            symbol=symbol,
                            qty=quantity,
                            side=OrderSide.SELL,
                            time_in_force=TimeInForce.GTC
                            )

        # Market order
        market_order = trading_client.submit_order(
                        order_data=market_order_data
                    )
        print(market_order)
        
        # Save trade information
        save_trade_info(symbol, 'SELL', quantity, sl=stop_price)




def trade_buy_stocks(symbol,stock_price,stop_price,quantity=1):
    logging.info(f'Buying {quantity} of {symbol} at {stock_price}')

    if check_market_order_placed(symbol):

        market_order_data = MarketOrderRequest(
                            symbol=symbol,
                            qty=quantity,
                            side=OrderSide.BUY,
                            time_in_force=TimeInForce.GTC
                            )

        # Market order
        market_order = trading_client.submit_order(
                        order_data=market_order_data
                    )
        print(market_order)
        
        # Save trade information
        save_trade_info(symbol, 'BUY', quantity, sl=stop_price)


def place_stop_order_stock(symbol,stop_price,quantity,side):
    logging.info(f'Placing stop order for {quantity} of {symbol} at {stop_price}')
    print('placing stop order')
    req = StopLimitOrderRequest(
                    symbol = symbol,
                    qty = quantity,
                    side = side,
                    time_in_force = TimeInForce.GTC,
                    limit_price = round(stop_price,2),
                    stop_price = round(stop_price,2)
                    )

    res = trading_client.submit_order(req)
    res


    # stop_order_data=StopOrderRequest(
    #                     symbol=symbol,
    #                     stop_price=int(stop_price),
    #                     qty=quantity,
    #                     side=side,
    #                     time_in_force=TimeInForce.GTC
    # )

    # stop_market_order = trading_client.submit_order(
    #                 order_data=stop_order_data
    #             )
    print(res)


def check_and_place_stop_order(pos_df,order_df):

        if not pos_df.empty:
            print('inside check and place stop order')
            l1=pos_df['symbol'].to_list()
            print(l1)
            print(list_of_tickers)
            #common stock in l1 and list_of_tickers
            l1=list(set(l1).intersection(set([l.replace('/','') for l in list_of_tickers])))
            
            print(l1)
            for ticker in list_of_tickers:
                #check if stop order exist
                try:
                        t=trading_client.get_open_position(ticker.replace('/',''))  
                        buy_price=float(t.avg_entry_price)
                        quantity=abs(round(float(t.qty),2))
                        s=t.side
                        if s==OrderSide.BUY:
                            s=OrderSide.SELL
                            stop_price=buy_price-buy_price*(1-(stop_perc/100))
                        else:
                            s=OrderSide.BUY
                            stop_price=buy_price+buy_price*(1-(stop_perc/100))
                        if order_df.empty or (ticker not in order_df['symbol'].to_list()):
                            place_stop_order_stock(ticker,stop_price,quantity,s)
                        print('stop order already placed')
                except Exception as e:
                    print(e)
                    print('stop order cannot be placed')
                    logging.info(f'Stop order cannot be placed for {ticker}')


def strategy_condition(hist_df_hourly,hist_df_daily,ticker):
    print('inside strategy conditional code ')
    # print(hist_df)
    print(ticker)
    buy_condition=hist_df_hourly['super'].iloc[-1]>0 and hist_df_daily['ema'].iloc[-1]<hist_df_hourly['close'].iloc[-1]
    buy_condition=True
    # sell_condition=hist_df_hourly['super'].iloc[-1]<0 and hist_df_daily['ema'].iloc[-1]>hist_df_hourly['close'].iloc[-1]
    # sell_condition=True


    hourly_closing_price=hist_df_hourly['close'].iloc[-1]
    atr_value=hist_df_daily['atr'].iloc[-1]

    if buy_condition:
        print('buy condition satisfied')
        trade_buy_stocks(ticker,hourly_closing_price,hourly_closing_price-atr_value)
    # elif sell_condition:
    #     print('sell condition satisfied')
    #     trade_sell_stocks(ticker,hourly_closing_price,hourly_closing_price+atr_value)
    else:
        print('no condition satisfied')

def main_strategy():
    pos_df= get_open_position()
    ord_df= get_open_orders()
    print(pos_df)
    print(ord_df)
    ord_df.to_csv('orders.csv')

    for ticker in list_of_tickers:
        print(ticker)
        #historical data with indicator data
        hist_df=get_historical_crypto_data(ticker,days,time_frame_unit)
        print(hist_df)
        hist_df_hourly=get_historical_crypto_data(ticker,10,TimeFrameUnit.Hour)
        hist_df_daily=get_historical_crypto_data(ticker,50,TimeFrameUnit.Day)
        print(hist_df_hourly)
        print(hist_df_daily)

        #get current money
        money=float(trading_client.get_account().cash)
        print(money)
        # money=500
        closing_price=hist_df['close'].iloc[-1]
        print(closing_price)
        quantity=money/closing_price
        print(quantity)


        if quantity<1:
            continue
        


        elif (pos_df.empty )  or (len(pos_df)!=0 and ticker.replace('/','') not in pos_df['symbol'].to_list()):
            print('we have some position but ticker is not in pos')
            strategy_condition(hist_df_hourly,hist_df_daily,ticker)

        elif len(pos_df)!=0 and ticker.replace('/','')  in pos_df['symbol'].to_list():
            print('we have some pos and ticker is in pos')
            curr_quant=float(pos_df[pos_df['symbol']==ticker.replace('/','')]['qty'].iloc[-1])
            print(curr_quant)
            if curr_quant==0:
                print('my quantity is 0')
                strategy_condition(hist_df_hourly,hist_df_daily,ticker)
            elif curr_quant>0:
                print('we are already long')
                sell_condition=hist_df_hourly['super'].iloc[-1]<0 and hist_df_daily['ema'].iloc[-1]>hist_df_hourly['close'].iloc[-1]
                sell_condition=True
                if sell_condition:
                    print('sell condition is satisfied ')
                    logging.info(f'Sell condition satisfied for {ticker}')
                    close_this_crypto_position(ticker)
                else:
                    print('sell condition not satisfied')
        
    time.sleep(1)
    check_and_place_stop_order(pos_df,ord_df)

main_strategy()

current_time=dt.now(time_zone)
print(current_time)
start_time=dt.datetime(current_time.year,current_time.month,current_time.day,start_hour,start_min,tz=time_zone)
end_time=dt.datetime(current_time.year,current_time.month,current_time.day,end_hour,end_min,tz=time_zone)
print('start time:', start_time)
print('end time:', end_time)


#pre hour and post hour

while dt.now(time_zone)<start_time :
    print(dt.now(time_zone))
    time.sleep(1)

print('we have reached start time ')
print('we are running our strategy now')
main_strategy()

while True:
    if dt.now(time_zone)>end_time:
        break
    ct=dt.now(time_zone)
    print(ct)
    if ct.second in range(2,3) and ct.minute in range(0,60,time_frame):
        # ct.second in range(2,4) and ct.minute==1
        main_strategy()
    time.sleep(1)




print('we have reached end time')


#close all orders
for ticker in list_of_tickers:
    close_this_order_for_crypto(ticker)
    print('order closed')



pos_df= get_open_position()
l1=pos_df['symbol'].to_list()
l1=list(set(l1).intersection(set([l.replace('/','') for l in list_of_tickers])))
#close all positions
for ticker in l1:
    close_this_crypto_position(ticker)
    print('position closed')


print('strategy stopped')