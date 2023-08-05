from Helping_funcs import _needs_number


class Game:
    """
    This class is the WOG's object which does
    necessary actions for each one of the games.
    """
    def __init__(self):
        """
        This runs every time a user calls the class
        and it necessary initializes variables.
        """
        self.game_difficulty = 0
        self.winning_status = False

    def set_difficulty(self):
        # This functioin asks for the game's difficulty.
        while (self.game_difficulty < 1) or (self.game_difficulty > 5):
            self.game_difficulty = input("Please choose game difficulty from 1 to 5: ")
            self.game_difficulty = _needs_number(self.game_difficulty)

    def win_or_lose(self):
        # This function prints whether the user won or lost the game.
        if self.winning_status:
            print("Well done, you are right!")
        else:
            print("Sorry, you didn't manage to win at this time.")

    def play(self):
        # This function is implemented in other classes.
        pass

    def start_game(self):
        # This function runs the game in the necessary order.
        self.set_difficulty()
        self.play()
        self.win_or_lose()
