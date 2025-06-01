

l1=[4,2,6,7,55,45,67]

high=l1[0]
for i in l1:
    if high<i:
        high=i
print(high)

Prices=[100, 105, 110]
Volumes=[200, 150, 300]
#vwap

num=0
den=0

for i in range(len(Prices)):
    n=Prices[i]*Volumes[i]
    num=num+n
    den=den+Volumes[i]

print(num/den)



quantities=[100, 200, 150]
Dividends =[0.5, 1, 0.2]

total=0

for i in range(len(Dividends)):
    total=total+quantities[i]*Dividends[i]
print(total)

trades=[20, -10, 15, -5, 30]
count=0
for i in trades:
    if i>0:
        count=count+1
        # count+=1
print(count)