#strategy description:
#1. wait till 10:15 and calculate high and low from 9:15 to 10:15
#2. sell atm call and put option at 10:15 (ATM based on spot price at 10:15, not daily open)
#3. if spot price goes above high, buy atm call option (closing loss making call position )
#4. if spot price goes below low, buy atm put option (closing loss making put position )
#5. after closing call position if spot price comes below high, sell atm call option again
#6. after closing  put position if spot price comes above low, sell atm put option again
#7. if the spot price is between high and low, do nothing
#8. checking for condition every 5 minutes
#9. closing all positions at 15:25

# IMPROVEMENTS MADE:
# - ATM strike now calculated based on actual spot price at 10:15 instead of daily open
# - Added helper functions for better code organization and error handling
# - Improved logging with more descriptive messages
# - Better error handling with proper validation
# - Cleaner code structure with consistent formatting
# - Portfolio structure enhanced to store contract details and strike prices
# - Removed unnecessary type conversions and improved data handling


#https://drive.google.com/file/d/1n7TCW01s7QvuS3p47-N3TbHVpczutQkq/view


from datetime import datetime, timedelta  # Importing necessary modules
from calendar import monthrange, weekday, WEDNESDAY, THURSDAY
import pandas as pd
import time as t
import sqlite3
import logging
pd.options.mode.chained_assignment = None  # default='warn'

logging.basicConfig(filename='option_backtesting.log', filemode='w', level=logging.INFO, format=' %(message)s')  # Configuring logging
logging.info('this is my first line')  # Logging the first line

data_address='/Users/new algo trading/batch32/18_option backtesting/option_history.db'

holidays = ['2021-01-26', '2021-03-11', '2021-03-29', '2021-04-02', '2021-04-14', '2021-04-21', '2021-05-13', '2021-07-21', '2021-08-19', '2021-09-10', '2021-10-15', '2021-11-04', '2021-11-05', '2021-11-19', '2022-01-26', '2022-03-01', '2022-03-18', '2022-04-14', '2022-04-15', '2022-05-03', '2022-08-09', '2022-08-15', '2022-08-31', '2022-10-05', '2022-10-24', '2022-10-26', '2022-11-08', '2023-01-26', '2023-03-07', '2023-03-30', '2023-04-04', '2023-04-07', '2023-04-14', '2023-04-21', '2023-05-01', '2023-06-28', '2023-08-15', '2023-09-19', '2023-10-02', '2023-10-24', '2023-11-14', '2023-11-27', '2023-12-25']
holidays = [datetime.strptime(x, '%Y-%m-%d') for x in holidays]  # Converting holiday strings to datetime objects
print(holidays)

def get_weekly_expiry(year, month):  # Function to get all Thursdays of the month
    d = monthrange(year, month)[1]
    thursdays = [datetime(year, month, day) for day in range(1, d + 1) if datetime(year, month, day).weekday() == 3]

    for hol in holidays:
        if hol in thursdays:
            thursdays[thursdays.index(hol)] = hol - timedelta(days=1)  # Update Thursday to Wednesday if it's a holiday
    return thursdays

l=get_weekly_expiry(2023,1)
print(l)


