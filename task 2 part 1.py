class Kaverit:
    def __init__(self, name, age, friendship_level, interests, nemesis):
        self.__name = name  # Private attribute
        self.age = age
        self.friendship_level = friendship_level
        self.interests = interests
        self.nemesis = nemesis

    def __repr__(self):
        return f"Kaverit({self.__name}, {self.age}, {self.friendship_level}, {self.interests}, {self.nemesis})"

    def get_name(self):
        return self.__name

def show_kamu_list():
    print("Current Friends List:")
    for kaveri in kamu_list:
        print(kaveri)
    print("\n")

def rearrange_kamu_list(criteria):
    global kamu_list
    if criteria == "name":
        kamu_list.sort(key=lambda k: k.get_name().lower())
    elif criteria == "age":
        kamu_list.sort(key=lambda k: k.age)
    elif criteria == "friendship_level":
        kamu_list.sort(key=lambda k: float(k.friendship_level.split('/')[0]))
    else:
        print("Invalid criteria. Choose from 'name', 'age', or 'friendship_level'.")
    
    print(f"List rearranged by {criteria}.")
    show_kamu_list()

def edit_kaveri(name):
    global kamu_list
    for kaveri in kamu_list:
        if kaveri.get_name().lower() == name.lower():
            kaveri.age = int(input("Enter new age: "))
            kaveri.friendship_level = input("Enter new friendship level (e.g., '4/10'): ")
            kaveri.interests = input("Enter new interests: ")
            kaveri.nemesis = input("Enter new pet status: ")
            print(f"{name} has been updated.")
            show_kamu_list()
            return
    print(f"{name} not found in the list.")

kamu_list = [
    Kaverit("Tommi", 21, "4/10", "ERITTÄIN miesläheinen", "Perkeleen kissa"),
    Kaverit("Iippu", 21, "0.006/10", "miesläheinen", "Tommi"),
    Kaverit("Veeti", 21, "2/10", "nylkyttää switch 2", "yläkerran muhamed"),
    Kaverit("Merppa", 21, "1.5/10", "intternet femboys", "Intternet femboy"),
    Kaverit("Danu", 22, "3.5/10", "auton pakoputki", "dogi"),
    Kaverit("Urtturi", 22, "3/10", "homo", "Eetu"),
    Kaverit("Eetu", 21, "1/10", "subwayn patonki", "Subwayn henkilökunta"),
    Kaverit("Leevi", 22, "1.5/10", "ies", "joku katti"),
    Kaverit("Allu", 21, "1/10", "PC", "Leevi"),
    Kaverit("Minna", 36, "2/10", "mummo", "plösö kissa"),
    Kaverit("Erika", 21, "0/10", "hullut", "Jenni"),
    Kaverit("Puksu", 21, "3/10", "milfs", "milf")
]

def remove_kaveri(name):
    global kamu_list
    kamu_list = [kaveri for kaveri in kamu_list if kaveri.get_name().lower() != name.lower()]
    print(f"{name} has been removed from the list.")
    show_kamu_list()

def add_kaveri():
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    rating = input("Enter rating (e.g., '4/10'): ")
    interests = input("Enter interests: ")
    nemesis = input("Enter pet status: ")
    new_kaveri = Kaverit(name, age, rating, interests, nemesis)
    kamu_list.append(new_kaveri)
    print(f"{name} has been added to the list.")
    show_kamu_list()

# Example usage
while True:
    print("Current list:")
    show_kamu_list()
    action = input("Enter 'remove' to delete a friend, 'add' to add a new friend, 'rearrange' to sort the list, 'edit' to modify a friend, or 'exit' to quit: ").strip().lower()
    if action == 'remove':
        user_input = input("Enter the name of the friend to remove: ")
        remove_kaveri(user_input)
    elif action == 'add':
        add_kaveri()
    elif action == 'rearrange':
        criteria = input("Enter sorting criteria ('name', 'age', 'friendship_level'): ").strip().lower()
        rearrange_kamu_list(criteria)
    elif action == 'edit':
        user_input = input("Enter the name of the friend to edit: ")
        edit_kaveri(user_input)
    elif action == 'exit':
        break
    else:
        print("Invalid input. Please enter 'remove', 'add', 'rearrange', 'edit', or 'exit'.")

print("Final list:")
show_kamu_list()
