from datetime import date

class GameConfig:
    def __init__(self, forceddate=None, word=None, random=False, infinite=False):

        self._date = forceddate
        self._word = word
        self._random = random or infinite
        self._infinite = infinite

        self._validate()

        if self.date == None: self._date = date.today()

    @property
    def date(self):
        return self._date

    @property
    def word(self):
        return self._word

    @property
    def random(self):
        return self._random

    @property
    def infinite(self):
        return self._infinite

    def _validate(self):
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
