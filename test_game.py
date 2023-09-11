import pytest
from game import Game
from gameconfig import GameConfig

def test_is_valid_word():
    game = Game(GameConfig())

    # Different case
    assert game.is_valid_word("RAISE") == True
    assert game.is_valid_word("raise") == True
    assert game.is_valid_word("rAiSe") == True

    # Valid words
    assert game.is_valid_word("DEISM") == True
    assert game.is_valid_word("GYPSY") == True
    assert game.is_valid_word("YEARS") == True

    # Too short
    assert game.is_valid_word("A") == False
    assert game.is_valid_word("HI") == False
    assert game.is_valid_word("BUT") == False
    assert game.is_valid_word("CALL") == False

    # Too long
    assert game.is_valid_word("PLIGHT") == False
    assert game.is_valid_word("QUADRANT") == False
    assert game.is_valid_word("PLIGHT") == False
    assert game.is_valid_word("PLIGHT") == False

    # Not in dictionary
    assert game.is_valid_word("PINCE") == False
    assert game.is_valid_word("BLANG") == False

    # Hyphentated
    assert game.is_valid_word("X-RAY") == False

    # Nonsense
    assert game.is_valid_word("$%@.,") == False

    # Accented
    assert game.is_valid_word("áéíóú") == False

