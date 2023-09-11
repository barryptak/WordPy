""" Unit tests for letter_utils. """

import pytest
from letter_utils import is_word_naively_valid, blank_character, score_word, LetterState

def test_is_word_naively_valid():
    """ Test naive word validity checking """

    # Test some 'valid' words
    assert is_word_naively_valid("RAISE")
    assert is_word_naively_valid("COUCH")
    assert is_word_naively_valid("ABCDE")
    assert is_word_naively_valid("ZZZZZ")

    # Test missing
    assert not is_word_naively_valid(None)

    # Test too short
    assert not is_word_naively_valid("A")
    assert not is_word_naively_valid("AB")
    assert not is_word_naively_valid("ABC")
    assert not is_word_naively_valid("ABCD")

    # Test too long
    assert not is_word_naively_valid("ABCDEF")
    assert not is_word_naively_valid("ABCDEFGH")
    assert not is_word_naively_valid("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    # Test invalid chars
    assert not is_word_naively_valid("_ABCD")
    assert not is_word_naively_valid("A BCD")
    assert not is_word_naively_valid("AB+CD")
    assert not is_word_naively_valid("ABC-D")
    assert not is_word_naively_valid("ABCD@")
    assert not is_word_naively_valid("áéíóú")


def test_blank_character():
    """ Test that blanking of specific characters works correctly. """
    assert blank_character("ABCDEF", -1) == "ABCDEF"
    assert blank_character("ABCDEF", 0) == "_BCDEF"
    assert blank_character("ABCDEF", 2) == "AB_DEF"
    assert blank_character("ABCDEF", 5) == "ABCDE_"
    assert blank_character("ABCDEF", 6) == "ABCDEF"
    assert blank_character("ABCDEF", 7) == "ABCDEF"


def test_score_word():
    """ Test scoring of words via score_word. """
    answer = "EAGER"

    score = score_word("POUND", answer)
    assert score[1] == [LetterState.WRONG] * 5

    score = score_word("ARISE", answer)
    assert score[1] == [LetterState.WRONG_PLACE,
                        LetterState.WRONG_PLACE,
                        LetterState.WRONG,
                        LetterState.WRONG,
                        LetterState.WRONG_PLACE]

    score = score_word("ERASE", answer)
    assert score[1] == [LetterState.CORRECT,
                        LetterState.WRONG_PLACE,
                        LetterState.WRONG_PLACE,
                        LetterState.WRONG,
                        LetterState.WRONG_PLACE]

    score = score_word("EAGER", answer)
    assert score[1] == [LetterState.CORRECT] * 5

    ## Test an invalid word
    with pytest.raises(ValueError):
        score_word("GARBAGE", answer)

    ## Test an invalid word
    with pytest.raises(ValueError):
        score_word("&*@$%", answer)
