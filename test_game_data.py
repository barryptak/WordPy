""" Unit tests for GameData class. """

from game_data import GameData

def test_is_valid_word():
    """ Test word validation. """
    data = GameData()

    # Different case
    assert data.is_valid_word("RAISE")
    assert data.is_valid_word("raise")
    assert data.is_valid_word("rAiSe")

    # Valid words
    assert data.is_valid_word("DEISM")
    assert data.is_valid_word("GYPSY")
    assert data.is_valid_word("YEARS")

    # Too short
    assert not data.is_valid_word("A")
    assert not data.is_valid_word("HI")
    assert not data.is_valid_word("BUT")
    assert not data.is_valid_word("CALL")

    # Too long
    assert not data.is_valid_word("PLIGHT")
    assert not data.is_valid_word("QUADRANT")
    assert not data.is_valid_word("PLIGHT")
    assert not data.is_valid_word("PLIGHT")

    # Not in dictionary
    assert not data.is_valid_word("STOOB")
    assert not data.is_valid_word("BLANG")

    # Hyphenated
    assert not data.is_valid_word("X-RAY")

    # Nonsense
    assert not data.is_valid_word("$%@.,")

    # Accented
    assert not data.is_valid_word("áéíóú")
