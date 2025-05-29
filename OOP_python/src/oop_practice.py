import math
from abc import abstractmethod, ABC
from datetime import datetime
# TASK 1
class Book:
    def __init__(self, title, author):
        self._title = title
        self._author = author
    def get_info(self):
        print(f"The {self._title} by {self._author}")

# TASK 2 (and 3)
class FictionBook(Book):
    def __init__(self, title, author, genre):
        super().__init__(title, author)
        self._genre = genre
    def get_info(self):
        print(f"The {self._title} ({self._genre}) by {self._author}")

# TASK 4
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
        if celsius < -273.15:
            raise ValueError("Temperature cannot be below -273.15°C (absolute zero)")
    
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        celsius = (value - 32) * 5/9
        if celsius < -273.15:
            raise ValueError("Temperature cannot be below -273.15°C (absolute zero)")
        self._celsius = celsius

# TASK 5
# Encapsulation: Create an  Account  class representing a bank account. It should
# have a public attribute  account_holder  and a private attribute  __balance
# initialized in the constructor. Implement public methods  deposit(amount)  and 
# withdraw(amount)  that modify the private  __balance . Ensure withdrawal doesn't
# allow the balance to go below zero. Add a public method  get_balance()  that
# returns the value of the private  __balance . Avoid direct access to  __balance  from
# outside the class.


class Account:
    def __init__(self, account_holder, balance):
        self.__balance = balance
        self.account_holder = account_holder
    
    def deposit(self, amount):
        self.__balance = self.__balance + amount
    def withdraw(self, amount):
        if amount < self.__balance:
            self.__balance = self.__balance - amount
        else:
            raise ValueError("Balance of account should not be < 0")
    def get_balance(self):
        return self.__balance

# Task 6
# Polymorphism: Write a function  display_area(shape)  that accepts any object
# which has an  calculate_area()  method and prints a message like "The area is:
# [area]". Create two different classes,  Rectangle  (with  width  and  height ) and 
# Circle  (with  radius ), both implementing a  calculate_area()  method. Instantiate
# both classes and pass the objects to your  display_area  function to demonstrate
# polymorphism.
def display_area(shape):
    print(f"The area is: {shape.calculate_area()}")

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def calculate_area(self):
        return self.width * self.height

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def calculate_area(self):
        return math.pi * self.radius ** 2

# Abstract Base Classes (ABC): Define an Abstract Base Class named  Vehicle  using
# the  abc  module. It should have an abstract method  start_engine() . Create two
# concrete subclasses,  Car  and  Motorcycle , that inherit from  Vehicle  and provide
# their own implementation for the  start_engine()  method (e.g., print "Car engine
# started Vroom Vroom" or "Motorcycle engine started Rrrrumble"). Verify that you
# cannot create an instance of the  Vehicle  ABC directly, but you can create instances
# of  Car  and  Motorcycle  and call their  start_engine()  methods.
class Vehicle(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def start_engine(self):
        print("sadfasdf")
class Car(Vehicle):
    def __init__(self):
        super().__init__()
    def start_engine(self):
        print("Car engine started Vroom Vroom")

class Motorcycle(Vehicle):
    def __init__(self):
        super().__init__()
    def start_engine(self):
        print("Motorcycle engine started Rrrrumble")

# Class Methods and Static Methods: Create a  StringUtils  class. Add a static
# method  is_palindrome(text)  that returns  True  if the given string  text  is a
# palindrome (reads the same forwards and backward), ignoring case and spaces,
# and  False  otherwise. Add a class method  get_info(cls)  that returns a string
# describing the class, like "This is a utility class: StringUtils". Test both methods by
# calling them directly on the class ( StringUtils.is_palindrome(...) , 
# StringUtils.get_info() ).
class StringUtils:
    @staticmethod
    def is_palindrome(text):
        cleaned_text = text.lower().replace(" ", "")
        return cleaned_text == cleaned_text[::-1]
    
    @classmethod
    def get_info(cls):
        return f"This is a utility class: {cls.__name__}"
    
    def reverse_string(self, text):
        print("call from reverse class !!!")
        print(self.is_palindrome(text))
        print(self.get_info())

# Operator Overloading: Create a  Vector2D  class representing a 2D vector with  x
# and  y  coordinates. Overload the addition operator ( + ) using the  __add__  special
# method so that adding two  Vector2D  objects results in a new  Vector2D  object
# representing their sum. Also, overload the multiplication operator ( * ) using 
# __mul__  so that multiplying a  Vector2D  object by a scalar (number) results in a
# new  Vector2D  object with scaled coordinates.
class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        if not isinstance(other, Vector2D):
            raise TypeError("Can only add Vector2D objects")
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar):
        if not isinstance(scalar, (int, float)):
            raise TypeError("Scalar must be a number (int or float)")
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"
# String Representations: Enhance the  Book  class from Task 1 or Task 2.
# Implement the  __str__  special method to return a user-friendly string
# representation (you can reuse the  get_info()  logic). Implement the  __repr__
# special method to return an unambiguous string representation that could ideally
# be used to recreate the object, such as  Book('The Great Gatsby', 'F. Scott
# Fitzgerald') .
# --> Handle in __repr__ of TASK 9

# Composition: Create an  Engine  class with attributes like  horsepower  and  type
# (e.g., "Petrol", "Electric"). Create a  Car  class (you can reuse the one from Task 7 or
# make a new one). Instead of inheriting, give the  Car  class an  engine  attribute
# which is an instance of the  Engine  class (passed during  Car 's initialization). Add a
# method to the  Car  class, like  display_engine_specs() , that accesses and displays
# information about its  engine  attribute.
class Engine:
    def __init__(self, horsepower, type):
        self._horsepower = horsepower
        self._type = type
    @property
    def horsepower(self):
        return self._horsepower
    @property
    def type(self):
        return self._type
