# \[W\]\[O\]\[R\]\[D\]\[Py\]
#### Author: Barry Ptak
#### Video Demo:  https://youtu.be/7Gw0yKOncZ0
---
## Description:
---
Originally created for the CS50 Introduction to Programming with Python course.

WordPy is a clone of the popular game Wordle that runs in the terminal.

Each day a new word is selected as the day's answer.
The aim is to guess the correct five-letter word of the day.
For each guess, the game indicates if each letter is in the correct answer and whether it's in the correct place or not.
The user has up to six tries to guess the right word and win the game.

This version allows (via command-line argument) the user to play over and over against random answers rather than needing to wait a day for a new word to guess.

---
## How to run
---
First ensure that the colorama library is installed:
```
pip install colorama
````
Then, to play today's word simply run the program with
```
python project.py
```
There are a number of command-line options available to change how the program runs:

#### -date <ISO_FORMAT_DATE>
The game picks a new word for each day.
The force the game to use a word from a specific date then pass it on the command line in ISO format (YYYY-MM-DD)

#### -word <FIVE_LETTER_WORD>
This option forces the game to use a specific five-letter word (A-Z characters only)

#### -random
The game will ignore the current date and pick a random word instead

#### -infinite
By default the game only has a single play-through at a time. Pass this option to keep playing over and over (this option forces -random too)

---
## Design decisions
---

There were a number of key design decisions made for this project:

### Separation of concerns
While it would be possible to keep all of the logic required for this project in a single file, by seperating out related functionality into classes and functions it made things easier to read, maintain and test.

The root file ([project.py](./project.py)) was kept as the best place to process command-line arguments, display usage help, and initialise the main game oject, but to perform any core logic itself.

If I was to work on more projects I might be tempted to make the command-line argument handling generic and reuse it across projects. Or there is likely already a pip-installable for this, of course!

All of the main game logic made sense to have in a single place ([game.py](./game.py)), of course, but by pulling the configuration data out we could create a standalone class to contain it that we can test and pass around easily.

Finally, there were a few repeated letter or word processing operations that the core game logic required. They could have been kept as part of game.py, but moving them out made the code more clean in both locations and allowed game.py to concentrate on the main state machine and display logic without being bloated out by string processing.

### Use of a state machine
The game moves through a series of distinct states based on what is currently going on. This made a perfect candidate for a simpel state machine implementation. This allowed us to have clean and separate methods for each state, and a clear place to handle and special logic required to move between states (and validate state changes if necessary).

### Data structures
After putting all of the structure in place all that was really left was determining how to represent some of the key bits of data used. Fortunately there were all straight-forward and didn't require anything very complex. In the end I settled for simply storing guesses as as tuple of the guessed word and a list containing the score/state of each letter. This could easily be stored as part of the game state and passed around for rendering. If the type had more complex requirements then I would have created a class to represent it, but we did n't quite get to that need so things were kept simple.

---
## Main Python Files
---

### [project.py](./project.py)
---
Main entry point to the project.
Contains functions for parsing the command-line arguments, handling errors, printing usage instructions, and creating and running the main Game object.

Tested via [test_project.py](./test_project.py)

### [game.py](./game.py)
---
Main game state machine and logic.
Loads word lists from JSON files.
Depending on config options passed during construction

Renders game 'screens' and state to the user and parses their input for interaction.
Contains the following main states:
- INTRO - Renders the welcome screen and prompts the user for how to proceed.
- HELP - Renders 'how to play' information and prompts the user for how to proceed.
- GUESSING - The is the main game state. Here the user is prompted to enter a guess (we keep prompting until we get valid input) which we then compare to the correct answer. We update the view to reflect the user's guess and indicate which letters are correct, correct but in the wrong place, and wrong. This state is repeated until the user guesses correctly, or they exceed the allowed number of guesses.
- WON - The user has won by correctly guessing the answer. Renders the success screen and prompts the user for how to proceed.
- LOST - The user has failed to correctly guess the answer within six guesses.  Renders the loss screen and prompts the user for how to proceed.
- QUIT - Cleanly exits the main loop so that the program can exit

Tested via [test_game.py](./test_game.py)

### [gameconfig.py](./gameconfig.py)
---
Simple class that stores the game configuration (e.g. which mode to run in, forced date, word, etc..)

This class was created and placed in its own file to make testing easy, and to make the configuration something that can possible be serialised in a later iteration.

Tested via [test_gameconfig.py](./test_gameconfig.py)

### [letterutils.py](./letterutils.py)
---
A set of utilities to make working with letters and words easier.
Provides functionality such as basic word validation (correct length and character set), scoring a word against the correct answer, and formatting a word for display using colours and other layout.

These utility functions were placed here to keep the main game logic cleaner and easier to read.

Tested via [test_letterutils.py](./test_letterutils.py)

---
## Other Files
---

### [data/answers.json](./data/answers.json)
JSON file containing all possible answers for the game.

### [data/valid_words.json](./data/valid_words.json)
JSON file containing all valid input words for the game

### [README.md](./README.md)
This file

### [requirements.txt](./requirements.txt)
Lists all pip-installable libraries required for this project

---
## Dependencies
---
Requires use of [colorama](https://pypi.org/project/colorama/) python module
```
pip install colorama
```
