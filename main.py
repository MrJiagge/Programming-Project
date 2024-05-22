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