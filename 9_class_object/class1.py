
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


class Student:
    dress_code='black_white'
    school_name='xaviers'
    subject='pcm'

    def __init__(self,name,gmail,roll_no):
        self.name=name
        self.gmail=gmail
        self.roll_no=roll_no
        

obj1=Student('matt','matt@gmail.com',55)
obj2=Student('sam','sam@gmail.com',66)

print(obj1.name)
print(obj2.name)