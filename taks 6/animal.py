class Animal:
    def __init__(self, number_of_legs: int, species: str):
        assert number_of_legs >= 0, "Number of legs cannot be negative."
        self.__legs = number_of_legs  # Encapsulated variable
        self.__species = species  # New instance variable

    def number_of_legs(self):
        return self.__legs  # Encapsulated getter

    def make_sound(self):
        print("*it's quiet*")

    def get_species(self):
        return self.__species  # Getter for species

    def set_species(self, species):
        self.__species = species  # Setter for species
