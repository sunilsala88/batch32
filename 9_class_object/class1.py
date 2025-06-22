
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
    
    def sell(self, number_sold):
        self.quantity=self.quantity-number_sold
    
    def restock(self, number_added): 
        self.quantity=self.quantity+number_added

b1 = Book(title="1984", author="George Orwell", price=29.99, quantity=100)
b2 = Book(title="flames", author="mathew", price=25, quantity=100)

print(b2.price)
b2.set_price(30)
print(b2.price)