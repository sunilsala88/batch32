


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



capital=1000
interest=8
years=0
current_money=capital
while True:
    if current_money>2*capital:
        break
    perc_8=capital*(interest/100)
    current_money=current_money+perc_8
    years=years+1

print(years)
