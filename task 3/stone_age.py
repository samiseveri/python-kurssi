from item import Item
from character import Character
from backpack import Backpack
import random

class StoneAge:
    """
    Root class for testing components of 
    the adventure game.
    """

    @staticmethod
    def main():
        StoneAge.test_items_and_characters()
        StoneAge.shop()
        StoneAge.world()

    @staticmethod
    def test_items_and_characters():
        stone = Item("small stone", 0.0, 2.0, 5.0, 10000.0)
        small_axe = Item("camping axe", 25.0, 6.0, 30.0, 42.0)

        leather_backpack = Backpack(100.0)
        if small_axe.get_volume() < leather_backpack.get_remaining_capacity():
            leather_backpack.put(small_axe)

    @staticmethod
    def shop():
        shop_keeper = Character("Bob", 10.0, 50.0, 10000.0, 9999999999)
        player = Character("Chris", 30.0, 20.0, 100.0, 200)

        sword = Item("sword", 30.0, 3.0, 8.0, 60)
        shield = Item("shield", 20.0, 4.0, 1.0, 100.0)
        shop_inventory = [sword, shield]

        leather_backpack = Backpack(100.0)
        player.set_backpack(leather_backpack)

        print("\nWelcome to the shop!")
        action = input("Would you like to buy, sell, or gamble? (buy/sell/gamble): ")

        if action == "buy":
            print(f"Available items: {[item.get_name() for item in shop_inventory]}")
            choice = input("What would you like to buy? ")
            for item in shop_inventory:
                if item.get_name().lower() == choice.lower():
                    print(f"You have bought {item.get_name()}.")
                    player.get_backpack().put(item)
                    break

        elif action == "sell":
            if player.get_backpack().is_empty():
                print("Your backpack is empty!")
            else:
                print(f"Your items: {[item.get_name() for item in player.get_backpack()._Backpack__items]}")
                choice = input("What would you like to sell? ")
                for item in player.get_backpack()._Backpack__items:
                    if item.get_name().lower() == choice.lower():
                        print(f"You sold {item.get_name()}.")
                        player.get_backpack()._Backpack__items.remove(item)
                        break

        elif action == "gamble":
            if player.get_backpack().is_empty():
                print("You have nothing to gamble!")
                return
            gamble_item = random.choice(player.get_backpack()._Backpack__items)
            reward_item = random.choice(shop_inventory)
            if random.random() > 0.5:
                print(f"You won! {gamble_item.get_name()} is replaced with {reward_item.get_name()}.")
                player.get_backpack()._Backpack__items.remove(gamble_item)
                player.get_backpack().put(reward_item)
            else:
                print(f"You lost! {gamble_item.get_name()} is taken by the shopkeeper.")
                player.get_backpack()._Backpack__items.remove(gamble_item)

    @staticmethod
    def world():
        print("\nInitializing the game world...")
        world_grid = [[None for _ in range(5)] for _ in range(5)]
        player_position = [2, 2]

        def move(direction):
            nonlocal player_position
            x, y = player_position
            if direction == "up" and x > 0:
                player_position[0] -= 1
            elif direction == "down" and x < 4:
                player_position[0] += 1
            elif direction == "left" and y > 0:
                player_position[1] -= 1
            elif direction == "right" and y < 4:
                player_position[1] += 1
            print(f"Player moved to {player_position}.")

        while True:
            command = input("Move (up/down/left/right) or exit: ")
            if command == "exit":
                break
            move(command)

if __name__ == "__main__":
    StoneAge.main()
