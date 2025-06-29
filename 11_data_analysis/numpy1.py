

#numy->array
#array is upgraded list
#numpy array has same type of value
#array we add with number (operation is performed 
# on inid element)

# l1=[33,44,55,66.5]
# print(l1*3)
# print(l1+l1)

# import numpy as np
# np1=np.array(l1)
# print(np1+3)
# print(np1+np1)

# l2=[
#     [11,22,33],
#     [44,55,66],
#     [77,88,99]
# ]
# print(l2)
# npm=np.array(l2)
# print(npm)
# print(npm[2,2])

# print(npm[1:,1:])

# print(npm[0:2,0:2])
import numpy as np
a=np.arange(25).reshape(5,5)
print(a)
print(a[1:3,2:4])