def get_nearest_expiry(current_day=datetime.now()):
    # Get the current year and month based on the input 'current_day'
    year = current_day.year
    month = current_day.month

    # Calculate the last day of the current month
    last_day_of_month = monthrange(year, month)[1]

    # Find all Thursdays of the month
    thursdays = [datetime(year, month, day) for day in range(1, last_day_of_month + 1) if weekday(year, month, day) == THURSDAY]

    # Adjust Thursdays for holidays
    for hol in holidays:
        if hol in thursdays:
            # If a holiday falls on a Thursday, move it to the previous day (Wednesday)
            thursdays[thursdays.index(hol)] = hol - timedelta(days=1)

    # Find the current expiry date
    current_expiry = None
    for curr_thursday in thursdays:
        if current_day <= curr_thursday:
            current_expiry = curr_thursday
            break

    # Handle the case when today is after the last Thursday of the month
    if current_day > thursdays[-1]:
        if month == 12:
            # Move to the next year and set month to January
            year += 1
            month = 1
        else:
            month += 1

        # Calculate the Thursdays for the next month
        d = monthrange(year, month)[1]
        thursdays = [datetime(year, month, day) for day in range(1, d + 1) if weekday(year, month, day) == THURSDAY]

        # Adjust for holidays in the next month
        for hol in holidays:
            if hol in thursdays:
                # If a holiday falls on a Thursday, move it to the previous day (Wednesday)
                thursdays[thursdays.index(hol)] = hol - timedelta(days=1)

        current_expiry = thursdays[0]
        return current_expiry

    return current_expiry


a=get_nearest_expiry(datetime(2023,9,28))
print(a)


def get_option_price(option_price_df, contract_name, datetime_str):
    """
    Helper function to safely get option price from dataframe
    
    Args:
        option_price_df: Dictionary containing option price dataframes
        contract_name: Name of the option contract
        datetime_str: Datetime string to filter data
    
    Returns:
        float: Option price or None if not found
    """
    try:
        if contract_name not in option_price_df:
            return None
            
        data = option_price_df[contract_name][option_price_df[contract_name]['datetime'] == datetime_str]
        
        if data.empty:
            return None
            
        return float(data.open.values[0])
    except Exception as e:
        logging.error(f'Error getting option price for {contract_name}: {str(e)}')
        return None


