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
AUTHORIZED_PLAYERS_FILE = "authorized_players.json"
LEADERBOARD_FILE = "leaderboard.json"

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
    """
    # Names in the JSON file are uppercase.
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
    """
    player1_card_number, player1_card_color = player1["cards"][-1]
    player2_card_number, player2_card_color = player2["cards"][-1]
    
    if player1_card_color != player2_card_color:
        if (player1_card_color == "red" and player2_card_color == "yellow") or \
           (player1_card_color == "yellow" and player2_card_color == "black"):
            return player2
        else:
            return player1
    else:
        return player2 if player2_card_number > player1_card_number else player1

def give_winner_cards(winner: Player, loser: Player) -> None:
    """
    Transfer the last card of the loser to the winner.
    """
    winner["cards"].append(loser["cards"].pop())

def update_leaderboard(winner_name: str, cards_count: int) -> None:
    """
    Update the leaderboard with the winner's name and number of cards they won by.
    """
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            leaderboard = load(file)
    except FileNotFoundError:
        leaderboard = []

    leaderboard.append({"name": winner_name, "cards": cards_count})
    
    # Sort the leaderboard by the number of cards in descending order
    leaderboard.sort(key=lambda x: x["cards"], reverse=True)
    
    with open(LEADERBOARD_FILE, "w") as file:
        dump(leaderboard, file, indent=4)
    
    print("Updating leaderboard...")
    for i in range(5):
        wait(1)
        print("...")
    wait(2)
    print("Leaderboard updated! 🏆")
    
    wait(3)
    print("Top 5 Scores on the Leaderboard:")
    wait(2)
    for i, entry in enumerate(leaderboard[:5], start=1):
        print(f"{i}. {entry['name']} - {entry['cards']} cards")

def fast_game() -> str:
    global deck_of_cards
    player1_name = player_1["name"]
    player2_name = player_2["name"]

    authorized_players.extend(load_authorized_players(AUTHORIZED_PLAYERS_FILE))
    if not check_players(player1_name, player2_name, authorized_players):
        print(f'Sorry, either "{player1_name}" or "{player2_name}", or both of you are not authorized to play 🚫')
        return

    deck_of_cards = create_deck(NUMBER_OF_CARDS_IN_DECK)
    
    while deck_of_cards:
        get_cards_from_deck(deck_of_cards, player_1, player_2)
        round_winner = calculate_winner(player_1, player_2)
        give_winner_cards(round_winner, player_1 if round_winner == player_2 else player_2)
    
    print(f'{player1_name.capitalize()} had these cards: {player_1["cards"]}')
    print(f'Overall, he had {len(player_1["cards"])} cards!')
    print('------------------------------------------------------------------------------------------------------')
    
    wait(2)
    print(f'{player2_name.capitalize()} had these cards: {player_2["cards"]}')
    print(f'Overall, he had {len(player_2["cards"])} cards!')
    print('------------------------------------------------------------------------------------------------------')
    
    # Determine the actual game winner based on the number of cards
    if len(player_1["cards"]) > len(player_2["cards"]):
        winner = player_1
        loser = player_2
    else:
        winner = player_2
        loser = player_1
    
    wait(3)
    print(f'{winner["name"].capitalize()} is the winner of this game!🏆🎖️')
    wait(2)
    print(f'Better luck next time, {loser["name"].capitalize()}!😆')
    wait(2)
    
    # Update leaderboard
    update_leaderboard(winner["name"], len(winner["cards"]))
    
    return winner["name"]

def normal_game() -> str:
    global deck_of_cards
    player1_name = player_1["name"]
    player2_name = player_2["name"]

    authorized_players.extend(load_authorized_players(AUTHORIZED_PLAYERS_FILE))
    if not check_players(player1_name, player2_name, authorized_players):
        print(f'Sorry, either {player1_name} or {player2_name}, or both of you are not authorized to play 🚫')
        return

    deck_of_cards = create_deck(NUMBER_OF_CARDS_IN_DECK)
    
    while deck_of_cards:
        get_cards_from_deck(deck_of_cards, player_1, player_2)
        player1_card = player_1["cards"][-1]
        player2_card = player_2["cards"][-1]
        
        round_winner = calculate_winner(player_1, player_2)
        
        print(f'{player1_name.capitalize()} draws card: {player1_card}')
        wait(2.5)
        print(f'{player2_name.capitalize()} draws card: {player2_card}')
        wait(2.5)
        print(f'{round_winner["name"].capitalize()} is the winner of this round.')
        print('---------------------------------------------------------------------------------------')
        
        give_winner_cards(round_winner, player_1 if round_winner == player_2 else player_2)
    
    wait(5)
    print(f'{player1_name.capitalize()} had these cards: {player_1["cards"]}')
    print(f'Overall, he had {len(player_1["cards"])} cards!')
    print('------------------------------------------------------------------------------------------------------')
    
    wait(3)
    print(f'{player2_name.capitalize()} had these cards: {player_2["cards"]}')
    print(f'Overall, he had {len(player_2["cards"])} cards!')
    print('------------------------------------------------------------------------------------------------------')
    
    # Determine the actual game winner based on the number of cards
    if len(player_1["cards"]) > len(player_2["cards"]):
        winner = player_1
        loser = player_2
    else:
        winner = player_2
        loser = player_1
    
    wait(3)
    print(f'{winner["name"].capitalize()} is the winner of this game!🏆🎖️')
    wait(2)
    print(f'Better luck next time, {loser["name"].capitalize()}!😆')
    wait(2)
    
    # Update leaderboard
    update_leaderboard(winner["name"], len(winner["cards"]))
    
    return winner["name"]

def main() -> None:
    game_chosen = input(f'Choose a game (normal/fast): ')
    if game_chosen == "normal".lower():
        winner = normal_game()
    elif game_chosen == "fast".lower():
        winner = fast_game()
    else:
        print(f'I dont think that "{game_chosen}" was one of the options mate...🤡')

if __name__ == "__main__":
    main()
