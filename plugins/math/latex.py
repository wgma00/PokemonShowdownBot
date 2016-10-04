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

import pyimgur
from pylatex import Document
from pylatex import Section
from pylatex import Subsection
from pylatex import Math
from pylatex import Quantity
from pylatex import Command
from pylatex import NoEscape
from pylatex import Package
import yaml


class latex(object):
    """Handles LaTeX related commands.

    This class will take in commands of the form ".latex $equation$". It will
    generate the corresponding LaTeX and upload it to the imgur image hosting.

    Attributes:
       client: client object that interacts with the imgur host
       details: map which holds values for sensitive variables i.e. api keys
    """

    def __init__(self):
        """Initliazes imgur client requirements."""
        with open("details.yaml", 'r') as yaml_file:
            self.details = yaml.load(yaml_file)
            client_id = self.details['imgur_apikey']
            self.client = pyimgur.Imgur(client_id)

    def handleRequest(self, msg):
        """Uploads LaTeX formated equations to imgur and returns a URL.

        Args:
            msg: string that is to converte to LaTeX, requires that string is
                 enclosed by $.
            example:
               handle_request("$\int \sqrt{1+\cos x + \sin x} dx$")
        Returns:
           A string that is the URL to the uploaded document.
        Raises:
           Imgur ERROR message: Invalid client_id.
           pdflatex ERROR message: Invalid LaTeX expression passed .
        """
        # create a barebones latex document with only the one line
        # specified from the user in the document.
        doc = Document(documentclass='minimal')
        doc.packages = [Package(i) for i in 'amsmath,amsthm,amssymb,amsfonts'.split(',')]
        doc.append(NoEscape(msg))
        doc.generate_pdf('default')
        # These are normal Linux commands that are used to convert the pdf
        # file created by pylatex into a snippet
        os.system("pdfcrop default.pdf")
        os.system("pdftoppm default-crop.pdf|pnmtopng > default.png")
        path = os.path.abspath('default.png')
        uploaded_image = self.client.upload_image(path, title="LaTeX")
        return uploaded_image.link

    def validateRequest(self, msg):
        """ Does a very basic check if the expression given is valid.

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
        return msg.startswith('$') and msg.endswith('$') and len(msg) > 2

