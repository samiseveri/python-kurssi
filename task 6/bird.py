from animal import Animal

class Bird(Animal):
    def __init__(self):
        super().__init__(2, "Bird")  # Birds have 2 legs, added species

    def make_sound(self):
        print("*clear bird singing*")  # Overriding method
