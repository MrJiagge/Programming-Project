#----------Imports----------
from random import randint, choice
from time import sleep as wait
from json import load, dump

#----------Global Variables----------
player_1 = {
    "name": input("👋 What is your name player 1?: "),
    "cards": list[tuple[int, str]]
}
player_2 = {
    "name": input("👋 What is your name player 2?: "),
    "cards": list[tuple[int, str]]
}
deck_of_cards = []
authorized_players = []
colors = ["yellow", "red", "black"]

#----------Constants----------
NUMBER_OF_CARDS_IN_DECK = 30

#----------Subprograms----------
def load_authorized_players(file_path) -> list[str]:
    with open("file_path", "r") as file:
        return load(file)

def check_players(player1_name, player2_name, authorized_players) -> bool:
    return player1_name.upper() and player2_name.upper() in authorized_players