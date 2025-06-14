
#parameter ,argument

def average(numbers):

    total=0
    for i in numbers:
        total=total+i
    avg=total/len(numbers)


    return avg

prices=[1,33,44,55,66]
avg=average(prices)
print(avg)


def get_fib(number):

    list1=[1,1]
    num1=list1[0]
    num2=list1[1]
    for i in range(number-2):
        num3=num1+num2
        list1.append(num3)
        num1=num2
        num2=num3
    
    return list1

l=get_fib(10)
print(l)

def add_value(num1,num2):
    return num1+num2

a=add_value(10,20)
print(a)

def print_hello():
    for i in range(5):
        print('hello')

print_hello()