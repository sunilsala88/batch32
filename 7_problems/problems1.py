


def rev_string(word:str)->str:
    l=len(word)
    indexes=range(-1,-(l+1),-1)
    ans=""
    for i in indexes:
        ans=ans+word[i]
    return ans

def rev_string2(word:str)->str:

    ans=''
    for i in word:
        ans=i+ans
    return ans

def is_plaindrome(word:str)->bool:
    rev_word=rev_string(word)
    print(rev_word)
    if word==rev_word:
        return True
    else:
        return False


word='level'
a=is_plaindrome(word)
print(a)
print(rev_string2('tsla'))



name=['TSLA','GOOG','AMZN']
prices=[66,77,88]
#l1+l2
stock_prices={}
for i in range(len(name)):
    stock_prices.update({name[i]:prices[i]})
print(stock_prices)


def get_year(capital:int,interest:int)->int:
    years=0
    current_money=capital
    while True:
        if current_money>2*capital:
            break
        perc_8=current_money*(interest/100)
        current_money=current_money+perc_8
        years=years+1

    return (years)
print(get_year(1000,8))


def get_shares(quantity,divends,price,years):

    total_value=quantity*price
    for i in range(years):
        total_value=total_value+(divends*quantity)
        quantity=total_value/price
    final=total_value/price
    return final

f=get_shares(100,2,50,5)
print(f)

def pension_fund(initial,monthy,interest,duration):

    current=initial
    for i in range(1,(duration*12)+1):
        if i%12==0:
            current_int=(current*(interest))
            current=current+monthy+current_int
            print(i,current_int)
        else:
            print(i)
            current=current+monthy
    return current


c=pension_fund(50000,200, 0.06,20)
print(c)



closing_prices=list(range(101,150))
print(closing_prices)
mv=5

sma=[]
for i in range(len(closing_prices)):
    if i<mv:
        sma.append(closing_prices[i])
    else:
        last_mv=closing_prices[i-5:i]
        avg=sum(last_mv)/mv
        sma.append(avg)
print(sma)