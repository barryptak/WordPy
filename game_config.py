"""
The game config holds parameters for controlling the behaviour of the current run of the game.
"""

from datetime import date

class GameConfig:
    """ Game config class describing current game parameters. """
    def __init__(self, forced_date=None, word=None, random=False, infinite=False):

        self._date = forced_date
        self._word = word
        self._random = random or infinite
        self._infinite = infinite

        self._validate()

        if self.date is None:
            self._date = date.today()

    @property
    def date(self):
        """ Date to use for picking game's solution word. """
        return self._date

    @property
    def word(self):
        """ Explicitly set solution word. """
        return self._word

    @property
    def random(self):
        """ Solution word should be picked at random. """
        return self._random

    @property
    def infinite(self):
        """ Keep playing over and over again forever. """
        return self._infinite

    def _validate(self):
        """ Checks that the provided configuration options are valid. """
        if self.infinite and self.word:
            raise ValueError("infinite and word are incompatible")
        if self.infinite and self.date:
            raise ValueError("infinite and date are incompatible")
        if self.random and self.word:
            raise ValueError("random and word are incompatible")
        if self.random and self.date:
            raise ValueError("random and date are incompatible")
        if self.word and self.date:
            raise ValueError("word and date are incompatible")
        if self.date and self.date < date(1970, 1, 1):
            raise ValueError("date must be 1970-01-01 or later")
