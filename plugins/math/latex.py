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
from xml.sax.saxutils import escape, unescape


class Latex(OnlineImage):
    """Handles LaTeX related commands.

    This class will take in commands of the form ".latex $equation$". It will
    generate the corresponding LaTeX and upload it to the imgur image hosting.

    Attributes:
        _LATEX_URL_HOST: str,  
    """
    _LATEX_URL_HOST = 'http://latex.codecogs.com/png.latex?\\bg_white&space;'
    _HTML_ESCAPE_TABLE = {" ": "&space;"}

    @staticmethod
    def html_escape(text):
        return escape(text, Latex._HTML_ESCAPE_TABLE)

    @staticmethod
    def escape_parenthesis(text):
        return ''.join(['\\'+ch if ch in ['(',')'] else ch for ch in text])
    

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
        # have to escape it when to place it into the url
        html_escaped_msg = Latex.html_escape(msg[1:-1])
        # have to escape the '(' and ')' parenthesis for the link
        uploaded_image = Latex._LATEX_URL_HOST + Latex.escape_parenthesis(html_escaped_msg)
        return uploaded_image, Latex.get_image_info(uploaded_image) 


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
        return (msg.startswith('$') and msg.endswith('$') and len(msg) > 2 
                and '\\input' not in msg and '\\def' not in msg 
                and '\\write18' not in msg and '\\immediate' not in msg)


if __name__ == '__main__':
    print(Latex.handle_request('1 + \sin{x}'))
