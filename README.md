[![Build Status](https://travis-ci.org/wgma00/PokemonShowdownBot.svg?branch=master)](https://travis-ci.org/wgma00/PokemonShowdownBot)

Pokemon Showdown Bot made in Python 3.

More detailed information can be found in the respective files.

Structure
---------

The Showdown bot is built from three components:

- app.py which contains the class PSBot(), the central workings, and is where most of the connections to other pieces of the app is created.
- The class PSBot is extended from the base class PokemonShowdownBot found in robot.py, and contain almost all basic functions that are required for the bot to function. Most of the more general functions like join, leave and say are defined here.
- The third file that this relies on is room.py, as every room joined creates new room objects that store information for the bot, such as userlists and allowed uses.

Style
-------
This project follows the PEP8 Standard and also the Google Python Standard. If
you notice any discreptencies please let me (wgma00) know.

Setting up
---------
#### Python version:
- Python 3.4.2

### OS enviornment:
-  Linux distribution like debian

### LaTeX dependecies:
- Requires the following to be installed, ``texlive-full`` and ``poppler-utils``

### Calculator requirements:
- Requires that ``gcalccmd`` is installed

#### Guide:
1. Clone the git repo to your desired location
2. Use `pip install requirements.txt` to get relevant modules for the project
3. Follow the instructions in `details-example.yaml` to configure it
4. Run using `python3 app.py`

License
-------

This project is distributed under the terms of the [GPLv3 and MIT License][1].

  [1]: https://github.com/wgma00/PokemonShowdownBot/blob/master/NOTICE

Credits
-------

Owner

- QuiteQuiet

Contributor
- wgma00
