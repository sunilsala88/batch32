



import pendulum as dt
import logging

list_of_tickers=["TSLA","AMZN"]
time_zone='America/New_York'
strategy_name='stock_sma'
logging.basicConfig(level=logging.INFO, filename=f'{strategy_name}_{dt.now(tz=time_zone).date()}.log',filemode='a',format="%(asctime)s - %(message)s")
logging.info(f'starting {strategy_name} strategy file')
print(f'starting {strategy_name} strategy file')

current_time=dt.now(tz=time_zone)
print(current_time)

