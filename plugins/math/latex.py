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
import struct
import imghdr
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
        return uploaded_image, self.get_image_size(path)

    def validateRequest(self, msg):
        """ Does a very basic check if the expression given is valid.

        the command '\input' is removed since it can display sensitive information from files like .ssh_config or
        TLS certs, and other files which manage to get compiled when ran through LaTeXmk. \def is also removed since
        it can cause an infinite loop which borks the bot.

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
        return msg.startswith('$') and msg.endswith('$') and len(msg) > 2 and '\\input' not in msg and '\\def' not in msg and '\\write18' not in msg and '\\immediate' not in msg

    def get_image_size(self, fname):
        '''Determine the image type of fhandle and return its size.
        from draco'''
        with open(fname, 'rb') as fhandle:
            head = fhandle.read(24)
            if len(head) != 24:
                return
            if imghdr.what(fname) == 'png':
                check = struct.unpack('>i', head[4:8])[0]
                if check != 0x0d0a1a0a:
                    return
                width, height = struct.unpack('>ii', head[16:24])
            elif imghdr.what(fname) == 'gif':
                width, height = struct.unpack('<HH', head[6:10])
            elif imghdr.what(fname) == 'jpeg':
                try:
                    fhandle.seek(0)  # Read 0xff next
                    size = 2
                    ftype = 0
                    while not 0xc0 <= ftype <= 0xcf:
                        fhandle.seek(size, 1)
                        byte = fhandle.read(1)
                        while ord(byte) == 0xff:
                            byte = fhandle.read(1)
                        ftype = ord(byte)
                        size = struct.unpack('>H', fhandle.read(2))[0] - 2
                    # We are at a SOFn block
                    fhandle.seek(1, 1)  # Skip `precision' byte.
                    height, width = struct.unpack('>HH', fhandle.read(4))
                except Exception:  # IGNORE:W0703
                    return
            else:
                return
            return width, height

