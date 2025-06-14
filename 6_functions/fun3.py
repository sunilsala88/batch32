

#default agrument
def operation(num1,num2=1):
    print(num1,num2)
    print(num1/num2)

# Positional Arguments
operation(5,10)

#Keyword Arguments
operation(num2=5,num1=10)

operation(5)



def outer():
    message = "I am outer"

    def inner():
        print(message)

    inner()

outer()




def modify_list(lst):
    lst.append(4)

my_list = [1, 2, 3]
modify_list(my_list)
print(my_list)

def modify_value(x):
    x = 10

num = 5
modify_value(num)
print(num)