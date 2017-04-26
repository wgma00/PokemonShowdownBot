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

from plugins.math.images import OnlineImage

import os
import pyimgur
from pylatex import Document
from pylatex import NoEscape
from pylatex import Package
import details


class Latex(OnlineImage):
    """Handles LaTeX related commands.

    This class will take in commands of the form ".latex $equation$". It will
    generate the corresponding LaTeX and upload it to the imgur image hosting.

    Attributes:
        client_id: client object that interacts with the imgur host
        client: client object that interacts with the imgur host
    """

    _client_id = details.client_id
    _client = pyimgur.Imgur(_client_id)

    @staticmethod
    def handle_request(msg):
        """Uploads LaTeX formated equations to imgur and returns a URL.

        Args:
            msg: string that is to converte to LaTeX, requires that string is
                 enclosed by $.
            example:
               handle_request("$\int \sqrt{1+\cos x + \sin x} dx$")
        Returns:
            A tuple (str, (int, int)), where str is the url, on codecogs and
            the tuples are the dimensions of the image (width, height).
        """
        # create a barebones latex document with only the one line
        # specified from the user in the document.
        doc = Document(documentclass='minimal')
        doc.packages = [Package(i) for i in 'amsmath,amsthm,amssymb,amsfonts'.split(',')]
        doc.append(NoEscape(msg))
        doc.generate_pdf('default', compiler_args=['-no-shell-escape',], compiler="pdflatex")
        # These are normal Linux commands that are used to convert the pdf
        # file created by pylatex into a snippet
        os.system("pdfcrop default.pdf")
        os.system("pdftoppm default-crop.pdf|pnmtopng > default.png")
        path = os.path.abspath('default.png')
        uploaded_image = Latex._client.upload_image(path, title="LaTeX")
        return uploaded_image.link, Latex.get_local_image_info(path)

    @staticmethod
    def validate_request(msg):
        """ Does a very basic check if the expression given is valid.

        the command '\input' is removed since it can display sensitive 
        information from files like .ssh_config or TLS certs, and other files 
        which manage to get compiled when ran through LaTeXmk. \def is also 
        removed since it can cause an infinite loop which borks the bot.

        Args:
            msg: string to be validated.
            example:
            >>> validateRequest("$\int \sqrt{1+\cos x + \sin x} dx$")
            True

            >>> validateRequest("\int \sqrt{1+\cos x + \sin x} dx")
            False

        Returns:
            True if message is valid, false otherwise.
        Raises:
            None.
        """
        return ('\\input' not in msg and '\\def' not in msg
                and '\\write18' not in msg and '\\immediate' not in msg)

