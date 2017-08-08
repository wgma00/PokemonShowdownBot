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
import re

import pyimgur
from pylatex import Document
from pylatex import Command
from pylatex import NoEscape
from pylatex import Package
from plugins.CommandBase import CommandBase
from robot import ReplyObject
from user import User
from plugins.images import OnlineImage
import urllib.request
import details
import random


START_YEAR = 1985
END_YEAR = 2016

URLS = ["http://kskedlaya.org/putnam-archive/{num}.tex".format(num=i) for i in range(START_YEAR, END_YEAR)]
FILE_PATH = ["putnam_tex/{num}.tex".format(num=i) for i in range(START_YEAR, END_YEAR)]


class LatexParsingException(Exception):
    pass


def download_putnam_problems():
    """Download the necessary .tex files"""
    global URLS
    global FILE_PATH
    for i in range(len(URLS)):
        path_prefix = '' if __name__ == '__main__' else 'plugins/math/'
        if not os.path.isfile(path_prefix + FILE_PATH[i]):
            urllib.request.urlretrieve(URLS[i], path_prefix + FILE_PATH[i])


def parse_tex_files():
    """Parses and splits a TeX file into its boilerplate and problem code"""
    global URLS
    global FILE_PATH
    path_prefix = '' if __name__ == '__main__' else 'plugins/math/'
    problem_archive = {}
    for i in FILE_PATH:
        file = open(path_prefix + i)
        file_list = []
        latex_template = []
        latex_problems = []
        year = int(i[11:15])
        # convert to easier format
        for line in file:
            line = line.strip()
            file_list.append(line)
        # get template from start
        start = 0
        for it in range(len(file_list)):
            if file_list[it].strip().startswith('\\begin{itemize}'):
                latex_template.append(file_list[it])
                start = it
                break
            else:
                latex_template.append(file_list[it])
        # get template from end
        end = 0
        stack = []
        for it in range(len(file_list) - 1, -1, -1):
            if file_list[it].strip() == '\\end{itemize}':
                latex_template.append(file_list[it])
                end = it
                while len(stack) != 0:
                    latex_template.append(stack.pop())
                break
            else:
                stack.append(file_list[it])
        # parse the meat of the problem
        temp_problem = []
        depth_cnt = 0
        for it in range(start + 1, end + 1):
            line = file_list[it]
            # begins with something like \item[] or is \end{itemize}
            pattern = "\\item\[[^\[\]]*\]"
            start_mode_enum = "\\begin{enumerate}"
            end_mode_enum = "\\end{enumerate}"
            start_mode_item = "\\begin{itemize}"
            end_mode_item = "\\end{itemize}"
            if line.startswith(start_mode_enum) or line.startswith(start_mode_item):
                depth_cnt += 1
            if line.startswith(end_mode_enum) or line.startswith(end_mode_item):
                depth_cnt -= 1
            if (re.search(pattern, line) and depth_cnt == 0) or it == end:
                if len(temp_problem) != 0:
                    latex_problems.append(temp_problem)
                temp_problem = [line]
            elif line:
                temp_problem.append(line)
        # now construct them
        problem_archive[year] = []
        for problem in latex_problems:
            problem_archive[year].append((latex_template, problem))
    return problem_archive


