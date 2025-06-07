

# num=1

# while True:
#     if num==101:
#         break
#     print(num)
#     num=num+2

# print('last line')

stock_prices={'tsla':700,'goog':900,'amzn':680,'nvda':567}
portfolio=[]
while True:
    name=input('enter the stock name (q to quit)')
    if name=='q':
        break
    found=stock_prices.get(name)
    if found:
        portfolio.append(name)
    else:
        print('this stock name is invalid type again')
print(portfolio)