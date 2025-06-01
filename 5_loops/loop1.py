

#looping ,iteration
#iterable
l1=[10,10,10,10,10]

#type 1 loop
wallet=0
for i in l1:
    wallet=wallet+i
print(wallet)
num=len(l1)
print(num)
print(wallet/num)

l2=(4,5,6)
t=0
for m1 in l2:
    t=t+m1
print(t/len(l2))

#type 2 loop
print('hello')
print(list(range(100)))

for i in range(10):
    print('hello',i)
#generate a list of 50 even numbers

l1=[]
for i in range(100):
    if i%2==0:
        l1.append(i)
print(l1)

for i in range(1):
    print(i)