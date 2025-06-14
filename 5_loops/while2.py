

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


# list1=[44,55,63,45,23,67,56]
# high=list1[0]
# i=0
# while True:
#     if i==len(list1):
#         break
#     current=list1[i]
#     print(current)
#     if high<current:
#         high=current
#     i=i+1
# print(high)


#10 fib number
# 1,1,2,3,5,8,13,21,34,55
# number=10
# fib=[1,1]
# n1=fib[0]
# n2=fib[1]
# for i in range(number-2):
#     n3=n1+n2
#     fib.append(n3)
#     n1=n2
#     n2=n3
# print(fib)


# number=10
# fib=[1,1]
# n1=fib[0]
# n2=fib[1]
# count=0
# while True:
#     if count==number-2:
#         break
#     n3=n1+n2
#     fib.append(n3)
#     n1=n2
#     n2=n3
#     count=count+1
# print(fib)

# l1=[44,55,66,77,88]

# i=-1
# l2=[]
# while True:
#     if i==-(len(l1)+1):
#         break
#     current=l1[i]
#     l2.append(current)
#     i=i-1
# print(l2)

print(list(range(5)))
print(list(range(5,10)))
print(list(range(5,25,3)))

print(list(range(-1,-6,-1)))

l1=[44,55,66,77,88]
l2=[]
end=-(len(l1)+1)
for i in range(-1,end,-1):
    l2.append(l1[i])
print(l2)