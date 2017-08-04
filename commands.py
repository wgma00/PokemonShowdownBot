# Copyright (C) 2016 William Granados<wiliam.granados@wgma00.me>
#
# This file is part of PokemonShowdownBot.
#
# PokemonShowdownBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PokemonShowdownBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PokemonShowdownBot.  If not, see <http://www.gnu.org/licenses/>.
#
# This file incorporates work covered by the following copyright and
# permission notice:
#
#     The MIT License (MIT)
#
#     Copyright (c) 2015 QuiteQuiet<https://github.com/QuiteQuiet>
#
#     Permission is hereby granted, free of charge, to any person obtaining a
#     copy of this software and associated documentation files (the "Software")
#     , to deal in the Software without restriction, including without
#     limitation the rights to use, copy, modify, merge, publish, distribute
#     sublicense, and/or sell copies of the Software, and to permit persons to
#     whom the Software is furnished to do so, subject to the following
#     conditions:
#
#     The above copyright notice and this permission notice shall be included
#     in all copies or substantial portions of the Software.
#
#     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#     OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#     MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#     IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
#     CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#     TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#     SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# The command file for every external command not specifically for running the
# bot. Even more relevant commands like broadcast options are treated as such.
#
# Information passed from the chat-parser:
#   self: The program object itself.
#
#   cmd: Contains what command was used.
#
#   msg: This hold everything else that was passed with the command, such as
#        optional parameters.
#
#   room: What room the command was used in. If the command was sent in a pm,
#         room will contain: 'Pm'. See room.py for more details.
#
#   user: A user object like the one described in the app.py file

from data.pokedex import Pokedex
from data.types import Types




from plugins.Test import Test

# from plugins.math import equation
# from plugins.math.latex import Latex
# from plugins.math.partyparrot import PartyParrot
# from plugins.math.putnam import Putnam
from robot import ReplyObject
from user import User
from room import RoomCommands


available_commands = [Test()]


def Command(self, cmd, room, msg, user):
    """ Handles commands given by the chat parser.

    Better documentation of the commands can be found in the COMMANDS.md file.

    Args:
        self: PSBot object of the main program.
        cmd: string representing the command the user wants to be done.
        room: Room object that this command was posted in.
        msg: the remaining message after this command.
        user: User object that initiated this command.
    Returns:
        Returns a Reply object a differing reply object depending on the
        nature of the command.
    Raises:
        Exception: There was likely improper input in the .calc command or
                   something I entirely missed lol.
    """
    args = list(filter(lambda m: m != '', msg.split(',')))
    for command in available_commands:
        if cmd in command.triggers:
            reply = command.response(user, room, args)
            print('text:', reply.text)
            return reply

    return ReplyObject('{command} is not a valid command.'.format(command=cmd))

def acceptableWeakness(team):
    """ Determines a threshold for a teams weakness to all possible types

    Args:
        team: list of string.
    Returns:
        Returns true if the team is below the threshold, false otherwise.
    Raises:
        None.
    """
    if not team:
        return False
    comp = {t: {"weak": 0, "res": 0} for t in Types}
    for poke in team:
        types = Pokedex[poke]["types"]
        if len(types) > 1:
            for matchup in Types:
                eff = Types[types[0]][matchup]*Types[types[1]][matchup]
                if eff > 1:
                    comp[matchup]["weak"] += 1
                elif eff < 1:
                    comp[matchup]["res"] += 1
        else:
            for matchup in Types:
                if Types[types[0]][matchup] > 1:
                    comp[matchup]["weak"] += 1
                elif Types[types[0]][matchup] < 1:
                    comp[matchup]["res"] += 1
    for t in comp:
        if comp[t]["weak"] >= 3:
            return False
        if comp[t]["weak"] >= 2 and comp[t]["res"] <= 1:
            return False
    return True
