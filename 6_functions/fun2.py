

#local var
#global var



# name='tsla'


# def average(numbers:list)->int:
#     """
#     this function will calc avg value
#     """
#     global name
#     print(name)
#     name='goog'
#     total=0
#     for i in numbers:
#         total=total+i
#     avg=total/len(numbers)


#     return avg

# prices=[1,33,44,55,66]
# avg=average(prices)
# print(avg)

# print(name)




def abc():

    b=20
    print(a,b)
    print('inside abc')


a=10
abc()




#var inside a func is local var
#var outside a func is global var
#local var has local scope
#global var has global scope
#if you want to update global var inside a func then
#you have to write global var_name
#global var is only acessible if it is initiated before the function call