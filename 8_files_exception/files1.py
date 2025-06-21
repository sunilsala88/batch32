
#we always store string in text file

# a='tsla'

# f1=open('demo1.txt','w')
# f1.write(a)
# f1.close()

# address=r'/Users/new algo trading/batch32/8_files_exception/demo1.txt'

# f2=open('8_files_exception/demo1.txt','r')
# d=f2.read()
# print(d)
# f2.close()

# f1=open('demo1.txt','a')
# f1.write('\nongc')
# f1.close()


def get_stocks(stock_prices):
    portfolio={}
    while True:
        name=input('enter the stock name (q to quit)')
        if name.upper()=='Q':
            break
        found=stock_prices.get(name)
        if found:
            portfolio.update({name:found})
        else:
            print('this stock does not exist try again')
    return portfolio

def save_data(portfolio):
    f1=open('data.txt','a')
    total=0
    for i,j in portfolio.items():
        d=i+":"+str(j)+'\n'
        f1.write(d)
        total=total+j
    f1.write("total"+":"+str(total)+'\n')
    f1.close()
stock_prices={'tsla':100,'nifty':600,'amzn':780,'nvda':756}
p=get_stocks(stock_prices)
print(p)
save_data(p)
