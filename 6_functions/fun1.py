
#parameter ,argument

def average(numbers:list)->int:
    """
    this function will calc avg value
    """

    total=0
    for i in numbers:
        total=total+i
    avg=total/len(numbers)


    return avg

prices=[1,33,44,55,66]
avg=average(prices)
print(avg)


def get_fib(number:int)->list:
    """
    this func will return fib numbers
    """

    list1=[1,1]
    num1=list1[0]
    num2=list1[1]
    for i in range(number-2):
        num3=num1+num2
        list1.append(num3)
        num1=num2
        num2=num3
    
    return list1

l=get_fib(10)
print(l)

def add_value(num1:int,num2:int)->int:
    return num1+num2

a=add_value(10,20)
print(a)

def print_hello():
    for i in range(5):
        print('hello')

print_hello()






def get_stocks(stock_prices:dict)->list:
    """
    this function will take input for stocks
    and return protfolio list
    """
    portfolio=[]
    while True:
        name=input('enter the stock name (q to quit)')
        if name.upper()=='Q':
            break
        if name=='nvda':
            print('you cannot trade this stock try something else')
            continue

        found=stock_prices.get(name)
        if found:
            portfolio.append(name)
        else:
            print('this stock name is invalid type again')
    return portfolio

# stock_prices={'tsla':700,'goog':900,'amzn':680,'nvda':567}
# p=get_stocks(stock_prices)
# print(p)


#rev list
#rev string

def rev_list(list1:list)->list:

    end=-(len(list1)+1)    
    l=range(-1,end,-1)
    print(list(l))
    ans=[]
    for i in l:
        ans.append(list1[i])
    return ans
print('hello')
a=rev_list([11,22,33])
print(a)


def rev_string(word:str)->str:

    end=-(len(word)+1)    
    l=range(-1,end,-1)
    print(list(l))
    ans=""
    for i in l:
        ans=ans+word[i]
    return ans
a=rev_string('sunil')
print(a)