class Car_v2:
    def __init__(self, car_type, Engine):
        self.__car_type = car_type
        self.__engine = Engine
    def display_engine_specs(self):
        print(f"The engine attributes of the car ({self.__car_type}): {self.__engine.horsepower} powers and {self.__engine.type} type ")
# Multiple Inheritance: Create a  Swimmer  class with a method  swim()  that prints
# "Swimming...". Create a  Flyer  class with a method  fly()  that prints "Flying...". Now,
# create an  AmphibiousPlane  class that inherits from both Swimmer  and  Flyer .
# Create an instance of  AmphibiousPlane  and call both its  swim()  and  fly()
# methods to show it has capabilities from both parent classes
class Swimmer:
    def _swim(self):
        print("Swimming....")

class Flyer:
    def _fly(self):
        print("Flying ...")

class AmphibiousPlane(Swimmer, Flyer):
    pass

# Decorators within Classes: Revisit the  StringUtils  class from Task 8. Ensure the 
# is_palindrome  method is decorated with  @staticmethod  and  get_info  is
# decorated with  @classmethod . Add a regular instance method 
# reverse_string(self, text)  that returns the reversed string. Create an instance of 
# StringUtils  and call the instance method. Verify that the static and class methods
# can still be called on the class itself
# ---> See detail in StringUtils.reverse_string()

# Singleton Pattern: Implement a  Logger  class as a singleton. This class should
# manage logging operations (you can just have it store log messages in a list for
# simplicity). Ensure that no matter how many times you try to create an instance of 
# Logger , you always get the same instance. Add a method  log(message)  to add a
# message to the log and a method  show_log()  to print all logged messages. Test by
# getting the instance multiple times, logging messages through different variables
# referencing the instance, and showing the log to confirm all messages are there
# and only one logger exists.

class Logger:
    _instance = None
    _log_history = []
    @staticmethod
    def get_instance():
        if Logger._instance == None:
            Logger()
        else:
            return Logger._instance
    
    def __init__(self):
        if Logger._instance == None:
            Logger._instance = self
        # else:
        #     raise Exception("This is singleton class")
        
    def log(self, message) -> None:
        self._log_history.append(message)
    
    def show_log(self):
        print(self._log_history)

# Mixin Classes: Create a  TimestampMixin  class. This mixin should provide a
# method  get_creation_timestamp()  that returns the time the object was created
# (hint: store  datetime.now()  in the  __init__  of the classes using the mixin, or within
# the mixin itself if designed carefully). Create two unrelated classes,  Document
# (with a  title  attribute) and  User  (with a  username  attribute). Have both 
# Document  and  User  inherit from  TimestampMixin  (and  object ). Instantiate
# both  Document  and  User  and demonstrate that both have access to the 
# get_creation_timestamp()  method provided by the mixin.

class TimestampMixin:
    def __init__(self):
        self._created_time = datetime.now()
    @property
    def created_time(self):
        return self._created_time
    
    def get_creation_timestamp(self):
        return self.created_time

class Document(TimestampMixin):
    def __init__(self):
        super().__init__()

    pass

class User(TimestampMixin):
    pass

# TASK 15
print("--------------15")
task15_ins = Document()
print(task15_ins.get_creation_timestamp())
# TASK 14 
print("--------------14")
task14_ins = Logger()
task14_ins.log("1111111111111")
task14_ins.show_log()

task14_ins2 = Logger()
task14_ins2.log("22222222222")
task14_ins2.show_log()

# TASK 1 Start
print("--------------1")
book_ins1 = Book("The Great Gatsby", "F. Scott Fitzgerald")
book_ins1.get_info()
# TASK 1 end
print("--------------2")
book_ins2 = FictionBook("Dune", "Frank Herbert", "Science Fiction")
book_ins2.get_info()
# Task 4
print("--------------4")
temp_ins1 = Temperature(15)  
print(temp_ins1.fahrenheit)  
# Task 5
print("--------------5")
banker_acc_ins1 = Account("Tuan dep zai", 100)
banker_acc_ins1.deposit(50)
#banker_acc_ins1.withdraw(151)
banker_acc_ins1.withdraw(99)
print(banker_acc_ins1.get_balance())
# Task 6
print("--------------6")
rect = Rectangle(5, 3)
circle = Circle(4)
display_area(rect)    
display_area(circle)
# Task 7
print("--------------7")
# veh_ins = Vehicle()
# veh_ins.start_engine()

car_ins = Car()
car_ins.start_engine()

motor_ins = Motorcycle()
motor_ins.start_engine()
# Task 8
print("--------------8")
print(StringUtils.is_palindrome("A man a plan a canal Panama"))
print(StringUtils.get_info())
# Task 9
print("--------------9")
v1 = Vector2D(2, 3)
v2 = Vector2D(1, 4)
print(f"v1: {v1}")                
print(f"v2: {v2}")                
print(f"v1 + v2: {v1 + v2}")       
print(f"v1 * 2: {v1 * 2}")      
# Task 11
print("--------------11")
car11_engine = Engine(110, "Electric")   
car_11 = Car_v2("SDV car", car11_engine)
car_11.display_engine_specs()
# Task 12
print("--------------12")
task12_ins = AmphibiousPlane()
task12_ins._fly()
task12_ins._swim()
# Task 13
print("--------------13")
task13_ins = StringUtils()
task13_ins.reverse_string("hihihi")
