""" Core game class for WordPy. """

import os
import random
import string
from datetime import date
from enum import Enum

import colorama
from colorama import Fore, Back, Style

import letter_utils
from letter_utils import LetterState

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
        from game_config import GameConfig
        from game import Game

        config = GameConfig() # There are optional parameters available here
        game = Game(config)
        game.run()
    '''

    def __init__(self, config, data):
        if config is None:
            raise ValueError("Config missing")
        if data is None:
            raise ValueError("Data missing")

        self._state = GameState.INTRO
        self._config = config
        self._data = data

        self._start()

        # Initialise colorama
        colorama.init(autoreset=True)


    def _pick_answer(self):
        '''
        Picks a new answer for the game.
        If the user forced a word via the command-line then that word will be
        used. Otherwise we use today's date (or the command-line forced date) to
        pick a random answer from the answers list.
        Returns: the answer for this run of the game
        '''
        if self._config.word is not None:
            return self._config.word.lower()
        else:
            # If random is True then use the default seed of the current system time.
            # If it's False then let's seed using a date
            if not self._config.random:
                # Pick a random answer based on today's (or the forced) date
                # This isn't what Wordle does ~(it just iterates through an
                # unordered list), and we can end up with
                # the same answer on multiple days, but it's fine for now.
                # It also prevents someone trivially looking up the next word in
                # the data file and cheating that way.
                days_since_epoch = self._config.date - date(1970, 1, 1)
                random.seed(days_since_epoch.days)

            num_answers = len(self._data.possible_answers)
            return self._data.possible_answers[random.randrange(0, num_answers)]


    def _start(self):
        '''
        Starts a new instance of the game and (re)initialises any per-game state
        '''
        self._answer = self._pick_answer()
        self._guess_number = 1
        self._won = False
        empty_guess = ("     ", [LetterState.NONE] * 5)
        self._guesses = [empty_guess] * 6

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

            if self._prompt_for_input():
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
            print("After each guess, the color of the tiles will change to show" +
                  "how close your guess was to the word.")
            print("------------------------------")
            print("\nExamples")
            print("\n" + letter_utils.format_word("WEARY",
                                                 [LetterState.CORRECT,
                                                  LetterState.NONE,
                                                  LetterState.NONE,
                                                  LetterState.NONE,
                                                  LetterState.NONE]))
            print("The letter W is in the word and in the correct spot.")
            print("\n" + letter_utils.format_word("PILLS",
                                                 [LetterState.NONE,
                                                  LetterState.WRONG_PLACE,
                                                  LetterState.NONE,
                                                  LetterState.NONE,
                                                  LetterState.NONE]))
            print("The letter I is in the word but in the wrong spot.")
            print("\n" + letter_utils.format_word("VAGUE", [LetterState.NONE] * 5))
            print("The letter U is not in the word in any spot.")
            print("\n------------------------------")
            print("A new WORDPy will be available each day")
            print("------------------------------")

            if self._prompt_for_input():
                break


    def _draw_grid(self):
        ''' Draws the current game grid to the console '''

        for guess in self._guesses:
            print(letter_utils.format_word(guess[0], guess[1]))

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
            for i, letter in enumerate(guess_word):
            #for i in range(len(guess_word)):
                letter = guess_word[i]

                if letter not in string.ascii_uppercase:
                    continue

                state = guess_state[i]
                # If we've already recorded this letter then we only want to update it if this is a
                # correct match (as there may have been a partial match already).
                # We don't want to overwrite correct matches with partial ones!
                if used_letters[letter] == LetterState.NONE or state == LetterState.CORRECT:
                    used_letters[letter] = state

        print(letter_utils.format_word(string.ascii_uppercase, list(used_letters.values())))


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
            if self._data.is_valid_word(word):

                guess = letter_utils.score_word(word, self._answer)
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
                print("The correct answer was " +
                      letter_utils.format_word(self._answer, [LetterState.CORRECT] * 5))

            if self._config.infinite:
                if self._prompt_for_input():
                    break
            else:
                self._change_state(GameState.QUIT)
                break
