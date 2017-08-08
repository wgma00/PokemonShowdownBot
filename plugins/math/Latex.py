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

import os
import subprocess
import pyimgur
from pylatex import Document
from pylatex import NoEscape
from pylatex import Package

from plugins.images import OnlineImage
from plugins.CommandBase import CommandBase
from robot import ReplyObject
from user import User
import details


class Latex(CommandBase):
    """Handles LaTeX related commands.

    This class will take in commands of the form ".latex $equation$". It will
    generate the corresponding LaTeX and upload it to the imgur image hosting.

    Attributes:
        _client_id: client object that interacts with the imgur host
        _client: client object that interacts with the imgur host
        packages: default packages which are run at start
    """
    def __init__(self):
        super().__init__(aliases=['latex'], has_html_box_feature=True)
        self._client_id = details.apikeys['imgur']
        self._client = pyimgur.Imgur(self._client_id)
        self.packages = 'amsmath,amsthm,amssymb,amsfonts,tikz-cd'

    def response(self, room, user, args):
        """ Returns a response to the user.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: list of str, possible args are showimage, and help
        Returns:
            ReplyObject
        """
        if len(args) == 1 and args[0] == 'help':
            return self._help(room, user, args)
        # error checking
        elif len(args) == 0:
            return self._error(room, user, 'insufficient_args')
        # handling addpackage command and latex command
        elif(len(args) == 2 and args[1] == 'addpackage' and user.hasRank('#')
             and not self.validate_package_install(args[0])):
            return self._error(room, user, 'invalid_package_install')
        elif len(args) == 2 and args[1] == 'addpackage' and not user.hasRank('#'):
            return self._error(room, user, 'insufficient_user_rank')
        elif(len(args) == 2 and args[1] == 'addpackage' and user.hasRank('#')
             and self.validate_package_install(args[0])):
            return self._success_add_package(room, user, args)

        elif len(args) >= 1 and not self.validate_request(args[0]):
            return self._error(room, user, 'invalid_latex_expression')
        elif len(args) == 2 and args[1] == 'showimage' and room.isPM:
            return self._error(room, user, 'show_image_pms')
        elif len(args) == 2 and args[1] == 'showimage' and not User.compareRanks(room.rank, '*'):
            return self._error(room, user, 'insufficient_room_rank')
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
        return ReplyObject(('Compiles a LaTeX expression and crops the relevant portion before uploading to imgur.'
                            ' This command supports showimages, but default behaviour is to post the url.'
                            'Note that \write18 command construct is disabled. Room owners may add packages'), True)

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
        if reason == 'insufficient_args':
            return ReplyObject("Insufficient arguments provided. Should have a LaTeX expression surrounded by $.\n",
                               True)
        elif reason == 'invalid_latex_expression':
            return ReplyObject(('You have inputted an invalid LaTeX expression. You may have forgotten to surround '
                                'your expression with $. Or you may have used restricted LaTeX commands'), True)
        elif reason == 'invalid_package_install':
            return ReplyObject(('You may only install one package at a time. i.e. latex tikz-cd, addpackage . If that '
                                'is not the issue then it is possible that the package specified is not available on '
                                'the host system'), True)

        elif reason == 'insufficient_room_rank':
            return ReplyObject('This bot requires * or # rank to showimage in chat', True)
        elif reason == 'insufficient_user_rank':
            return ReplyObject('This command is reserved for RoomOwners', True)
        elif reason == 'show_image_pms':
            return ReplyObject('This bot cannot showimage in PMs.', True)
        elif reason == 'internal_error':
            return ReplyObject('There was an internal error. Check your LaTeX expression for any errors')

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
        uploaded_image_data = self.handle_request(args[0])
        uploaded_image = uploaded_image_data[0]
        uploaded_image_dims = uploaded_image_data[1]

        show_image = args[-1] == 'showimage'
        if User.compareRanks(room.rank, '*') and show_image:
            # don't render to 100% of screen because latex renders badly
            return ReplyObject('/addhtmlbox <img src="{url}" height="{height}" width="{width}"></img>'.format(
                url=uploaded_image, height=uploaded_image_dims[1], width=uploaded_image_dims[0]), True, True)
        else:
            return ReplyObject(uploaded_image, True)

    def _success_add_package(self, room, user, args):
        """ Adds a package a LaTeX package to the currently supported libraries on compilation

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: list of str, any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        """
        self.packages = '{prev_pkgs},{new_pkg}'.format(prev_pkgs=self.packages, new_pkg=args[0])
        return ReplyObject('{new_pkg} has been added. This is not saved on restart'.format(new_pkg=args[0]), True, True)

    def handle_request(self, latex_expr):
        """Uploads LaTeX formated equations to imgur and returns a URL.

        Args:
            latex_expr: string that is to converte to LaTeX, requires that string is enclosed by $.
            >>> handle_request("$\int \sqrt{1+\cos x + \sin x} dx$")
        Returns:
            A tuple (str, (int, int)), where str is the url, on codecogs and
            the tuples are the dimensions of the image (width, height).
        """
        # create a bare bones latex document with only the one line specified from the user in the document.
        doc = Document(documentclass='minimal')
        doc.packages = [Package(NoEscape(i)) for i in self.packages.split(',')]
        doc.append(NoEscape(latex_expr))
        doc.generate_pdf('default', compiler_args=['-no-shell-escape', ], compiler="pdflatex", clean=True, clean_tex=True)
        # These are normal Linux commands that are used to convert the pdf
        # file created by pylatex into a snippet
        os.system("pdfcrop default.pdf")
        os.system("pdftoppm default-crop.pdf|pnmtopng > default.png")
        path = os.path.abspath('default.png')
        uploaded_image = self._client.upload_image(path, title="LaTeX")
        return uploaded_image.link, OnlineImage.get_local_image_info(path)

    def validate_request(self, msg):
        """ Does a very basic check if the expression given is valid.

        the command '\input' is removed since it can display sensitive
        information from files like .ssh_config or TLS certs, and other files
        which manage to get compiled when ran through LaTeXmk. \def is also
        removed since it can cause an infinite loop which borks the bot.

        Args:
            msg: string to be validated.
            example:
            >>> validate_request("$\int \sqrt{1+\cos x + \sin x} dx$")
            True

            >>> validate_request("\int \sqrt{1+\cos x + \sin x} dx")
            False

        Returns:
            True if message is valid, false otherwise.
        Raises:
            None.
        """
        return (msg.startswith('$') and msg.endswith('$') and len(msg) > 2
                and '\\input' not in msg and '\\def' not in msg
                and '\\write18' not in msg and '\\immediate' not in msg)

    def validate_package_install(self, msg):
        """ validates package installation

        Args:
            msg: str, name of a latex library
        Returns:
            True if that library is available on the host system, False otherwise
        """
        # only handles the case for the file being on pdfLaTeX on linux
        try:
            output = subprocess.check_output('kpsewhich {lib}.sty'.format(lib=msg), shell=True)
        except subprocess.CalledProcessError:
            return False
        return output != ''
