from animal import Animal
from mammal import Mammal
from wolf import Wolf
from bird import Bird
from dog import Dog
import time

#Tests basic Animal class (legs, species, sound).
def run_a_tests():
    print("Running A Tests...")
    time.sleep(1.0)

    a1 = Animal(6, "Insect")  
    a2 = Animal(4, "Cow") 

    a1.make_sound()
    print(f"Legs: {a1.number_of_legs()}, Species: {a1.get_species()}")  

    a2.make_sound()
    print(f"Legs: {a2.number_of_legs()}, Species: {a2.get_species()}")  



#Tests polymorphism (Mammal, Bird, Wolf).
def run_b_tests():
    print("Running B Tests...")
    time.sleep(1.0)

    a3 = Mammal("Mammal") 
    a4 = Bird()
    wolf1 = Wolf("Raasinkorpi")

    make_it_do_the_sound(a3)
    make_it_do_the_sound(a4)
    make_it_do_the_sound22(a4)
    make_it_do_the_sound(wolf1)

    wolf1.another_make_sound()
    print(f"Legs: {a3.number_of_legs()}, Species: {a3.get_species()}")  # Using encapsulated getter



def make_it_do_the_sound(any_animal: Animal):
    any_animal.make_sound()


def make_it_do_the_sound22(any_bird: Bird):
    any_bird.make_sound()



#Tests Wolf class (howling, pack name).
def run_c_tests():
    print("Running C Tests...")
    time.sleep(1.0)

    wolf = Wolf("Raasinkorpi")

    wolf.make_sound()
    print(f"Legs: {wolf.number_of_legs()}, Species: {wolf.get_species()}, Pack: {wolf.get_pack_name()}")




#Tests Bird class (singing, legs).
def run_d_tests():
    print("Running D Tests...")
    time.sleep(1.0)

    bird = Bird()

    bird.make_sound()
    print(f"Legs: {bird.number_of_legs()}")



#	Tests Dog class (barking, fetching, breed).
def run_dog_tests():
    print("Running Dog Tests...")
    time.sleep(1.0)

    dog1 = Dog("Buddy", "Golden Retriever")
    dog2 = Dog("Max", "Bulldog")

    dog1.make_sound()  
    dog2.make_sound()  
    
    dog1.fetch()  
    dog2.fetch()  

    print(f"Dog 1: Name = {dog1.get_breed()}, Species = {dog1.get_species()}")
    print(f"Dog 2: Name = {dog2.get_breed()}, Species = {dog2.get_species()}")


# Running all tests
print("Starting Tests...\n")

print("A-Tests:")
run_a_tests()

print("\nB-Tests:")
run_b_tests()

print("\nC-Tests:")
run_c_tests()

print("\nD-Tests:")
run_d_tests()

print("\nDog-Tests:")
run_dog_tests()
