""" Test methods for wordpy.py. """

from datetime import date
import pytest
import test_game_data
import test_game_config
import test_letter_utils
import wordpy

def test_create_game_config_from_args():
    """ Validate config generation from command arguments. """

    # Test for handling missing args
    args = None
    with pytest.raises(ValueError):
        game_data = wordpy.create_game_config_from_args(args)

    # test for defaults - expect today's date
    args = ["wordpy.py"]
    game_data = wordpy.create_game_config_from_args(args)
    assert game_data.date == date.today()
    assert game_data.word is None

    # test for forced date
    args = ["wordpy.py", "-date", "2001-01-31"]
    game_data = wordpy.create_game_config_from_args(args)
    assert game_data.date == date(2001, 1, 31)
    assert game_data.word is None

    # test for forced date arg but missing date
    args = ["wordpy.py", "-date"]
    with pytest.raises(ValueError):
        game_data = wordpy.create_game_config_from_args(args)

    # test for forced date arg but invalid date
    args = ["wordpy.py", "-date", "cat"]
    with pytest.raises(ValueError):
        game_data = wordpy.create_game_config_from_args(args)

    # test for forced date arg but invalid date
    args = ["wordpy.py", "-date", "01-01-2001"]
    with pytest.raises(ValueError):
        game_data = wordpy.create_game_config_from_args(args)

    # test for forced word
    args = ["wordpy.py", "-word", "RAISE"]
    game_data = wordpy.create_game_config_from_args(args)
    assert game_data.date == date.today()
    assert game_data.word == "RAISE"

    # test for forced word missing
    args = ["wordpy.py", "-word"]
    with pytest.raises(ValueError):
        game_data = wordpy.create_game_config_from_args(args)

    # test for forced word invalid
    args = ["wordpy.py", "-word", "A"]
    with pytest.raises(ValueError):
        game_data = wordpy.create_game_config_from_args(args)
    args = ["wordpy.py", "-word", "ABCDEFG"]
    with pytest.raises(ValueError):
        game_data = wordpy.create_game_config_from_args(args)
    args = ["wordpy.py", "-word", "ABCD£"]
    with pytest.raises(ValueError):
        game_data = wordpy.create_game_config_from_args(args)

    # test for forced date and forced word
    args = ["wordpy.py", "-date", "2024-11-15", "-word", "AGILE"]
    with pytest.raises(ValueError):
        game_data = wordpy.create_game_config_from_args(args)
    args = ["wordpy.py", "-word", "AGILE", "-date", "2024-11-15",]
    with pytest.raises(ValueError):
        game_data = wordpy.create_game_config_from_args(args)

    # test for bad inputs
    args = ["wordpy.py", "cat"]
    with pytest.raises(ValueError):
        game_data = wordpy.create_game_config_from_args(args)

    # test for bad inputs
    args = ["wordpy.py", "-date", "2023-12-05", "elephant"]
    with pytest.raises(ValueError):
        game_data = wordpy.create_game_config_from_args(args)

    # test for bad inputs
    args = ["wordpy.py", "garbage", "-date", "2023-12-05"]
    with pytest.raises(ValueError):
        game_data = wordpy.create_game_config_from_args(args)


def test_parse_date():
    """ Validate date param parsing. """

    # Good inputs
    args = ["2023-12-05"]
    assert wordpy.parse_date(args, 0) == date(2023, 12, 5)
    args = ["fish", "goat", "2019-03-04"]
    assert wordpy.parse_date(args, 2) == date(2019, 3, 4)

    # Bad index
    args = ["2023-12-05"]
    with pytest.raises(IndexError):
        wordpy.parse_date(args, -1)

    # Bad format
    args = ["12-01-1999"]
    with pytest.raises(ValueError):
        wordpy.parse_date(args, 0)

    # Bad input
    args = ["garbage"]
    with pytest.raises(ValueError):
        wordpy.parse_date(args, 0)


def test_parse_word():
    """ Validate word param parsing. """

    # Good inputs
    args = ["ARISE"]
    assert wordpy.parse_word(args, 0) == "ARISE"
    args = ["fishy", "goats", "2019-03-04"]
    assert wordpy.parse_word(args, 1) == "goats"

    # Bad index
    args = ["BRAIN"]
    with pytest.raises(IndexError):
        wordpy.parse_word(args, -1)

    # Too short
    args = ["HELP"]
    with pytest.raises(ValueError):
        wordpy.parse_word(args, 0)

    # Too long
    args = ["PLAINS"]
    with pytest.raises(ValueError):
        wordpy.parse_word(args, 0)

    # Bad characters
    args = ["BRA1N"]
    with pytest.raises(ValueError):
        wordpy.parse_word(args, 0)
    args = ["plan+"]
    with pytest.raises(ValueError):
        wordpy.parse_word(args, 0)


def test_print_usage(capfd):
    """ Validate that printing usage appears to work as expected. """

    TEST_STRING = "TEST ERROR"

    wordpy.print_usage(TEST_STRING)

    out, _ = capfd.readouterr()
    assert out.startswith(TEST_STRING)
    assert len(out) > len(TEST_STRING)


def test_all():
    """ Run all tests. """
    test_game_data.test_is_valid_word()
    test_game_config.test_GameConfig()
    test_letter_utils.test_is_word_naively_valid()
    test_letter_utils.test_blank_character()
    test_letter_utils.test_score_word()
