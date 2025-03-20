from wolf import Wolf

class Dog(Wolf):
    def __init__(self, name: str, breed: str):
        super().__init__("Domestic Pack")  # Dogs belong to domestic packs
        self.__name = name  # Encapsulated dog name
        self.__breed = breed  # Encapsulated breed

    def make_sound(self):
        print("Bark! Bark!")  # Dynamic binding - overriding method

    def fetch(self):
        print(f"{self.__name} is fetching the ball!")  # New method for dogs

    def get_breed(self):
        return self.__breed  # Getter for breed

    def set_breed(self, breed):
        self.__breed = breed  # Setter for breed
