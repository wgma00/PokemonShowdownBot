[![Build Status](https://travis-ci.org/wgma00/quadbot.svg?branch=master)](https://travis-ci.org/wgma00/quadbot) 
[![Coverage Status](https://coveralls.io/repos/github/wgma00/PokemonShowdownBot/badge.svg)](https://coveralls.io/github/wgma00/PokemonShowdownBot)

Pokemon Showdown chat bot made in Python 3.

Functionality
-------------
This chat bot supports the following
- Moderation
- Games and leader-boards
- LaTeX compilation
- Battling
- Sentence generator using Markov chains
- More functionality detailed in ``commands.py`` and ``commands.md``

Structure
---------

The Showdown bot is built from four main components:

- app.py which contains the class PSBot, the central workings, and is where most of the connections to other pieces of 
  the app is created.
- The class PSBot is extended from the base class PokemonShowdownBot found in robot.py, which contains almost all basic 
  functions that are required for the bot to function. Most of the more general functions like ``join``, ``leave`` and 
  ``say`` are defined here.
- The third file that this relies on is room.py, as every room joined creates new room objects that store information 
  for the bot, such as ``userlists`` and ``allowed uses``.
  
- ``commands.py`` delegates or handles most of the commands given by users. You can define your own commands here
   or have them defined in the plugins module. These are considered ``External Commands``.
  
Most of the fun modules are implemented in the plugins section and are treated as stand alone programs, so to not 
interfere up the core functionality of the bot. These modules are meant to contain the implementation of chat games. 
If you want to develop your own feature you should create a submodule in plugins, and map the handler for the command 
in the ``__init__.py`` module handler ``PluginCommands`` section. Here are some examples of implemented commands.

- ``anagram`` is a simple game where the user has to determine, from a randomize string, the original string it was 
  created from. This is pretty famous game in rooms like gamecorner. The game currently only chooses words for Pokemon 
  related stuff like names, and battle moves. 
 
- ``periodic`` is an academic game where the user is given a random word from the BSD dictionary, and must determine a 
  a correct sequence of chemistry symbols (i.e. H, He, Li, etc) which spell out the word.



Style
-------
This project follows the PEP8 Standard and also the Google Python Standard. There may be some discrepancies, as I 
am trying to claw my way closer to these standards.

Setting up
---------
The following are the necessary dependencies for running this software.

### Operating System:
- APT/RPM based linux distribution like Debian or Fedora
- Some functionality may still work on Windows, but have not been fully tested. Use at your own discretion.

### LaTeX:
- Requires the following to be installed, ``texlive`` and ``poppler-utils``

### Calculator:
- Requires that ``gcalccmd`` is installed

#### Python:
- Python 3.4, not tested for any other versions yet. And no plans are made to make it Python 2 compliant.
- PIP - package manager for python

#### Guide:
0. (optional) setup a virtualenv with the following ``virtualenv -p /usr/bin/python3 pokemonshowdownbot && source pokemonshowdownbot/bin/activate`` 
1. Clone the git repo to your desired location
2. Install pip dependencies manually  with `pip install -r requirements.txt`, and install the aforementioned software manually. 
   Or you run the install script using  ``chmod +x install.sh && ./install.sh``
3. Follow the instructions in `details-example.yaml` to configure your bot for login
4. Run using `python3 app.py`
5. (optional) Test for errors you can run ``test.sh`` using ``chmod +x test.sh && ./test.sh``
6. Run git update-index --assume-unchanged plugins/SecretCommands.py to stop tracking SecretCommands.py



### Docker (optional)
A docker image is available with the all of the necessary dependencies installed. You will still need to follow steps
3-4 in the above guide. ``docker pull wgma/pokemonshowdownbot``

License
-------

This project is distributed under the terms of the [GPLv3 and MIT License][1].

  [1]: https://github.com/wgma00/PokemonShowdownBot/blob/master/NOTICE

Credits
-------

Maintainer

- wgma00 

Previous maintainer:
- QuiteQuiet
