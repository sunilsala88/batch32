

# num=1

# while True:
#     if num==101:
#         break
#     print(num)
#     num=num+2

# print('last line')

# stock_prices={'tsla':700,'goog':900,'amzn':680,'nvda':567}
# portfolio=[]
# while True:
#     name=input('enter the stock name (q to quit)')
#     if name.upper()=='Q':
#         break
#     if name=='nvda':
#         print('you cannot trade this stock try something else')
#         continue

#     found=stock_prices.get(name)
#     if found:
#         portfolio.append(name)
#     else:
#         print('this stock name is invalid type again')
# print(portfolio)


list1=[44,55,63,45,23,67,56]
high=list1[0]
i=0
while True:
    if i==len(list1):
        break
    print(list1[i])
    if high<list1[i]:
        high=list1[i]
    i=i+1
print(high)