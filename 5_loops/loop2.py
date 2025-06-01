
d1={'tcs':600,'amzn':780,'goog':890}

for i in d1:
    print(i,d1.get(i))

print(list(d1.keys()))
print(list(d1.values()))
print(list(d1.items()))

for i in d1.keys():
    print(i)

for i in d1.values():
    print(i)

#type 4
for i,j in d1.items():
    print(i,j)

a='hello'

for i in a:
    print(i)

for i in range(len(a)):
    print(a[i])