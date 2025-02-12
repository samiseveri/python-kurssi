import uuid  # For unique friend IDs

class Kaverit:
    def __init__(self, name, age, friendship_level, interests, nemesis, location):
        self.friend_id = str(uuid.uuid4())  # Unique identifier for each friend
        self.__name = name  # Private attribute
        self.age = age
        self.friendship_level = friendship_level
        self.interests = interests
        self.nemesis = nemesis
        self.location = location  # New attribute for location

    def __repr__(self):
        return (f"Kaverit(ID: {self.friend_id}, Name: {self.__name}, Age: {self.age}, "
                f"Score: {self.friendship_level}, Interests: {self.interests}, "
                f"Nemesis: {self.nemesis}, Location: {self.location})")

    def get_name(self):
        return self.__name

def show_kamu_list():
    """Displays the current list of friends."""
    print("\nCurrent Friends List:")
    for kaveri in kamu_list:
        print(kaveri)
    print("\n")

def rearrange_kamu_list(criteria):
    """Sorts the friend list by name, age, or friendship level."""
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
    """Edits details of a specific friend."""
    global kamu_list
    for kaveri in kamu_list:
        if kaveri.get_name().lower() == name.lower():
            try:
                kaveri.age = int(input("Enter new age: "))
            except ValueError:
                print("Invalid age. Must be a number.")
                return
            kaveri.friendship_level = input("Enter new friendship level (e.g., '4/10'): ")
            kaveri.interests = input("Enter new interests: ")
            kaveri.nemesis = input("Enter new nemesis: ")
            kaveri.location = input("Enter new location: ")  # Editing location
            print(f"{name} has been updated.")
            show_kamu_list()
            return
    print(f"{name} not found in the list.")

def remove_kaveri(name):
    """Removes a friend from the list but ensures at least one remains."""
    global kamu_list
    if len(kamu_list) == 1:
        print("Cannot remove the last friend in the list!")
        return

    kamu_list = [k for k in kamu_list if k.get_name().lower() != name.lower()]
    print(f"{name} has been removed from the list.")
    show_kamu_list()

def add_kaveri():
    """Adds a new friend to the list."""
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    rating = input("Enter rating (e.g., '4/10'): ")
    interests = input("Enter interests: ")
    nemesis = input("Enter nemesis: ")
    location = input("Enter location: ")  # New location input
    new_kaveri = Kaverit(name, age, rating, interests, nemesis, location)
    kamu_list.append(new_kaveri)
    print(f"{name} has been added to the list.")
    show_kamu_list()

def mark_best_friend():
    """Marks the best friend based on the highest friendship level."""
    if not kamu_list:
        print("No friends in the list.")
        return
    best_friend = max(kamu_list, key=lambda k: float(k.friendship_level.split('/')[0]))
    print(f"Best Friend: {best_friend.get_name()} (Friendship Score: {best_friend.friendship_level})")

# Initial friends list
kamu_list = [
    Kaverit("Tommi", 21, "4/10", "ERITTÄIN miesläheinen", "Perkeleen kissa", "Helsinki"),
    Kaverit("Iippu", 21, "0.006/10", "miesläheinen", "Tommi", "Tampere"),
    Kaverit("Veeti", 21, "2/10", "nylkyttää switch 2", "yläkerran muhamed", "Espoo"),
    Kaverit("Merppa", 21, "1.5/10", "intternet femboys", "Intternet femboy", "Oulu"),
    Kaverit("Danu", 22, "3.5/10", "auton pakoputki", "dogi", "Turku"),
    Kaverit("Urtturi", 22, "3/10", "homo", "Eetu", "Turku"),
    Kaverit("Eetu", 21, "1/10", "subwayn patonki", "Subwayn henkilökunta", "Turku"),
    Kaverit("Leevi", 22, "1.5/10", "ies", "joku katti", "Turku"),
    Kaverit("Allu", 21, "1/10", "PC", "Leevi", "Turku"),
    Kaverit("Minna", 36, "2/10", "mummo", "plösö kissa", "Turku"),
    Kaverit("Erika", 21, "0/10", "hullut", "Jenni", "Turku"),
    Kaverit("Puksu", 21, "3/10", "milfs", "milf", "Turku")
]

# Menu for interaction
while True:
    print("\nFriend Management System")
    action = input("Enter 'add', 'remove', 'sort', 'edit', 'best', 'show', or 'exit': ").strip().lower()

    if action == 'add':
        add_kaveri()

    elif action == 'remove':
        user_input = input("Enter the name of the friend to remove: ")
        remove_kaveri(user_input)

    elif action == 'sort':
        criteria = input("Sort by 'name', 'age', or 'friendship_level': ").strip().lower()
        rearrange_kamu_list(criteria)

    elif action == 'edit':
        user_input = input("Enter the name of the friend to edit: ")
        edit_kaveri(user_input)

    elif action == 'best':
        mark_best_friend()

    elif action == 'show':
        show_kamu_list()

    elif action == 'exit':
        break

    else:
        print("Invalid input. Please enter 'add', 'remove', 'sort', 'edit', 'best', 'show', or 'exit'.")


"""
Train Functions to Friend System

(a) Constructor initializes at least one carriage.	        -->        Each friend group must start with at least one friend.
(b) A train must always have at least one carriage.	        -->        A friend list must always have at least one friend.
(c) Carriages can be added to the train.	                -->        Friends can be added to the list.
(d) Carriages can be removed.	                            -->        Friends can be removed from the list.
(e) Carriages maintain a specific order.	                -->        Friends maintain an order in the list and can be sorted.
(f) Seats can be reserved in a suitable carriage.	        -->        A "best friend" can be marked based on a condition (like the highest friendship score).
(g) Seat reservations are visually reportable.	            -->        The friend list can be displayed in a clear, structured way.
(h) The train has a unique identifier.	                    -->        Each friend has a unique identifier (e.g., friend_id).
(i) The train has a departure & destination.	            -->        Friends can have a "hometown" or location.
(j) Train and carriage info must be retrievable the same way.  -->     Friend details should be accessible in a structured format.
"""
