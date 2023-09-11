""" Utilities for handling letters in wordpy. """
import re

from enum import Enum
from colorama import Fore, Back

class LetterState(Enum):
    ''' The state of each letter in a user's guess '''
    NONE = 0
    WRONG = 1
    WRONG_PLACE = 2
    CORRECT = 3

def is_word_naively_valid(word):
    """
    Determines if the supplied word is valid for use in the game.
    The word must be 5 letters in length and contain only a-z | A-Z.
    The word does NOT have to be a valid dictionary word to pass this check
    Arguments:
        word: The word to check
    Returns: True for a valid word, False for an invalid one
    """
    if word is None:
        return False

    return re.fullmatch(r"[a-zA-Z]{5}", word) is not None


def blank_character(word, index):
    '''
    Returns a copy of the input string with the specified index blanked out
    If the index is out of range then the original string is returned
    Arguments:
        word: the word to blank a character from
        index: the index of the character to blank
    '''
    if index < 0 or index > len(word) - 1:
        return word

    return word[:index] + '_' + word[index+1:]


def score_word(word, answer):
    '''
    Determines the score/letter state for the supplied word and returns a tuple
    containing the word and the score/state for each letter
        e.g. ("ERASE", [LetterState.CORRECT,
                        LetterState.WRONG_PLACE,
                        LetterState.WRONG_PLACE,
                        LetterState.WRONG,
                        LetterState.WRONG_PLACE])
    Arguments:
        word: the word to score
        answer: the correct answer to score against
    Returns: Tuple containing the original word and an array with the
        score/state for each letter
    '''
    if not is_word_naively_valid(word):
        raise ValueError()

    score = [LetterState.WRONG] * 5

    # Check for fully correct letters first
    # We do correct letters in the wrong place in the second pass so that they
    # don't match against already fully correct letters
    for i in range(5):
        letter = word[i]
        if letter == answer[i]:
            score[i] = LetterState.CORRECT
            # We blank out any correctly guessed letters so that other guesses
            # of the same letter don't pick them up
            answer = blank_character(answer, i)

    # Do our second pass looking for letters in the wrong place now that we've
    # marked off the fully correct letters
    for i in range(5):
        # Skip already correct letters
        if score[i] == LetterState.CORRECT:
            continue

        letter = word[i]
        for j in range(5):
            if j != i and letter == answer[j]:
                score[i] = LetterState.WRONG_PLACE
                # We blank out any correctly guessed letters so that other
                # guesses of the same letter don't pick them up
                answer = blank_character(answer, j)
                break

    return (word, score)


def format_word(word, word_state):
    '''
    Gets the marked up string so that the provided word is laid out on a grid and letters are
    coloured according to their score/state.
    Correct letters get a green background, wrongly placed letters get a yellow background,
    wrong letters get a grey background, default is black.
    Arguments:
        word: the word to mark up
        word_state: the scores/state for each letter (a list of LetterState enum values)
    Returns: the marked up string ready for printing to the console
    '''
    if word is None or word_state is None or len(word) != len(word_state):
        raise ValueError(f"{word}, ({len(word)}) {word_state}, {len(word_state)}")

    letter_backgrounds = {
        LetterState.NONE: Back.BLACK,
        LetterState.WRONG: Back.LIGHTBLACK_EX,
        LetterState.WRONG_PLACE: Back.LIGHTYELLOW_EX,
        LetterState.CORRECT: Back.GREEN
    }

    # We always display words as all-caps
    word = word.upper()

    text = ""
    for i, letter in enumerate(word):
        text += Fore.WHITE + letter_backgrounds[word_state[i]] + "[" + letter + "]"

    return text
