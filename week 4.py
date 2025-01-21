class Kaverit:
    species = "Canine"  # Class attribute (you can change this if needed!)

    def __init__(self, name, age, tuntenut, score, sukupuoli, lemmikki_status):
        self.__name = name  # Private instance attribute
        self.age = age  # Instance attribute
        self.tuntenut = tuntenut  # How long they've known each other
        self.score = score  # Friendship score
        self.sukupuoli = sukupuoli  # Personality trait or gender attribute
        self.lemmikki_status = lemmikki_status  # Pet status or unique quirk

    def __str__(self):
        return (f"{self.__name}, {self.age} years old, "
                f"Known for {self.tuntenut} years, "
                f"Score: {self.score}, Sexuality: {self.sukupuoli}, "
                f"Lemmikki: {self.lemmikki_status}")

    def get_name(self):
        """Getter for the private name attribute."""
        return self.__name

    def compare_score(self, other):
        """Compares the friendship score with another Kaverit."""
        if isinstance(other, Kaverit):
            return f"{self.__name} and {other.get_name()}: {self.score} vs {other.score}"
        return "Comparison failed: other is not a Kaverit."

    def get_friendship_strength(self):
        """Calculates a simple friendship strength metric."""
        try:
            numeric_score = float(self.score.split('/')[0])
            return numeric_score * self.tuntenut
        except ValueError:
            return 0  # Handles invalid score formatting


# Creating objects
kamu_list = [
    Kaverit("Tommi", 21, 8, "4/10", "ERITTÄIN miesläheinen", "Perkeleen kissa"),
    Kaverit("Iippu", 21, 13, "0.006/10", "miesläheinen", "Tommi"),
    Kaverit("Veeti", 21, 5, "2/10", "nylkyttää switch 2", "yläkerran muhamed"),
    Kaverit("Merppa", 21, 6, "1.5/10", "intternet femboys", "Intternet femboy"),
    Kaverit("Danu", 22, 10, "3.5/10", "auton pakoputki", "dogi"),
    Kaverit("Urtturi", 22, 6, "3/10", "homo", "Eetu"),
    Kaverit("Eetu", 21, 6, "1/10", "subwayn patonki", "Subwayn henkilökunta"),
    Kaverit("Leevi", 22, 6, "1.5/10", "ies", "joku katti"),
    Kaverit("Allu", 21, 6, "1/10", "PC", "Leevi"),
    Kaverit("Minna", 36, 1, "2/10", "mummo", "plösö kissa"),
    Kaverit("Erika", 21, 7, "0/10", "hullut", "Jenni"),
    Kaverit("Puksu", 21, 10, "3/10", "milfs", "milf")
]

# Example usage
print("All Friends:")
for kamu in kamu_list:
    print(kamu)

print("\nComparing Scores:")
print(kamu_list[0].compare_score(kamu_list[1]))

print("\nFriendship Strength Rankings:")
sorted_kamu = sorted(kamu_list, key=lambda x: x.get_friendship_strength(), reverse=True)
for idx, kamu in enumerate(sorted_kamu, 1):
    print(f"{idx}. {kamu.get_name()} - Strength: {kamu.get_friendship_strength()}")