def calculate_atm_strike(spot_price, strike_interval=100):
    """
    Calculate ATM strike price based on spot price
    
    Args:
        spot_price: Current spot price
        strike_interval: Strike price interval (default 100)
    
    Returns:
        int: ATM strike price
    """
    return int(spot_price // strike_interval) * strike_interval


def get_from_database():
    con = sqlite3.connect(data_address)
    cursorObj = con.cursor()
    cursorObj.execute('SELECT name from sqlite_master where type= "table"')
    data= cursorObj.fetchall()
    option_price_df={}
    temp=0
    for i in data:
        # temp=temp+1
        # if temp==5:
        #     break
        k=i[0]
        option_price_df[k]=pd.read_sql_query(f'SELECT * FROM {k}',con)
        # print(option_price_df)
    return option_price_df




year=2023
month=1
money=2000
trades=open('trades.csv','w')
trades.write('time'+","+'option_contract_name' +","+'position'+','+'option_price'+','+'underlying_price'+','+'balance'+'\n')


# start1 = datetime(year, month, 1)
option_price_df1=get_from_database()
option_price_df={}
# print(option_price_df1)
# #resample 1min to 5min and store in option_price_df

for i,j in option_price_df1.items():
    if j.empty == False:
        j=j[['datetime','open','high','low','close','volume']]
        j['datetime']=pd.to_datetime(j['datetime'])
        j.set_index('datetime',inplace=True)
        ohlcv_dict = {
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }
        option_price_df[i]=j.resample('5min').agg(ohlcv_dict)
        #drop nan rows
        option_price_df[i].dropna(inplace=True)
        #remove date before 9:15 and after 15:30
        option_price_df[i]=option_price_df[i].between_time('09:15','15:30')
        option_price_df[i].reset_index(inplace=True)

print(option_price_df)



for month in range(1,7):
    end=get_weekly_expiry(year,month)[-1]
    start=datetime(year,month,1)
    underlying_df_daily=option_price_df['daily'+end.strftime('%Y%m%d')]
    underlying_df_5min=option_price_df['min'+end.strftime('%Y%m%d')]

    for i in underlying_df_daily.index:
        open_price=(int(float(underlying_df_daily['open'][i]))//100)*100
        time=underlying_df_daily['datetime'][i]
        if time>datetime(2023,6,20):
            break
        start=datetime(time.year,time.month,time.day,9,15)
        end2=datetime(time.year,time.month,time.day,15,25)
        portfolio={}
        first_trade=False

        # Pre-calculate expiry date for efficiency
        expiry_date = get_nearest_expiry(time).strftime('%Y%m%d')
        
        while start <= end2:
            try:
                # Get current spot price
                current_time_str = start.strftime('%Y-%m-%d %H:%M:%S')
                spot_data = underlying_df_5min[underlying_df_5min['datetime'] == current_time_str]
                
                if spot_data.empty:
                    logging.warning(f'No spot data found for {current_time_str}')
                    start = start + timedelta(minutes=5)
                    continue
                    
                spot_price = float(spot_data.open.values[0])

                # Entry condition - Take ATM contracts at 10:15 based on current spot price
                if (not first_trade) and (start.time() == datetime(time.year, time.month, time.day, 10, 15).time()):
                    logging.info(f'Taking positions at 10:15, spot price: {spot_price}')
                    first_trade = True
                    
                    # Calculate ATM strike based on spot price at 10:15
                    atm_strike = calculate_atm_strike(spot_price)
                    
                    # Calculate high and low from 9:15 to 10:15
                    range_start = datetime(time.year, time.month, time.day, 9, 15).strftime('%Y-%m-%d %H:%M:%S')
                    range_end = datetime(time.year, time.month, time.day, 10, 15).strftime('%Y-%m-%d %H:%M:%S')
                    
                    range_data = underlying_df_5min[
                        (underlying_df_5min.datetime >= range_start) & 
                        (underlying_df_5min.datetime < range_end)
                    ]
                    
                    if range_data.empty:
                        logging.error(f'No data found for range {range_start} to {range_end}')
                        start = start + timedelta(minutes=5)
                        continue
                        
                    high = float(range_data.high.astype(float).max())
                    low = float(range_data.low.astype(float).min())
                    
                    logging.info(f'Calculated range: High={high}, Low={low}, ATM Strike={atm_strike}')
                    
                    # Create option contract names
                    atm_call_contract = f'call{atm_strike}{expiry_date}'
                    atm_put_contract = f'put{atm_strike}{expiry_date}'
                    
                    # Get option prices using helper function
                    atm_call_price = get_option_price(option_price_df, atm_call_contract, current_time_str)
                    atm_put_price = get_option_price(option_price_df, atm_put_contract, current_time_str)
                    
                    if atm_call_price is None or atm_put_price is None:
                        logging.error(f'Could not get option prices for {atm_call_contract} or {atm_put_contract} at {current_time_str}')
                        start = start + timedelta(minutes=5)
                        continue
                    
                    # Sell ATM call and put options
                    money = money + atm_call_price + atm_put_price
                    portfolio['atm_call'] = {'price': atm_call_price, 'contract': atm_call_contract, 'strike': atm_strike}
                    portfolio['atm_put'] = {'price': atm_put_price, 'contract': atm_put_contract, 'strike': atm_strike}
                    
                    logging.info(f'Sold ATM options - Call: {atm_call_price}, Put: {atm_put_price}, Balance: {money}')
                    
                    # Record trades
                    trades.write(f'{current_time_str}, {atm_call_contract}, sell, {atm_call_price}, {spot_price}, {money - atm_put_price}\n')
                    trades.write(f'{current_time_str}, {atm_put_contract}, sell, {atm_put_price}, {spot_price}, {money}\n')

                # Exit condition - Close all positions at 15:25
                elif start == datetime(time.year, time.month, time.day, 15, 25):
                    logging.info('Closing positions at 15:25')
                    
                    if 'atm_call' in portfolio:
                        call_contract = portfolio['atm_call']['contract']
                        atm_call_price = get_option_price(option_price_df, call_contract, current_time_str)
                        
                        if atm_call_price is not None:
                            money = money - atm_call_price
                            logging.info(f'Bought back ATM call option: {atm_call_price}, Balance: {money}')
                            trades.write(f'{current_time_str}, {call_contract}, buy, {atm_call_price}, {spot_price}, {money}\n')
                            del portfolio['atm_call']
                        else:
                            logging.warning(f'Could not get call price for exit at {current_time_str}')

                    if 'atm_put' in portfolio:
                        put_contract = portfolio['atm_put']['contract']
                        atm_put_price = get_option_price(option_price_df, put_contract, current_time_str)
                        
                        if atm_put_price is not None:
                            money = money - atm_put_price
                            logging.info(f'Bought back ATM put option: {atm_put_price}, Balance: {money}')
                            trades.write(f'{current_time_str}, {put_contract}, buy, {atm_put_price}, {spot_price}, {money}\n')
                            del portfolio['atm_put']
                        else:
                            logging.warning(f'Could not get put price for exit at {current_time_str}')

                # Strategy condition between entry and exit
                elif first_trade:
                    # Check if we have call position
                    if 'atm_call' in portfolio:
                        if spot_price > high:
                            # Close call position when price breaks above high
                            call_contract = portfolio['atm_call']['contract']
                            atm_call_price = get_option_price(option_price_df, call_contract, current_time_str)
                            
                            if atm_call_price is not None:
                                money = money - atm_call_price
                                logging.info(f'Closing call position above high: {atm_call_price}, Balance: {money}')
                                trades.write(f'{current_time_str}, {call_contract}, buy, {atm_call_price}, {spot_price}, {money}\n')
                                del portfolio['atm_call']
                    else:
                        # Re-enter call position when price comes back below high
                        if spot_price < high:
                            atm_strike = portfolio.get('atm_put', {}).get('strike', calculate_atm_strike(spot_price))
                            call_contract = f'call{atm_strike}{expiry_date}'
                            atm_call_price = get_option_price(option_price_df, call_contract, current_time_str)
                            
                            if atm_call_price is not None:
                                money = money + atm_call_price
                                portfolio['atm_call'] = {'price': atm_call_price, 'contract': call_contract, 'strike': atm_strike}
                                logging.info(f'Re-entering call position below high: {atm_call_price}, Balance: {money}')
                                trades.write(f'{current_time_str}, {call_contract}, sell, {atm_call_price}, {spot_price}, {money}\n')

                    # Check if we have put position
                    if 'atm_put' in portfolio:
                        if spot_price < low:
                            # Close put position when price breaks below low
                            put_contract = portfolio['atm_put']['contract']
                            atm_put_price = get_option_price(option_price_df, put_contract, current_time_str)
                            
                            if atm_put_price is not None:
                                money = money - atm_put_price
                                logging.info(f'Closing put position below low: {atm_put_price}, Balance: {money}')
                                trades.write(f'{current_time_str}, {put_contract}, buy, {atm_put_price}, {spot_price}, {money}\n')
                                del portfolio['atm_put']
                    else:
                        # Re-enter put position when price comes back above low
                        if spot_price > low:
                            atm_strike = portfolio.get('atm_call', {}).get('strike', calculate_atm_strike(spot_price))
                            put_contract = f'put{atm_strike}{expiry_date}'
                            atm_put_price = get_option_price(option_price_df, put_contract, current_time_str)
                            
                            if atm_put_price is not None:
                                money = money + atm_put_price
                                portfolio['atm_put'] = {'price': atm_put_price, 'contract': put_contract, 'strike': atm_strike}
                                logging.info(f'Re-entering put position above low: {atm_put_price}, Balance: {money}')
                                trades.write(f'{current_time_str}, {put_contract}, sell, {atm_put_price}, {spot_price}, {money}\n')



                start = start + timedelta(minutes=5)
            
            except Exception as e:
                logging.error(f'Error processing time {start}: {str(e)}')
                start = start + timedelta(days=1)
                continue


print(money)
logging.info('money : '+str(money))
trades.close()