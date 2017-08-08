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

from plugins.images import OnlineImage
from plugins.CommandBase import CommandBase
from robot import ReplyObject
import random
from user import User


class PartyParrot(CommandBase):
    def __init__(self):
        super().__init__(aliases=['pp', 'parrot', 'party', 'partyparrot'], has_html_box_feature=False)
        self._Base = 'http://cultofthepartyparrot.com/parrots/'
        self._Extra = {'sirocco': 'http://cultofthepartyparrot.com/assets/sirocco.gif'}
        self._Parrot = {'aussiecongaparrot': '.gif',
                        'aussieparrot': '.gif',
                        'aussiereversecongaparrot': '.gif',
                        'bananaparrot': '.gif',
                        'blondesassyparrot': '.gif',
                        'bluecluesparrot': '.gif',
                        'boredparrot': '.gif',
                        'chillparrot': '.gif',
                        'christmasparrot': '.gif',
                        'coffeeparrot': '.gif',
                        'confusedparrot': '.gif',
                        'congaparrot': '.gif',
                        'congapartyparrot': '.gif',
                        'darkbeerparrot': '.gif',
                        'dealwithitparrot': '.gif',
                        'dreidel-parrot': '.xcf',
                        'dreidelparrot': '.gif',
                        'driedelparrot': 'gif',
                        'driedelparrot2': '.gif',
                        'explodyparrot': '.gif',
                        'fastparrot': '.gif',
                        'fieriparrot': '.gif',
                        'fiestaparrot': '.gif',
                        'gentlemanparrot': '.gif',
                        'gothparrot': '.gif',
                        'halalparrot': '.gif',
                        'hamburgerparrot': '.gif',
                        'harrypotterparrot': '.gif',
                        'ice-cream-parrot': '.gif',
                        'magaritaparrot': '.gif',
                        'margaritaparrot': '.gif',
                        'middleparrot': '.gif',
                        'oldtimeyparrot': '.gif',
                        'oriolesparrot': '.gif',
                        'parrot': '.gif',
                        'parrotbeer': '.gif',
                        'parrotcop': '.gif',
                        'parrotdad': '.gif',
                        'parrotmustache': '.gif',
                        'parrotsleep': '.gif',
                        'parrotwave1': '.gif',
                        'parrotwave2': '.gif',
                        'parrotwave3': '.gif',
                        'parrotwave4': '.gif',
                        'parrotwave5': '.gif',
                        'parrotwave6': '.gif',
                        'parrotwave7': '.gif',
                        'partyparrot': '.gif',
                        'pizzaparrot': '.gif',
                        'rightparrot': '.gif',
                        'sadparrot': '.gif',
                        'sassyparrot': '.gif',
                        'shipitparrot': '.gif',
                        'shufflefurtherparrot': '.gif',
                        'shuffleparrot': '.gif',
                        'shufflepartyparrot': '.gif',
                        'skiparrot': '.gif',
                        'slowparrot': '.gif',
                        'stableparrot': '.gif',
                        'tripletsparrot': '.gif',
                        'twinsparrot': '.gif',
                        'upvotepartyparrot': '.gif',
                        'witnessprotectionparrot': '.gif',
                        'moonwalkingparrot': '.gif',
                        'reversecongaparrot': '.gif'}

    def response(self, room, user, args):
        """ Returns a response to the user.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: list of str, any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        """
        if len(args) == 1 and args[0] == 'help':
            return self._help(room, user, args)
        elif len(args) == 1 and not self.valid(args[0]):
            return self._error(room, user, 'incorrect_args')
        else:
            return self._success(room, user, args)

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
        return ReplyObject(('If left empty prints a url to a random parrot from http://cultofthepartyparrot.com/, '
                            'otherwise you may choose to print a specific url. This command supports showimages.'),
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
        if reason == 'incorrect_args':
            return ReplyObject('Correct args are nothing or something on http://cultofthepartyparrot.com/', True)

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
        uploaded_image_data = self.random_parrot()
        if args and self.get_parrot(args[0]):
            uploaded_image_data = self.get_parrot(args[0])
        uploaded_image = uploaded_image_data[0]
        uploaded_image_dims = uploaded_image_data[1]
        if User.compareRanks(room.rank, '*'):
            return ReplyObject(('/addhtmlbox <img src="{url}" height="{height}" width={width}></img>'
                                '').format(url=uploaded_image, height=uploaded_image_dims[1],
                                           width=uploaded_image_dims[0]), True, True)
        else:
            return ReplyObject(uploaded_image, True)

    def valid(self, arg):
        """Check for validation of arguments.

        Args:
            arg: str, possible command
        """
        if (not arg) or (arg in self._Parrot) or (arg in self._Extra):
            return True
        return False

    def random_parrot(self):
        """Generates a tuple for (str:url, (int:width, int:height))"""
        parrot = random.choice(list(self._Parrot.keys()))
        ext = self._Parrot[parrot]
        url = self._Base + parrot + ext
        return url, OnlineImage.get_image_info(url)

    def get_parrot(self, parrot):
        if parrot in self._Parrot:
            parrot, ext = parrot, self._Parrot[parrot]
            url = self._Base + parrot + ext
            return url, OnlineImage.get_image_info(url)
        if parrot in self._Extra:
            url = self._Extra[parrot]
            return url, OnlineImage.get_image_info(url)
        return None
