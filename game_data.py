""" Wordle game data (lists of valid words). """

import json
from json import JSONDecodeError

import letter_utils

class GameData:
    """ GameData class holds all of the valid words for the game. """

    def __init__(self):
        self._load_word_lists()


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

        file_exceptions = (
            FileNotFoundError,
            PermissionError,
            FileExistsError,
            IsADirectoryError,
            TypeError,
            JSONDecodeError)

        try:
            with open("./data/answers.json", encoding="utf-8") as answers_file:
                self._answers = json.load(answers_file)
            with open("./data/valid_words.json", encoding="utf-8") as words_file:
                self._words = json.load(words_file)
        except file_exceptions:
            return False

        return True


    def is_valid_word(self, word):
        '''
        Is the specified word a valid dictionary word?
        Arguments:
            word: The word to validate
        Returns: True if the word is valid, False if it is not
        '''

        if not letter_utils.is_word_naively_valid(word):
            return False

        return word.lower() in self.valid_words
