# ---------- Imports ----------
from random import randint, choice
from time import sleep as wait
from json import load, dump
from typing import List, Tuple, Dict

# ---------- Type Aliases ----------
Card = Tuple[int, str]
Deck = List[Card]

# ---------- Constants ----------
NUMBER_OF_CARDS_IN_DECK = 30
COLORS = ["yellow", "red", "black"]

# ---------- Classes ----------
class Player:
    def __init__(self, name: str):
        self.name = name
        self.cards: Deck = []

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def remove_card(self) -> Card:
        return self.cards.pop()

class AuthorizedPlayers:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.players: List[str] = self.load_authorized_players()

    def load_authorized_players(self) -> List[str]:
        with open(self.file_path, "r") as file:
            return load(file)

    def is_authorized(self, player_name: str) -> bool:
        return player_name.upper() in self.players

class Deck:
    def __init__(self):
        self.cards: Deck = self.create_deck()

    def create_deck(self) -> Deck:
        deck: Deck = []
        existing_cards = set()
        while len(deck) < NUMBER_OF_CARDS_IN_DECK:
            number = randint(1, 10)
            color = choice(COLORS)
            new_card = (number, color)
            if new_card not in existing_cards:
                existing_cards.add(new_card)
                deck.append(new_card)
        return deck

    def draw_card(self) -> Card:
        return self.cards.pop(0)

class Game:
    def __init__(self):
        self.deck = Deck()
        self.authorized_players = AuthorizedPlayers("authorized_players.json")

    def check_players(self, player1: Player, player2: Player) -> bool:
        return self.authorized_players.is_authorized(player1.name) and self.authorized_players.is_authorized(player2.name)

    def get_cards_from_deck(self, player1: Player, player2: Player) -> None:
        player1.add_card(self.deck.draw_card())
        player2.add_card(self.deck.draw_card())

    def calculate_winner(self, player1: Player, player2: Player) -> Player:
        player1_card_number, player1_card_color = player1.cards[-1]
        player2_card_number, player2_card_color = player2.cards[-1]
        if player1_card_color != player2_card_color:
            if (player1_card_color == "red" and player2_card_color == "yellow") or \
               (player1_card_color == "yellow" and player2_card_color == "black"):
                return player2
            else:
                return player1
        else:
            return player2 if player2_card_number > player1_card_number else player1

    def give_winner_cards(self, winner: Player, loser: Player) -> None:
        winner.add_card(loser.remove_card())

class NormalGame(Game):
    def play(self, player1: Player, player2: Player) -> None:
        if not self.check_players(player1, player2):
            print(f'Sorry, either {player1.name} or {player2.name}, or both of you are not authorized to play 🚫')
            return

        while self.deck.cards:
            self.get_cards_from_deck(player1, player2)
            winner = self.calculate_winner(player1, player2)
            self.give_winner_cards(winner, player1 if winner == player2 else player2)
        
        self.display_results(player1, player2)

    def display_results(self, player1: Player, player2: Player) -> None:
        print(f'{player1.name.capitalize()} had these cards: {player1.cards}')
        print(f'Overall, he had {len(player1.cards)} cards!')
        print('-----------------------------------------------------------------------')
        wait(2)
        print(f'{player2.name.capitalize()} had these cards: {player2.cards}')
        print(f'Overall, he had {len(player2.cards)} cards!')

class SlowGame(Game):
    def play(self, player1: Player, player2: Player) -> None:
        pass

def main() -> None:
    player_1 = Player(name=input("👋 What is your name player 1?: "))
    player_2 = Player(name=input("👋 What is your name player 2?: "))

    game_mode = input("Choose game mode (normal/slow): ").lower()
    if game_mode == "normal":
        game = NormalGame()
        game.play(player_1, player_2)
    elif game_mode == "slow":
        game = SlowGame()
        game.play(player_1, player_2)
    else:
        print("Invalid game mode selected.")

if __name__ == "__main__":
    main()
