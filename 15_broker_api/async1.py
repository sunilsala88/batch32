#concorrent programming

# import time

# def fun1():
#     print('start fun1')
#     time.sleep(2)
#     print('end fun1')

# def fun2():
#     print('start fun2')
#     time.sleep(2)
#     print('end fun2')


# fun1()
# fun2()



# import asyncio

# async def fun1():
#     print('start fun1')
#     await asyncio.sleep(2)
#     print('end fun1')

# async def fun2():
#     print('start fun2')
#     await asyncio.sleep(2)
#     print('end fun2')

# async def main():
#     await asyncio.gather(fun1(),fun2())

# asyncio.run(main())


#time.sleep blocking code 
#asyncio.sleep non blocking code


import os
import certifi
#for windows ssl error
os.environ['SSL_CERT_FILE'] = certifi.where()


import asyncio
from alpaca.data.historical.crypto import CryptoHistoricalDataClient
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.live.crypto import CryptoDataStream

api_key='PKCGQ99MC5FQA1P8ZSRE'
secret_key='rkWLI1F2poiTbuERdzozfOLgVV6mrFKTH27Ugvb1'


# Initialize Historical Data Client
crypto_historical_data_client = CryptoHistoricalDataClient()

# Historical Data Retrieval Function
async def get_history():
    while True:
        symbol = "SOL/USD"
        now = datetime.now(ZoneInfo("America/New_York"))
        req = CryptoBarsRequest(
            symbol_or_symbols=[symbol],
            timeframe=TimeFrame(amount=1, unit=TimeFrameUnit.Minute),
            start=now - timedelta(days=1),
        )
        history_df2 = crypto_historical_data_client.get_crypto_bars(req).df
        print("Historical Data:")
        print(history_df2)
        await asyncio.sleep(30)  # Wait for 10 seconds before fetching again

# Initialize Data Stream Client
crypto_data_stream_client = CryptoDataStream(api_key, secret_key)

# Live Data Stream Handler
async def crypto_data_stream_handler(data):
    print(data)

# Function to Start the Live Stream
async def start_crypto_stream():
    symbol = ['SOL/USD']
    crypto_data_stream_client.subscribe_quotes(crypto_data_stream_handler, *symbol)
    print("Starting Live Data Stream...")
    
    await crypto_data_stream_client._run_forever()  # Await the internal run method

# Main Function to Run Both Tasks Concurrently
async def main():
    # Run both tasks concurrently
    await asyncio.gather(
        get_history(),            # Historical data retrieval every 10 seconds
        start_crypto_stream()     # Live data stream
    )

asyncio.run(main())