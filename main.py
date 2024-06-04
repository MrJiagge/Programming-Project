#----------Imports----------
from random import randint, choice
from time import sleep as wait
from json import load, dump

#----------Type Aliases----------
player = dict[str, list[tuple[int, str]]]
card = tuple[int, str]
deck = list[card]

#----------Global Variables----------
player_1 = {
    "name": input("👋 What is your name player 1?: "),
    "cards": deck
}
player_2 = {
    "name": input("👋 What is your name player 2?: "),
    "cards": deck
}
deck_of_cards = []
authorized_players = []
colors = ["yellow", "red", "black"]

#----------Constants----------
NUMBER_OF_CARDS_IN_DECK = 30

#----------Subprograms----------
def load_authorized_players(file_path: str) -> list[str]:
    with open(file_path, "r") as file:
        return load(file)

def check_players(player1_name, player2_name, authorized_players) -> bool:
    return player1_name.upper() and player2_name.upper() in authorized_players

def create_deck(deck, number_of_cards) -> deck:
    existing_cards = set()
    
    while len(deck) < number_of_cards:
        number = randint(1, 10)
        color = choice(colors)
        new_card = (number, color)
        
        if new_card not in existing_cards:
            existing_cards.add(new_card)
            deck.append(new_card)
    return deck

def get_card_from_deck(deck, player) -> None:
    removed_card = deck.pop(0)
    player["cards"].append(removed_card)

def calculate_winner(player1, player2) -> player:
    # card from deck was APPENDED -> use -1 to get last element
    # cards are a tuple[int, str] -> use 0 to get 1st element which is int(card number)
    player1_card_number = player_1["cards"][-1][0]
    player2_card_color = player_2["cards"][-1][1]
    
    # use 1 to get 2nd element which is str(card color)
    player1_card_color = player_1["cards"][-1][1]
    player2_card_number = player_2["cards"][-1][0]
    
    if player1_card_color != player2_card_color:
        # if statement contains all possible ways player2 can win otherwise player1 wins
        return player2 if (player1_card_color == "red" and player2_card_color == "yellow") or (player1_card_color == "yellow" and player2_card_color == "black") else player1
    # return player who's card has a greater number if colors are equal
    return player2 if player2_card_number > player1_card_number else player1

print("Commit test")
    