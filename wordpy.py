import letterutils
import sys

from gameconfig import GameConfig
from game import Game
from datetime import date

def main():
    # Read in the command line options and create the matching game data
    try:
        game_data = create_game_data_from_args(sys.argv)
    except ValueError as e:
        print_usage(e)
        sys.exit()

    # Now create our Game object and run it
    game = Game(game_data)
    try:
        game.run()
    # Capture Ctrl + C and quit gracefully
    except KeyboardInterrupt:
        sys.exit()

def create_game_data_from_args(argv):
    """
    Parses the set of command line arguments and creates the appropriate GameData object for it.
    Arguments:
        argv: the sys.argv parameters that this program was launched with
    Raises:
        ValueError: on invalid input
    """

    if argv == None:
        raise ValueError("No arguments passed in")

    num_args = len(argv)
    current_arg = 1
    game_date = None
    word = None
    infinite = False
    random = False

    # Iterate through the provided arguments determining their meaning and performing any further validation
    while current_arg < num_args:
        match argv[current_arg]:

            case "-?" | "-help":
                # Ok, it's a bit weird raising an error for this, but we don't want to run normally and
                # throwing here will result in the usage being printed out as desired.
                raise ValueError()

            # The -date argument must be followed by a date in ISO format (YYYY-MM-DD)
            case "-date":
                # Need to increment current_arg to that we read the next argument
                current_arg += 1
                game_date = parse_date(argv, current_arg)

            case "-infinite":
                infinite = True

            case "-random":
                random = True

            # The -word argument must be followed by a 5 letter (a-zA-Z) word
            case "-word":
                # Need to increment current_arg to that we read the next argument
                current_arg += 1
                word = parse_word(argv, current_arg)

            # Unexpected arguments mean that we should reject everything
            case _:
                 raise ValueError(f"Unexpected argument found: {argv[current_arg]}")

        # Move on to the next argument
        current_arg += 1

    return GameConfig(forceddate=game_date, word=word, infinite=infinite, random=random)


def parse_date(argv, index):
    """
    Parse the date parameter from the command-line args and create a valid date object from it
    Input date is expected to be in ISO format (YYY-MM-DD)
    Arguments:
        argv: the command-line parameters passed to the program
        index: the index to read the date argument from
    Returns: the created date object
    Raises:
        IndexError: when negative index is supplied
        ValueError: when date argument is missing, or when arguement is not in the expected ISO format
    """
    if index < 0:
        raise IndexError(index)

    # If there's no argument after this one then the date is missing and these arguments are bad
    if index >= len(argv):
        raise ValueError(f"Missing date argument")

    # Try to read the next argument as an ISO format date
    try:
        dateArg = argv[index]
        return date.fromisoformat(dateArg)
    except ValueError:
        raise ValueError(f"Invalid date argument: {dateArg}")


def parse_word(argv, index):
    """
    Parse the word parameter from the command-line args and return it
    Input word is expected to be 5-letters all in the range of a-Z|A-Z
    Arguments:
        argv: the command-line parameters passed to the program
        index: the index to read the word argument from
    Returns: the created date object
    Raises:
        IndexError: when negative index is supplied
        ValueError: when word argument is missing, or when arguement is invalid (wrong length or characters)
    """
    if index < 0:
        raise IndexError(index)

    # If there's no argument after this one then the word is missing and these arguments are bad
    if index >= len(argv):
        raise ValueError(f"Missing word argument")

    # Next check that the word is the correct length and character set
    wordArg = argv[index]
    if letterutils.is_word_naively_valid(wordArg) == False:
        raise ValueError(f"Invalid word argument: {wordArg}")
    return wordArg


def print_usage(errorStr = None):
    """
    Prints out the valid command-line usage for this program.
    Arguments:
        [optional] errorStr: An error string to print out before the normal usage instructions
    """
    if str and len(str(errorStr)) > 0: print(errorStr)
    print(  "usage project.py [option]\n" +
            "  options:\n" +
            "   -date <date>      : forces the game to use the word from the specified date\n" +
            "                       The date must be provided in ISO format: YYYY-MM-DD\n" +
            "                       Defaults to today's date\n" +
            "                       Incompatible with -infinite, -random or -word\n" +
            "   -help, -?         : displays this usage help\n" +
            "   -infinite         : puts the game into infinite looping mode where you can play\n" +
            "                       continuously (implies -random)\n" +
            "                       Incompatible with -date or -word\n" +
            "                       Defaults to False\n" +
            "   -random           : forces the game to use a random word\n" +
            "                       Incompatible with -date or -word\n" +
            "                       Defaults to False\n" +
            "   -word <word>      : forces the use of the specified 5-letter word\n" +
            "                       Incompatible with -date, -infinite or -random")


if __name__ == "__main__":
    main()