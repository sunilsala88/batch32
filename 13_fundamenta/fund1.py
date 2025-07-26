import pandas as pd
from finvizfinance.quote import finvizfinance

stock = finvizfinance('tsla')

d=stock.ticker_fundament()
p=d.get('P/E')
print(p)
# pd.Series(d).to_csv('data.csv')


#news
n=stock.ticker_news()
print(n)
print(stock.ticker_description())


# ticker_list=['TSLA','GOOG','AMZN','NVDA','JPM']
# b_list=[]
# for t in ticker_list:
#     stock = finvizfinance(t)
#     d=stock.ticker_fundament()
#     p=float(d.get('P/E'))
#     b_list.append(p)
# print(b_list)
# i=b_list.index(max(b_list))
# print(ticker_list[i])