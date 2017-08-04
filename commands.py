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

from plugins.Send import Send
from plugins.Credits import Credits
from plugins.math.Latex import Latex
from plugins.Machine import Machine

from robot import ReplyObject
from user import User
from room import RoomCommands


available_commands = [Send(), Credits(), Latex(), Machine()]


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
    # filter out empty spaces from list and strip them
    args = list(filter(lambda m: m != '', [item.strip() for item in msg.split(',')]))
    for command in available_commands:
        if cmd in command.aliases:
            return command.response(room, user, args)

    return ReplyObject('{command} is not a valid command.'.format(command=cmd))

