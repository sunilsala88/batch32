
try:
    f2=open('/Users/new algo trading/batch32/8_files_exception/data.txt','r')
    d=f2.read()
    print(d)
    print(100/0)
except:
    print('something went wrong')

print('this is very important line')