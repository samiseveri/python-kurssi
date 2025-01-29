import random

# Card class to represent a single playing card
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"

# Deck class to represent a deck of 52 playing cards
class Deck:
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', '11 (Jack)', '12 (Queen)', '13 (King)', 'Ace']

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)

    def deal(self, num_cards):
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards

# Player class to represent a player in the game
class Player:
    def __init__(self, name, chips, is_human=False):
        self.name = name
        self.hand = []
        self.chips = chips
        self.current_bet = 0
        self.is_human = is_human

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def show_hand(self):
        return f"{self.name}'s hand: {', '.join(map(str, self.hand))}"

    def place_bet(self, amount):
        if amount > self.chips:
            raise ValueError(f"{self.name} does not have enough chips to bet {amount}.")
        self.chips -= amount
        self.current_bet += amount
        return amount

    def reset_bet(self):
        self.current_bet = 0

    def is_busted(self):
        return self.chips <= 0

# Game class to manage the Texas Hold'em game
class TexasHoldemGame:
    def __init__(self, human_name, starting_chips, num_computers):
        self.deck = Deck()
        self.players = [Player(human_name, starting_chips, is_human=True)]
        self.players.extend([Player(f"Computer {i+1}", starting_chips) for i in range(num_computers)])
        self.community_cards = []
        self.pot = 0

    def deal_hole_cards(self):
        for player in self.players:
            player.receive_cards(self.deck.deal(2))

    def deal_community_cards(self, number):
        self.community_cards.extend(self.deck.deal(number))

    def show_community_cards(self):
        return f"Community Cards: {', '.join(map(str, self.community_cards))}"

    def betting_round(self):
        print("Starting a betting round...")
        for player in self.players[:]:
            if player.is_busted():
                continue
            if player.is_human:
                try:
                    bet = int(input(f"{player.name}, you have {player.chips} chips. Enter your bet (0 to fold): "))
                    if bet == 0:
                        print(f"{player.name} folds.")
                        self.players.remove(player)
                    else:
                        self.pot += player.place_bet(bet)
                        print(f"{player.name} bets {bet}. Current pot: {self.pot} chips.")
                except ValueError:
                    print(f"Invalid input! {player.name} folds.")
                    self.players.remove(player)
            else:
                # Simple AI: Computer bets a random amount within their chips
                bet = random.randint(1, player.chips // 2) if player.chips > 1 else 1
                self.pot += player.place_bet(bet)
                print(f"{player.name} bets {bet}. Current pot: {self.pot} chips.")

    def play_game(self):
        print("Starting Texas Hold'em Game!")
        while len([player for player in self.players if not player.is_busted()]) > 1:
            self.deck = Deck()
            self.community_cards = []
            self.pot = 0
            self.deal_hole_cards()

            # Show human player's hand
            for player in self.players:
                if player.is_human:
                    print(player.show_hand())

            # Pre-flop betting
            self.betting_round()

            # Flop (3 community cards)
            print("\nDealing the flop...")
            self.deal_community_cards(3)
            print(self.show_community_cards())
            self.betting_round()

            # Turn (1 community card)
            print("\nDealing the turn...")
            self.deal_community_cards(1)
            print(self.show_community_cards())
            self.betting_round()

            # River (1 community card)
            print("\nDealing the river...")
            self.deal_community_cards(1)
            print(self.show_community_cards())
            self.betting_round()

            # Reset bets for the next round
            for player in self.players:
                player.reset_bet()

            print(f"\nEnd of the round. The pot is {self.pot} chips. Evaluate hands to determine the winner.")

        winner = [player for player in self.players if not player.is_busted()][0]
        print(f"Game over! The winner is {winner.name} with {winner.chips} chips left.")

# Example usage
if __name__ == "__main__":
    human_name = "Player"
    starting_chips = 100
    num_computers = 2
    game = TexasHoldemGame(human_name, starting_chips, num_computers)
    game.play_game()


# all in ei toimi, jos pelaajan panokset loppuu niin peli menee rikki