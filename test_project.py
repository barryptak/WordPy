import test_game
import test_gameconfig
import test_letterutils
import project
import pytest

from datetime import date

def test_create_game_data_from_args():
    # Test for handling missing args
    args = None
    with pytest.raises(ValueError):
        game_data = project.create_game_data_from_args(args)

    # test for defaults - expect today's date
    args = ["project.py"]
    game_data = project.create_game_data_from_args(args)
    assert game_data.date == date.today()
    assert game_data.word == None

    # test for forced date
    args = ["project.py", "-date", "2001-01-31"]
    game_data = project.create_game_data_from_args(args)
    assert game_data.date == date(2001, 1, 31)
    assert game_data.word == None

    # test for forced date arg but missing date
    args = ["project.py", "-date"]
    with pytest.raises(ValueError):
        game_data = project.create_game_data_from_args(args)

    # test for forced date arg but invalid date
    args = ["project.py", "-date", "cat"]
    with pytest.raises(ValueError):
        game_data = project.create_game_data_from_args(args)

    # test for forced date arg but invalid date
    args = ["project.py", "-date", "01-01-2001"]
    with pytest.raises(ValueError):
        game_data = project.create_game_data_from_args(args)

    # test for forced word
    args = ["project.py", "-word", "RAISE"]
    game_data = project.create_game_data_from_args(args)
    assert game_data.date == date.today()
    assert game_data.word == "RAISE"

    # test for forced word missing
    args = ["project.py", "-word"]
    with pytest.raises(ValueError):
        game_data = project.create_game_data_from_args(args)

    # test for forced word invalid
    args = ["project.py", "-word", "A"]
    with pytest.raises(ValueError):
        game_data = project.create_game_data_from_args(args)
    args = ["project.py", "-word", "ABCDEFG"]
    with pytest.raises(ValueError):
        game_data = project.create_game_data_from_args(args)
    args = ["project.py", "-word", "ABCD£"]
    with pytest.raises(ValueError):
        game_data = project.create_game_data_from_args(args)

    # test for forced date and forced word
    args = ["project.py", "-date", "2024-11-15", "-word", "AGILE"]
    with pytest.raises(ValueError):
        game_data = project.create_game_data_from_args(args)
    args = ["project.py", "-word", "AGILE", "-date", "2024-11-15",]
    with pytest.raises(ValueError):
        game_data = project.create_game_data_from_args(args)

    # test for bad inputs
    args = ["project.py", "cat"]
    with pytest.raises(ValueError):
        game_data = project.create_game_data_from_args(args)

    # test for bad inputs
    args = ["project.py", "-date", "2023-12-05", "elephant"]
    with pytest.raises(ValueError):
        game_data = project.create_game_data_from_args(args)

    # test for bad inputs
    args = ["project.py", "garbage", "-date", "2023-12-05"]
    with pytest.raises(ValueError):
        game_data = project.create_game_data_from_args(args)


def test_parse_date():
    # Good inputs
    args = ["2023-12-05"]
    assert project.parse_date(args, 0) == date(2023, 12, 5)
    args = ["fish", "goat", "2019-03-04"]
    assert project.parse_date(args, 2) == date(2019, 3, 4)

    # Bad index
    args = ["2023-12-05"]
    with pytest.raises(IndexError):
        project.parse_date(args, -1)

    # Bad format
    args = ["12-01-1999"]
    with pytest.raises(ValueError):
        project.parse_date(args, 0)

    # Bad input
    args = ["garbage"]
    with pytest.raises(ValueError):
        project.parse_date(args, 0)


def test_parse_word():
    # Good inputs
    args = ["ARISE"]
    assert project.parse_word(args, 0) == "ARISE"
    args = ["fishy", "goats", "2019-03-04"]
    assert project.parse_word(args, 1) == "goats"

    # Bad index
    args = ["BRAIN"]
    with pytest.raises(IndexError):
        project.parse_word(args, -1)

    # Too short
    args = ["HELP"]
    with pytest.raises(ValueError):
        project.parse_word(args, 0)

    # Too long
    args = ["PLAINS"]
    with pytest.raises(ValueError):
        project.parse_word(args, 0)

    # Bad characters
    args = ["BRA1N"]
    with pytest.raises(ValueError):
        project.parse_word(args, 0)
    args = ["plan+"]
    with pytest.raises(ValueError):
        project.parse_word(args, 0)


def test_print_usage(capfd):

    TEST_STRING = "TEST ERROR"

    project.print_usage(TEST_STRING)

    out, err = capfd.readouterr()
    assert out.startswith(TEST_STRING)
    assert len(out) > len(TEST_STRING)


def test_all():
    test_game.test_is_valid_word()
    test_gameconfig.test_GameConfig()
    test_letterutils.test_is_word_naively_valid()
    test_letterutils.test_blank_character()
    test_letterutils.test_score_word()
