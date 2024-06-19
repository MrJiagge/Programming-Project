# ---------- Imports ----------
from random import randint, choice
from time import sleep as wait
from json import load, dump
from typing import Dict, List, Tuple

# ---------- Type Aliases ----------
Player = Dict[str, List[Tuple[int, str]]]
Card = Tuple[int, str]
Deck = List[Card]

# ---------- Global Variables ----------
player_1: Player = {
    "name": input("👋 What is your name player 1?: "),
    "cards": []
}
player_2: Player = {
    "name": input("👋 What is your name player 2?: "),
    "cards": []
}
deck_of_cards: Deck = []
authorized_players: List[str] = []
colors = ["yellow", "red", "black"]

# ---------- Constants ----------
NUMBER_OF_CARDS_IN_DECK = 30

# ---------- Subprograms ----------
def load_authorized_players(file_path: str) -> List[str]:
    """
    Load the list of authorized players from a JSON file.
    """
    with open(file_path, "r") as file:
        return load(file)

def check_players(player1_name: str, player2_name: str, authorized_players: List[str]) -> bool:
    """
    Check if both players are authorized to play the game.
    Names in the JSON file are uppercase.
    """
    return player1_name.upper() in authorized_players and player2_name.upper() in authorized_players

def create_deck(number_of_cards: int) -> Deck:
    """
    Create a deck of unique cards with specified number of cards.
    """
    deck: Deck = []
    existing_cards = set()
    
    while len(deck) < number_of_cards:
        number = randint(1, 10)
        color = choice(colors)
        new_card = (number, color)
        
        if new_card not in existing_cards:
            existing_cards.add(new_card)
            deck.append(new_card)
    return deck

def get_cards_from_deck(deck: Deck, player1: Player, player2: Player) -> None:
    """
    Distribute one card to each player from the deck.
    """
    player1["cards"].append(deck.pop(0))
    player2["cards"].append(deck.pop(0))

def calculate_winner(player1: Player, player2: Player) -> Player:
    """
    Determine the winner between two players based on the last card drawn.
    The card was appended therefore -1 index gets the last element.
    """
    
    player1_card_number, player1_card_color = player1["cards"][-1]
    player2_card_number, player2_card_color = player2["cards"][-1]
    
    if player1_card_color != player2_card_color:
        """
        The IF statement contains all possible ways player_2 can win
        """
        if (player1_card_color == "red" and player2_card_color == "yellow") or \
           (player1_card_color == "yellow" and player2_card_color == "black"):
            return player2
        else:
            return player1
    else:
        """"
        If both card colors are the same, return the player who's card number
        is the greatest.
        """
        return player2 if player2_card_number > player1_card_number else player1

def give_winner_cards(winner: Player, loser: Player) -> None:
    """
    Transfer the last card of the loser to the winner.
    """
    winner["cards"].append(loser["cards"].pop())

def normal_game() -> None:
    """
    Conduct the normal game flow: load players, create deck, distribute cards, 
    determine the winner, and print final card holdings of each player. This is
    the faster game.
    """
    global deck_of_cards
    player1_name = player_1["name"]
    player2_name = player_2["name"]

    authorized_players.extend(load_authorized_players("authorized_players.json"))
    if not check_players(player1_name, player2_name, authorized_players):
        print(f'Sorry, either {player1_name} or {player2_name}, or both of you are not authorized to play 🚫')
        return

    deck_of_cards = create_deck(NUMBER_OF_CARDS_IN_DECK)
    while deck_of_cards:
        get_cards_from_deck(deck_of_cards, player_1, player_2)
        winner = calculate_winner(player_1, player_2)
        """"
        The player who is the loser in this parameter is always player_1
        if the winner is player_2. Otherwise, player_2 is the loser as they are
        not the winner.
        """
        give_winner_cards(winner, player_1 if winner == player_2 else player_2)
    
    print(f'{player1_name.capitalize()} had these cards: {player_1["cards"]}')
    print(f'Overall, he had {len(player_1["cards"])} cards!')
    print('-----------------------------------------------------------------------')
    
    wait(2)
    print(f'{player2_name.capitalize()} had these cards: {player_2["cards"]}')
    print(f'Overall, he had {len(player_2["cards"])} cards!')
    
    
def slow_game() -> None:
    pass

def main() -> None:
    """
    Entry point for the game.
    """
    normal_game()

if __name__ == "__main__":
    main()

