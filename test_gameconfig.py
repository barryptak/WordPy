import pytest

from datetime import date
from gameconfig import GameConfig

def test_GameConfig():

    # Bad mixing of params
    with pytest.raises(ValueError):
        data = GameConfig(word = "WORD", infinite = True)

    with pytest.raises(ValueError):
        data = GameConfig(word = "WORD", random = True)

    with pytest.raises(ValueError):
        data = GameConfig(forceddate = date.today(), infinite = True)

    with pytest.raises(ValueError):
        data = GameConfig(forceddate = date.today(), random = True)

    with pytest.raises(ValueError):
        data = GameConfig(word = "WORD", forceddate = date.today())

    with pytest.raises(ValueError):
        data = GameConfig(forceddate = date(1969, 12, 31))

    # Good data
    data = GameConfig(random = True)
    assert data.date == date.today()
    assert data.word == None
    assert data.random == True
    assert data.infinite == False

    data = GameConfig(infinite = True)
    assert data.date == date.today()
    assert data.word == None
    assert data.random == True # Infinite implies random
    assert data.infinite == True

    data = GameConfig(forceddate = date(1999, 1, 1))
    assert data.date == date(1999, 1, 1)
    assert data.word == None
    assert data.random == False
    assert data.infinite == False

    data = GameConfig(word = "TESTY")
    assert data.date == date.today()
    assert data.word == "TESTY"
    assert data.random == False
    assert data.infinite == False

