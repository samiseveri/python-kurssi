import random
import time
import os
from datetime import datetime

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.coins = 100
        self.inventory = []
        self.properties_owned = []
        self.movie_collection = set()

    def add_score(self, points):
        self.score += points
        print(f"🌟 +{points} points! Total score: {self.score}")

class GameManager:
    def __init__(self):
        self.clear_screen()
        print("🎮 Welcome to the Ultimate Mini-Game Collection! 🎮")
        player_name = input("Enter your player name: ")
        self.player = Player(player_name)
        self.movies = {
            "Action": [
                ("The Dark Knight", 50),
                ("Mad Max: Fury Road", 40),
                ("John Wick", 45)
            ],
            "Sci-Fi": [
                ("Inception", 55),
                ("The Matrix", 50),
                ("Interstellar", 60)
            ],
            "Adventure": [
                ("Indiana Jones", 35),
                ("Jurassic Park", 45),
                ("The Lord of the Rings", 65)
            ]
        }
        self.properties = [
            ("Cozy Studio", 50, 1000, 100),
            ("Downtown Loft", 80, 2000, 200),
            ("Luxury Penthouse", 200, 5000, 500)
        ]

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_status(self):
        print(f"\
{'='*50}")
        print(f"Player: {self.player.name} | Score: {self.player.score} | Coins: 🪙 {self.player.coins}")
        if self.player.inventory:
            print("Inventory:", ", ".join(self.player.inventory))
        if self.player.properties_owned:
            print("Properties:", ", ".join(prop[0] for prop in self.player.properties_owned))
        if self.player.movie_collection:
            print("Movie Collection:", ", ".join(self.player.movie_collection))
        print(f"{'='*50}\
")

    def coin_flip_game(self):
        self.clear_screen()
        print("🎲 Welcome to the Coin Flip Challenge! 🎲")
        
        while True:
            if self.player.coins < 10:
                print("❌ Not enough coins to play!")
                return
            
            print(f"\
You have 🪙 {self.player.coins} coins")
            bet = input("Place your bet (10-50 coins) or 'q' to quit: ")
            
            if bet.lower() == 'q':
                break
                
            try:
                bet = int(bet)
                if bet < 10 or bet > 50 or bet > self.player.coins:
                    print("Invalid bet amount!")
                    continue
                    
                guess = input("Choose (H)eads or (T)ails: ").upper()
                if guess not in ['H', 'T']:
                    print("Invalid choice!")
                    continue
                
                print("\
Flipping coin", end="")
                for _ in range(3):
                    time.sleep(0.5)
                    print(".", end="", flush=True)
                print("\
")
                
                result = random.choice(['H', 'T'])
                print("🪙 Result:", "Heads" if result == 'H' else "Tails")
                
                if guess == result:
                    win_amount = bet * 2
                    self.player.coins += bet
                    self.player.add_score(bet)
                    print(f"🎉 You won {win_amount} coins!")
                else:
                    self.player.coins -= bet
                    print("😢 You lost your bet!")
                
            except ValueError:
                print("Please enter a valid number!")

    def movie_trading_game(self):
        self.clear_screen()
        print("🎬 Welcome to Movie Trading! 🎬")
        
        while True:
            print("\
Available genres:")
            for i, genre in enumerate(self.movies.keys(), 1):
                print(f"{i}. {genre}")
            print("4. Exit")
            
            choice = input("\
Select a genre (1-4): ")
            if choice == "4":
                break
                
            try:
                genre = list(self.movies.keys())[int(choice)-1]
                print(f"\
Movies in {genre}:")
                
                for i, (movie, price) in enumerate(self.movies[genre], 1):
                    owned = "✓" if movie in self.player.movie_collection else " "
                    print(f"{i}. [{owned}] {movie} - 🪙 {price}")
                
                movie_choice = input("\
Select a movie to buy (or 0 to go back): ")
                if movie_choice == "0":
                    continue
                    
                movie, price = self.movies[genre][int(movie_choice)-1]
                
                if movie in self.player.movie_collection:
                    print("You already own this movie!")
                elif self.player.coins >= price:
                    self.player.coins -= price
                    self.player.movie_collection.add(movie)
                    self.player.add_score(price)
                    print(f"🎉 You bought {movie}!")
                else:
                    print("❌ Not enough coins!")
                    
            except (ValueError, IndexError):
                print("Invalid choice!")

    def property_management_game(self):
        self.clear_screen()
        print("🏠 Welcome to Property Tycoon! 🏠")
        
        while True:
            print("\
Available properties:")
            for i, (name, size, price, income) in enumerate(self.properties, 1):
                owned = "✓" if (name, size, price, income) in self.player.properties_owned else " "
                print(f"{i}. [{owned}] {name}")
                print(f"   Size: {size}m² | Price: 🪙 {price} | Income: 🪙 {income}/turn")
            print(f"{len(self.properties)+1}. Exit")
            
            choice = input("\
Select a property (or exit): ")
            if choice == str(len(self.properties)+1):
                break
                
            try:
                property_data = self.properties[int(choice)-1]
                name, size, price, income = property_data
                
                if property_data in self.player.properties_owned:
                    print("You already own this property!")
                    self.player.coins += income
                    print(f"Collected 🪙 {income} in rent!")
                elif self.player.coins >= price:
                    confirm = input(f"Buy {name} for 🪙 {price}? (y/n): ")
                    if confirm.lower() == 'y':
                        self.player.coins -= price
                        self.player.properties_owned.append(property_data)
                        self.player.add_score(price // 10)
                        print(f"🎉 Congratulations! You now own {name}!")
                else:
                    print("❌ Not enough coins!")
                    
            except (ValueError, IndexError):
                print("Invalid choice!")

    def play(self):
        while True:
            self.clear_screen()
            self.display_status()
            
            print("🎮 Main Menu 🎮")
            print("1. 🎲 Coin Flip Challenge")
            print("2. 🎬 Movie Trading")
            print("3. 🏠 Property Management")
            print("4. 📊 Save & Exit")
            
            choice = input("\
Select a game (1-4): ")
            
            if choice == "1":
                self.coin_flip_game()
            elif choice == "2":
                self.movie_trading_game()
            elif choice == "3":
                self.property_management_game()
            elif choice == "4":
                self.save_game()
                print("Thanks for playing! 👋")
                break
            else:
                print("Invalid choice!")

    def save_game(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_data = f"""
Player: {self.player.name}
Final Score: {self.player.score}
Coins: {self.player.coins}
Properties Owned: {len(self.player.properties_owned)}
Movies Collected: {len(self.player.movie_collection)}
Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """
        
        with open(f"game_save_{timestamp}.txt", "w") as f:
            f.write(save_data)
        print(f"\
Game saved as game_save_{timestamp}.txt")

if __name__ == "__main__":
    game = GameManager()
    game.play()


# Save the gamified version to a file
with open('ultimate_minigames.py', 'w') as f:
    f.write(code)

print("Gamified version saved as ultimate_minigames.py. Features include:")
print("- Player profile with score and coin system")
print("- Coin flip gambling mini-game")
print("- Movie collection trading")
print("- Property management with passive income")
print("- Save game functionality")
print("- Interactive menus with emoji graphics")
print("\Run it with: python ultimate_minigames.py")