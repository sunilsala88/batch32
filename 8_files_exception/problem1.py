

f1=open('/Users/new algo trading/batch32/8_files_exception/story.txt','r')
d=f1.read()
print(d)
l=d.split('\n')
print(l)
# l.reverse()
new_list=[]
for i in range(-1,-(len(l)+1),-1):
    new_list.append(l[i])
l=new_list
print(l)
f1.close()
f2=open('/Users/new algo trading/batch32/8_files_exception/story.txt','w')
for i in l:
    f2.write(i+'\n')
f2.close()