""" Unit tests for GameConfig class. """

from datetime import date
import pytest
from game_config import GameConfig

def test_GameConfig():
    """ Test GameConfig generation via various options. """

    # Bad mixing of params
    with pytest.raises(ValueError):
        data = GameConfig(word = "WORD", infinite = True)

    with pytest.raises(ValueError):
        data = GameConfig(word = "WORD", random = True)

    with pytest.raises(ValueError):
        data = GameConfig(forced_date = date.today(), infinite = True)

    with pytest.raises(ValueError):
        data = GameConfig(forced_date = date.today(), random = True)

    with pytest.raises(ValueError):
        data = GameConfig(word = "WORD", forced_date = date.today())

    with pytest.raises(ValueError):
        data = GameConfig(forced_date = date(1969, 12, 31))

    # Good data
    data = GameConfig(random = True)
    assert data.date == date.today()
    assert data.word is None
    assert data.random
    assert not data.infinite

    data = GameConfig(infinite = True)
    assert data.date == date.today()
    assert data.word is None
    assert not data.random # Infinite implies random
    assert not data.infinite

    data = GameConfig(forced_date = date(1999, 1, 1))
    assert data.date == date(1999, 1, 1)
    assert data.word is None
    assert not data.random
    assert not data.infinite

    data = GameConfig(word = "TESTY")
    assert data.date == date.today()
    assert data.word == "TESTY"
    assert not data.random
    assert not data.infinite
