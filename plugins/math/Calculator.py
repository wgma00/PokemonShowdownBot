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

import subprocess
from plugins.CommandBase import CommandBase
from robot import ReplyObject


def MATH_CONST():
    return {"pi": "π", "phi": "(1+sqrt(5))/2"}


class Calculator(CommandBase):
    def __init__(self):
        super().__init__(aliases=['calc', 'calculator'], can_learn=False)

    def learn(self, room, user, data):
        pass

    def response(self, room, user, args):
        """ Returns a response to the user.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: no arguments should be passed except for help
        Returns:
            ReplyObject
        """
        if len(args) == 0:
            return self._error(room, user, 'not_enough_args')
        if len(args) == 1 and args[0] == 'help':
            return self._help(room, user, args)
        elif len(args) > 2:
            return self._error(room, user, 'too_many_args')
        else:
            try:
                return self._success(room, user, args)
            except subprocess.CalledProcessError:
                return self._error(room, user, 'internal_error')

    def _help(self, room, user, args):
        """ Returns a help response to the user.

        In particular gives more information about this command to the user.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: list of str, any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        """
        return ReplyObject('Calculator functionality through GNOME Calculator. Supports substitution for a value x',
                           True)

    def _error(self, room, user, reason):
        """ Returns an error response to the user.

        In particular gives a helpful error response to the user. Errors can range
        from internal errors to user input errors.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            reason: str, reason for this error.
        Returns:
            ReplyObject
        """
        if reason == 'internal_error':
            return ReplyObject("There was an internal error", True)
        elif reason == 'too_many_args':
            return ReplyObject('This command supports only 1 substitution for value x', True)
        elif reason == 'not_enough_args':
            return ReplyObject('There should be an expression optionally followed by substitution', True)

    def _success(self, room, user, args):
        """ Returns a success response to the user.

        Successfully returns the expected response from the user based on the args.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: list of str, any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        """
        if len(args) == 2:
            return ReplyObject(str(self.solve_on_standard_posix(args[0], args[1])), True)
        else:
            return ReplyObject(str(self.solve_on_standard_posix(args[0])), True)

    def sanitize_input(self, user_input):
        """ Removes nasty stuff that could bork the system."""
        user_input = user_input.replace('$', '')
        user_input = user_input.replace('>', '')
        user_input = user_input.replace("'", '')
        user_input = user_input.replace('"', '')
        user_input = user_input.replace('rm', '')
        user_input = user_input.replace('quit', '')
        user_input = user_input.replace('exit', '')
        return user_input

    def solve_on_standard_posix(self, user_input, x="0"):
        """Solves the equation on a normal unix or unix like operating system.

        Pipes input to gcalccmd library which is currently only supported on linux.
        """
        user_input = self.sanitize_input(user_input)
        x = self.sanitize_input(x)
        for const in MATH_CONST():
            user_input = user_input.replace(const, MATH_CONST()[const])
            x = x.replace(const, MATH_CONST()[const])
        user_input = user_input.replace("x", x)
        out = subprocess.check_output("echo '{uinput}' | gcalccmd".format(uinput=user_input), shell=True)
        ret = out.decode("utf-8")
        # return is generally returned as a string starting with > followed by a new line and some white space
        # followed by the output, then followed by the another >
        if ret is None or ret.count('>') != 2:
            return "invalid input"
        # checks if there is an empty line between the two >
        if ret.count('>') == 2 and ret[ret.index(">") + 1:ret[ret.index(">") + 1:].index(">")].strip().replace(' ', '') == '':
            return "invalid input"
        else:
            return ret[ret.index(">") + 1:ret[ret.index(">") + 1:].index(">")].strip()
