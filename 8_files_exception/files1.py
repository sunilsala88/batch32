
#we always store string in text file

# a='tsla'

# f1=open('demo1.txt','w')
# f1.write(a)
# f1.close()

f2=open('demo1.txt','r')
d=f2.read()
print(d)
f2.close()

# f1=open('demo1.txt','a')
# f1.write('\nongc')
# f1.close()