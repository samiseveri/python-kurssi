from animal import Animal

class Mammal(Animal):
    def __init__(self, species="Mammal"):  # Default species is "Mammal"
        super().__init__(4, species)  # Mammals have 4 legs
