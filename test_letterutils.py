import pytest

from letterutils import is_word_naively_valid, blank_character, score_word, LetterState

def test_is_word_naively_valid():

    # Test some 'valid' words
    assert is_word_naively_valid("RAISE") == True
    assert is_word_naively_valid("COUCH") == True
    assert is_word_naively_valid("ABCDE") == True
    assert is_word_naively_valid("ZZZZZ") == True

    # Test missing
    assert is_word_naively_valid(None) == False

    # Test too short
    assert is_word_naively_valid("A") == False
    assert is_word_naively_valid("AB") == False
    assert is_word_naively_valid("ABC") == False
    assert is_word_naively_valid("ABCD") == False

    # Test too long
    assert is_word_naively_valid("ABCDEF") == False
    assert is_word_naively_valid("ABCDEFGH") == False
    assert is_word_naively_valid("ABCDEFGHIJKLMNOPQRSTUVWXYZ") == False

    # Test invalid chars
    assert is_word_naively_valid("_ABCD") == False
    assert is_word_naively_valid("A BCD") == False
    assert is_word_naively_valid("AB+CD") == False
    assert is_word_naively_valid("ABC-D") == False
    assert is_word_naively_valid("ABCD@") == False
    assert is_word_naively_valid("áéíóú") == False


def test_blank_character():
    assert blank_character("ABCDEF", -1) == "ABCDEF"
    assert blank_character("ABCDEF", 0) == "_BCDEF"
    assert blank_character("ABCDEF", 2) == "AB_DEF"
    assert blank_character("ABCDEF", 5) == "ABCDE_"
    assert blank_character("ABCDEF", 6) == "ABCDEF"
    assert blank_character("ABCDEF", 7) == "ABCDEF"


def test_score_word():
    answer = "EAGER"

    score = score_word("POUND", answer)
    assert score[1] == [LetterState.WRONG, LetterState.WRONG, LetterState.WRONG, LetterState.WRONG, LetterState.WRONG]

    score = score_word("ARISE", answer)
    assert score[1] == [LetterState.WRONG_PLACE, LetterState.WRONG_PLACE, LetterState.WRONG, LetterState.WRONG, LetterState.WRONG_PLACE]

    score = score_word("ERASE", answer)
    assert score[1] == [LetterState.CORRECT, LetterState.WRONG_PLACE, LetterState.WRONG_PLACE, LetterState.WRONG, LetterState.WRONG_PLACE]

    score = score_word("EAGER", answer)
    assert score[1] == [LetterState.CORRECT, LetterState.CORRECT, LetterState.CORRECT, LetterState.CORRECT, LetterState.CORRECT]

    ## Test an invalid word
    with pytest.raises(ValueError):
        score_word("GARBAGE", answer)

    ## Test an invalid word
    with pytest.raises(ValueError):
        score_word("&*@$%", answer)