class Putnam(CommandBase):
    """Generates a random putnam problem and upload the problem to imgur.

    This class will take in commands of the form ".putnam" and It will
    randomly generate a random putnam problem from the following problem
    archive:  http://kskedlaya.org/putnam-archive/ .

    Attributes:
       _client_id: secret url API key received from imgur.
       _client: client object that interacts with the imgur host.
       _problem_archive: a map, maps an integer year to a list of problems for
                        that specific year in TeX format.
    """

    def __init__(self):
        super().__init__(aliases=['putnam'], has_html_box_feature=True)
        self._client_id = details.apikeys['imgur']
        self._client = pyimgur.Imgur(self._client_id)
        download_putnam_problems()
        self._problem_archive = parse_tex_files()

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
        elif len(args) > 1 and args[0] != 'showimage':
            return self._error(room, user, 'too_many_args')
        elif len(args) == 1 and args[0] == 'showimage' and room.isPM:
            return self._error(room, user, 'show_image_pms')
        elif len(args) == 1 and args[0] == 'showimage' and not User.compareRanks(room.rank, '*'):
            return self._error(room, user, 'insufficient_room_rank')
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
        return ReplyObject('This generates a link to a random putnam problem from {start} to {end} and supports showimages'.format(start=START_YEAR, end=END_YEAR), True)

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
        if reason == 'too_many_args':
            return ReplyObject('This command does not take any arguments', True)
        elif reason == 'insufficient_room_rank':
            return ReplyObject('This bot requires * or # rank to showimage in chat', True)
        elif reason == 'show_image_pms':
            return ReplyObject('This bot cannot showimage in PMs.', True)

    def _success(self, room, user, args):
        """ Returns a success response to the user.

        Successfully returns the expected response from the user based on the args.

        Args:
            room: Room, room this command was evoked from.
            user: User, user who evoked this command.
            args: list of str, any sequence of parameters which are supplied to this command
        Returns:
            ReplyObject
        Raises:
            LatexParsingException: there was an issue parsing the document
        """
        showimage = True if len(args) == 1 and args[0] == 'showimage' else False

        uploaded_image_data = self._upload_random_problem()
        uploaded_image = uploaded_image_data[0]
        uploaded_image_dims = uploaded_image_data[1]

        if showimage:
            return ReplyObject('/addhtmlbox <img src="{url}" height="{height}" width="{width}"></img>'.format(
                url=uploaded_image_data, height=uploaded_image_dims[1], width=uploaded_image_dims[0]), True, True)
        else:
            return ReplyObject('{url}'.format(url=uploaded_image), True)

    def _random_problem(self):
        """ Returns a random problem from [START_YEAR, END_YEAR).

        Returns:
            returns a random problem from problem_archive(a list of strings).
        """
        global START_YEAR
        global END_YEAR
        random_year = random.randint(START_YEAR, END_YEAR - 1)
        random_problem = random.choice(self._problem_archive[random_year])
        return random_problem

    def _upload_problem(self, problem):
        """Uploads a specified problem to imgur.

        Returns:
            A tuple (str, (int, int)), where str is the url, on imgur and
            the tuples are the dimensions of the image (width, height).
        Raises:
           LatexParsingException : there was an issue parsing the document
        """
        default_doc = []
        # populate doc with the appropriate problem
        for line in problem[0]:
            # these first two statements are for wrapping the title around in a minipage which allows
            # the problem to be generated on one page and doesn't invoke \newpage
            if line == '\\begin{document}':
                default_doc.append(NoEscape(line))
                default_doc.append(NoEscape('\\begin{minipage}{\\textwidth}'))
            elif line == '\\maketitle':
                default_doc.append(NoEscape(line))
                default_doc.append(NoEscape('\\end{minipage}'))
            elif line == '\\end{itemize}':
                for line2 in problem[1]:
                    default_doc.append(NoEscape(line2))
                default_doc.append(NoEscape(line))
            else:
                default_doc.append(NoEscape(line))

        doc_class_line = NoEscape(default_doc[0])
        use_pkg_line = NoEscape(default_doc[1])
        # skip twocolumn since it makes the problem look spread awfully
        opts = filter(lambda pkg: pkg != 'twocolumn', doc_class_line[doc_class_line.find('[') + 1: doc_class_line.find(']')].split(','))
        args = NoEscape(doc_class_line[doc_class_line.find('{') + 1: doc_class_line.find('}')])
        doc = Document(documentclass=Command('documentclass', options=opts, arguments=args))
        # load packages
        doc.packages = [Package(i) for i in use_pkg_line[use_pkg_line.find('{') + 1: use_pkg_line.find('}')].split(',')]
        # position right after \begin{document}
        it = 4
        while default_doc[it].strip() != '\end{document}':
            doc.append(NoEscape(default_doc[it]))
            it += 1
        # fail safe for future problems which may not parse correctly
        try:
            doc.generate_pdf('default', compiler="pdflatex")
        except:
            raise LatexParsingException

        # These are normal Linux commands that are used to convert the pdf
        # file created by pylatex into a snippet
        os.system("pdfcrop default.pdf")
        os.system("pdftoppm default-crop.pdf|pnmtopng > default.png")
        path = os.path.abspath('default.png')
        uploaded_image = self._client.upload_image(path, title="LaTeX")
        return uploaded_image.link, OnlineImage.get_local_image_info(path)

    def _upload_random_problem(self):
        """Uploads a random problem to imgur.

        Selects a random problem from the putnam exam, then uploads that problem
        to imgur.

        Returns:
            A tuple (str, (int, int)), where str is the url, on imgur and
            the tuples are the dimensions of the image (width, height).
        Raises:
           LatexParsingException: there was an issue parsing the document
        """
        problem = self._random_problem()
        return self._upload_problem(problem)
