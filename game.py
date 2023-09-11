import colorama
import json
import letterutils
import os
import random
import string

from colorama import Fore, Back, Style
from datetime import date
from enum import Enum
from letterutils import LetterState

class GameState(Enum):
    ''' Valid game states '''
    INTRO = 0
    HELP = 1
    GUESSING = 2
    WON = 3
    LOST = 4
    QUIT = 5

class Game:
    '''
    Our main game class. Contains a state machine for managing the game state and progression.
    Usage:
        from gamedata import GameData
        from game import Game

        config = GameData() # There are optional parameters available here
        game = Game(config)
        game.run()
    '''

    def __init__(self, config):
        if config == None:
            raise ValueError("Config missing")

        self._state = GameState.INTRO
        self._config = config
        self._words = None
        self._answers = None

        if not self._load_word_lists():
            raise ValueError("Error loading word lists")

        self._start()

        # Initialise colorama
        colorama.init(autoreset=True)


    @property
    def valid_words(self):
        ''' List of valid words '''
        return self._words["words"]


    @property
    def possible_answers(self):
        ''' List of all possible answers '''
        return self._answers["words"]


    def _load_word_lists(self):
        '''
        Loads the json files containing the valid words and valid answers
        Returns: True for success, False for failure
        '''

        try:
            with open("./data/answers.json") as answers_file:
                self._answers = json.load(answers_file)
            with open("./data/valid_words.json") as words_file:
                self._words = json.load(words_file)
        except Exception as ex:
            return False

        return True


    def is_valid_word(self, word):
        '''
        Is the specified word a valid dictionary word?
        Arguments:
            word: The word to validate
        Returns: True if the word is valid, False if it is not
        '''

        if letterutils.is_word_naively_valid(word) == False:
            return False

        return word.lower() in self.valid_words


    def _pick_answer(self):
        '''
        Picks a new answer for the game.
        If the user forced a word via the command-line then that word will be used.
        Otherwise we use today's date (or the command-line forced date) to pick a random answer from the answers list.
        Returns: the answer for this run of the game
        '''
        if self._config.word != None:
            return self._config.word.lower()
        else:
            # If random is True then use the default seed of the current system time.
            # If it's False then let's seed using a date
            if self._config.random == False:
                # Pick a random answer based on today's (or the forced) date
                # This isn't what Wordle does ~(it just iterates through an unordered list), and we can end up with
                # the same answer on multiple days, but it's fine for now.
                # It also prevents someone trivially looking up the next word in the data file and cheating that way.
                days_since_epoch = self._config.date - date(1970, 1, 1)
                days_since_epoch.days
                random.seed(days_since_epoch.days)

            return self.possible_answers[random.randrange(0, len(self.possible_answers))]


    def _start(self):
        '''
        Starts a new instance of the game and (re)initialises any per-game state
        '''
        self._answer = self._pick_answer()
        self._guess_number = 1
        self._won = False
        self._guesses = [
            ("     ", [LetterState.NONE, LetterState.NONE,LetterState.NONE,LetterState.NONE,LetterState.NONE]),
            ("     ", [LetterState.NONE, LetterState.NONE,LetterState.NONE,LetterState.NONE,LetterState.NONE]),
            ("     ", [LetterState.NONE, LetterState.NONE,LetterState.NONE,LetterState.NONE,LetterState.NONE]),
            ("     ", [LetterState.NONE, LetterState.NONE,LetterState.NONE,LetterState.NONE,LetterState.NONE]),
            ("     ", [LetterState.NONE, LetterState.NONE,LetterState.NONE,LetterState.NONE,LetterState.NONE]),
            ("     ", [LetterState.NONE, LetterState.NONE,LetterState.NONE,LetterState.NONE,LetterState.NONE])]


    def run(self):
        '''
        Runs the main game state machine. Exists when game is finished / user quits.
        '''
        while True:
            match self._state:
                case GameState.INTRO:
                    self._show_intro()

                case GameState.HELP:
                    self._show_help()

                case GameState.GUESSING:
                    self._show_game()

                case GameState.WON:
                    self._show_end(True)

                case GameState.LOST:
                    self._show_end(False)

                case GameState.QUIT:
                    print("")
                    break


    def _change_state(self, new_state):
        '''
        Attempt to change the current state of the game.
        Arguments:
            new_state: The state to change to
        Raises: RuntimeError if the state change is not valid
        '''

        # Handle any state transition (entry/exit) logic that we need
        if new_state == GameState.GUESSING:
            self._start()

        self._state = new_state


    def _print_logo(self):
        ''' Prints out the game logo to the console'''

        print(  Fore.BLACK + Back.GREEN +
                    "[W]" + Back.BLACK + " " + Back.WHITE +
                    "[O]" + Back.BLACK + " " + Back.WHITE +
                    "[R]" + Back.BLACK + " " + Back.WHITE +
                    "[D]" + Back.BLACK + " " + Back.YELLOW +
                    "[Py]")

    def _prompt_for_input(self):
        ''' Reusable user prompt for moving around the game states '''

        print("\nPress [enter] to play")
        print("\nType 'help' for how to play")
        print("Type 'quit' or press [Ctrl + D] to quit")
        try:
            command = input()
        except EOFError:
            self._change_state(GameState.QUIT)
            return True

        if command == "help":
            self._change_state(GameState.HELP)
            return True
        elif command == "quit":
            self._change_state(GameState.QUIT)
            return True
        elif command == "":
            self._change_state(GameState.GUESSING)
            return True
        else:
            return False

    def _show_intro(self):
        ''' Prints the intro information to the console '''

        while True:
            os.system("clear")
            self._print_logo()

            if self._prompt_for_input() == True:
                break

    def _show_help(self):
        ''' Prints the help information to the console '''

        while True:
            os.system("clear")
            self._print_logo()

            print(Style.BRIGHT + "\nHOW TO PLAY")
            print("------------------------------")
            print("Guess the WORDPy in 6 tries")
            print("Each guess must be a valid 5-letter word. Hit the enter button to submit.")
            print("After each guess, the color of the tiles will change to show how close your guess was to the word.")
            print("------------------------------")
            print("\nExamples")
            print("\n" + letterutils.format_word("WEARY", [LetterState.CORRECT, LetterState.NONE,LetterState.NONE,LetterState.NONE,LetterState.NONE]))
            print("The letter W is in the word and in the correct spot.")
            print("\n" + letterutils.format_word("PILLS", [LetterState.NONE, LetterState.WRONG_PLACE,LetterState.NONE,LetterState.NONE,LetterState.NONE]))
            print("The letter I is in the word but in the wrong spot.")
            print("\n" + letterutils.format_word("VAGUE", [LetterState.NONE, LetterState.NONE,LetterState.NONE,LetterState.WRONG,LetterState.NONE]))
            print("The letter U is not in the word in any spot.")
            print("\n------------------------------")
            print("A new WORDPy will be available each day")
            print("------------------------------")

            if self._prompt_for_input() == True:
                break


    def _draw_grid(self):
        ''' Draws the current game grid to the console '''

        for guess in self._guesses:
            print(letterutils.format_word(guess[0], guess[1]))

    def _draw_used_letters(self):
        '''
        Draws all of the letters of the alphabet out indicating the known state of each
        (right place, wrong place, not in word, not used)
        This is useful as a reminder for the user as it can be quite hard without this reference
        '''

        print("Used letters: ", end="")

        # Create a dictionary of all letters
        used_letters = {}
        for letter in string.ascii_uppercase:
            used_letters[letter] = LetterState.NONE

        # Iterate over the player's guesses and determine the overall state of each letter
        # Correct overrides wrong place, which overrides wrong, which overrides none.
        # The value of some of these (wrong place vs correct)
        for guess in self._guesses:
            guess_word = guess[0].upper()
            guess_state = guess[1]
            for i in range(len(guess_word)):
                letter = guess_word[i]

                if letter not in string.ascii_uppercase:
                    continue

                state = guess_state[i]
                # If we've already recorded this letter then we only want to update it if this is a
                # correct match (as there may have been a partial match already).
                # We don't want to overwrite correct matches with partial ones!
                if used_letters[letter] == LetterState.NONE or state == LetterState.CORRECT:
                    used_letters[letter] = state

        print(letterutils.format_word(string.ascii_uppercase, list(used_letters.values())))


    def _show_game(self):
        ''' Draws the current game state to the console and prompts the user for input '''

        # Draw 5 x 6 grid of guesses
        os.system("clear")
        self._draw_grid()
        print("")
        self._draw_used_letters()
        print("")

        # Prompt user for guess
        word = ""
        while True:
            try:
                word = input("Enter guess: ").lower()
            except EOFError:
                self._change_state(GameState.QUIT)
                break

            # Validate word
            if self.is_valid_word(word):

                guess = letterutils.score_word(word, self._answer)
                self._guesses[self._guess_number - 1] = guess
                self._guess_number += 1

                # Have we guessed all the letters correctly?
                if all(item == LetterState.CORRECT for item in guess[1]):
                    # We've won!!!
                    self._change_state(GameState.WON)
                elif self._guess_number > 6:
                    # We've lost!!!
                    self._change_state(GameState.LOST)
                break
            else:
                print("Invalid word. Try again...")


    def _show_end(self, won):
        '''
        Draws the end of game screen
        Arguments:
            won: whether the player won the game or not
        '''

        while True:
            os.system("clear")
            self._draw_grid()
            if won:
                print("\nWell done!")
            else:
                print("\nSorry, you lost...")
                print(f"The correct answer was " + letterutils.format_word(self._answer, [LetterState.CORRECT, LetterState.CORRECT, LetterState.CORRECT, LetterState.CORRECT, LetterState.CORRECT]))

            if self._config.infinite == True:
                if self._prompt_for_input() == True:
                    break
            else:
                self._change_state(GameState.QUIT)
                break



