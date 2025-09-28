from alpaca.data.historical.news import NewsClient
from alpaca.data.requests import NewsRequest
from datetime import datetime

api_key='PKCGQ99MC5FQA1P8ZSRE'
secret_key='rkWLI1F2poiTbuERdzozfOLgVV6mrFKTH27Ugvb1'
# no keys required for news data
client = NewsClient(api_key=api_key,secret_key=secret_key)

request_params = NewsRequest(
                        symbols="AAPL",
                        start=datetime.strptime('2016-01-01', '%Y-%m-%d'),
                        end=datetime.strptime('2023-12-01', '%Y-%m-%d'),
                        include_content=True,
                        exclude_contentless = True  
                        )

news = client.get_news(request_params)

# convert to dataframe
data=news.df
data