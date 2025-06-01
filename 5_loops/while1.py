
i=10
while True:
    if i==20:
        break
    print(i)
    i=i+1

#get me all even numbers between 1 and 100

l1=[]
i=0
while True:
    if i>100:
        break
    i=i+1
    if i%2==0:
        l1.append(i)
print(l1)

#multiplication table
num1=3
num2=1
while True:
    if num2==11:
        break
    print(num1,'X',num2,num1*num2)
    num2=num2+1