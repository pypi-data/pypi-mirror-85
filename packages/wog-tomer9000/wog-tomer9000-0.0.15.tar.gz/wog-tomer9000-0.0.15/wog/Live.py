from GuessGame import GuessGame
from MemoryGame import MemoryGame
from Helping_funcs import _needs_number
from CurrencyRouletteGame import CurrencyRouletteGame


def welcome(name):
    # Welcomes the user.
    return f"Hello {name} and welcome to the World of Games (WoG).\n" \
           f"Here you can find many cool games to play."


def load_game():
    # This func loads the game that the user chooses to play.
    game_to_play = input("Please choose a game to play:\n"
                         "\t1. Memory Game - a sequence of numbers will "
                         "appear for 1 second and you have to guess it back\n"
                         "\t2. Guess Game - guess a number and see "
                         "if you chose like the computer\n"
                         "\t3. Currency Roulette - try and guess the value "
                         "of a random amount of USD in ILS ")
    while not (game_to_play == "1" or game_to_play == "2" or game_to_play == "3"):
        game_to_play = input("Please choose the game to play, 1,2, or 3 ")
    dict_game = {"1": MemoryGame(), "2": GuessGame(), "3": CurrencyRouletteGame()}
    game_chosen = dict_game[game_to_play]
    game_chosen.start_game()
