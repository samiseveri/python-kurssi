from mammal import Mammal

class Wolf(Mammal):
    def __init__(self, pack_name: str):
        super().__init__("Wolf")  
        self.__pack_name = pack_name  

    def make_sound(self):
        print("*Awooooo!*")  

    def another_make_sound(self):
        print("*Growl...*")

    def get_pack_name(self):
        return self.__pack_name  

    def set_pack_name(self, pack_name):
        self.__pack_name = pack_name  
