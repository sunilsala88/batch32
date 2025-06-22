
#class
#class is the blueprint of obeject

#object
#instance of the class

#atrribute
#any variable that you create inside a class is called attribute

#class attribute
#common characteristic of a entity

#instance attribute
#unique for each object

#method
#function that you create inside a class is called method

#init method->constructor
#it is executed automatically when you create an object

class Student:
    dress_code='black_white'
    school_name='xaviers'
    subject='pcm'

    #constructor
    def __init__(self,name,gmail,roll_no):
        self.name=name
        self.gmail=gmail
        self.roll_no=roll_no
        
    def about_me(self):
        return f'my name is {self.name}'

obj1=Student('matt','matt@gmail.com',55)
obj2=Student('sam','sam@gmail.com',66)

print(obj1.name)
print(obj2.name)

print(obj1.about_me())
print(obj2.about_me())


#class called circle

class Circle:
    pi=3.14

    def __init__(self,radius):
        self.radius=radius

    def circumference(self):
        #2*pi*r
        return 2*self.pi*self.radius

    def area(self):
        return self.pi*(self.radius**2)

c1=Circle(radius=5)
c2=Circle(radius=10)

print(c1.radius)
print(c2.radius)

print(c1.area())
print(c2.area())


class Book:

    def __init__(self,title,author,price,quantity=10):
        self.title=title
        self.author=author
        self.price=price
        self.quantity=quantity

    def get_price(self):
        return self.price
    
    def set_price(self, new_price):
        self.price=new_price

    def get_quantity(self):
        return self.quantity
    
    def set_quantity(self, new_quantity):
        self.quantity=new_quantity
        return self.quantity
    
    def sell(self, number_sold):
        self.quantity=self.quantity-number_sold
    
    def restock(self, number_added): 
        self.quantity=self.quantity+number_added

b1 = Book(title="1984", author="George Orwell", price=29.99, quantity=100)
b2 = Book(title="flames", author="mathew", price=25, quantity=100)

print(b1.set_quantity(200))
print(Book.set_quantity(b1,200))



# print(b2.price)
# b2.set_price(30)
# print(b2.price)

# class BankAccount:
#     bank_name='jpmorgan'

#     def __init__(self,account_number, initial_balance):
#         self.account_number=account_number
#         self.balance=initial_balance
    
#     def deposit(self,amount):
#         if amount<0:
#             print('invalid amount')
#         else:
#             self.balance=self.balance+amount
    
#     def withdraw(self, amount):
#         if amount<self.balance:
#             self.balance=self.balance-amount
#     def get_balance(self):
#         return self.balance
    
# my_account = BankAccount(account_number="12345678", initial_balance=1000)

# # Deposit and withdraw
# my_account.deposit(500)
# my_account.withdraw(200)
# print(my_account.get_balance())  # Output: 1300


# class Broker:
#     stock_prices={'tsla':100,'nifty':600,'amzn':780,'nvda':756}
    

#     def __init__(self,name,acc_no,money):
#         self.account_name=name
#         self.wallet=money
#         self.account_no=acc_no
#         self.portfolio={}

#     def get_porfolio(self):
#         return self.portfolio
    
#     def buy_stock(self,name):
#         found=self.stock_prices.get(name)
#         if found:
#             if self.wallet>found:
#                 self.portfolio.update({name:found})
#                 self.wallet=self.wallet-found
#                 return 'buying '+name
#             else:
#                 print('not enough money')
#         else:
#             print('not found')
    
#     def sell_stock(self,name):
#         found=self.portfolio.get(name)
#         if found:
#             self.portfolio.pop(name)
#             self.wallet=self.wallet+found
#             return 'selling ' +name
#         else:
#             print('stock not found')

        


# user1=Broker('matt',450,1000)
# print(user1.account_name,user1.wallet,user1.portfolio)
# print(user1.buy_stock('tsla'))
# print(user1.get_porfolio())
# print(user1.buy_stock('nifty'))
# print(user1.get_porfolio())
# print(user1.sell_stock('tsla'))
# print(user1.get_porfolio())

# #self
# #all method first parameter should be self
# #if you want to access any attribute (varible ) inside a class then you have to use self