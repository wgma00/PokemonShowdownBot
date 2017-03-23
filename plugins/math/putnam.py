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
import urllib.request
import details
import random


START_YEAR = 1985
END_YEAR = 2016

URLS = ["http://kskedlaya.org/putnam-archive/"+str(i)+".tex"
        for i in range(START_YEAR, END_YEAR)]
FILE_PATH = ["putnam_tex/"+str(i)+".tex" for i in range(START_YEAR, END_YEAR)]


class LatexParsingException(Exception):
    """Exception raised for incorrect LaTeX parsing.
    Attributes:
    tex_dump: list of str, corresponding tex file.
    """
    def __init__(self, tex_dump):
        self.tex_dump = tex_dump


def download_putnam_problems():
    """Download the necessary .tex files"""
    global URLS
    global FILE_PATH
    for i in range(len(URLS)):
        path_prefix = '' if __name__ == '__main__' else 'plugins/math/'
        if not os.path.isfile(path_prefix+FILE_PATH[i]):
            urllib.request.urlretrieve(URLS[i], path_prefix+FILE_PATH[i])


def parse_tex_files():
    """Parses and splits a TeX file into its boilerplate and problem code"""
    global URLS
    global FILE_PATH
    path_prefix = '' if __name__ == '__main__' else 'plugins/math/'
    problem_archive = {}
    for i in FILE_PATH:
        file = open(path_prefix+i)
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
        for it in range(len(file_list)-1, -1, -1):
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
        enum_cnt = 0
        for it in range(start+1, end+1):
            line = file_list[it]
            # begins with something like \item[] or is \end{itemize}
            pattern = "\\item\[[^\[\]]*\]"
            start_mode = "\\begin{enumerate}"
            end_mode = "\\end{enumerate}"
            if line.startswith(start_mode):
                enum_cnt += 1
            if line.startswith(end_mode):
                enum_cnt -= 1
            if (re.search(pattern, line) and enum_cnt == 0) or it == end:
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


class Putnam(object):
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
    _client_id = details.client_id
    _client = pyimgur.Imgur(_client_id)
    download_putnam_problems()
    _problem_archive = parse_tex_files()

    @staticmethod
    def random_problem():
        """ Returns a random problem from [START_YEAR, END_YEAR).

        Returns:
            returns a random problem from problem_archive(a list of strings).
        """
        global START_YEAR
        global END_YEAR
        random_year = random.randint(START_YEAR, END_YEAR-1)
        random_problem = random.choice(Putnam._problem_archive[random_year])
        return random_problem

    @staticmethod
    def upload_random_problem():
        """Uploads a random problem to imgur.

        Selects a random problem from the putnam exam, then uploads that problem
        to imgur.

        Returns:
            A URL to the uploaded document.
        Raises:
           LatexParsingException: There was likely an issue with my parsing and
                                  it didn't compile.
        """
        problem = Putnam.random_problem()
        default_doc = []
        # populate doc with the appropriate problem 
        for line in problem[0]:
            if line == '\\end{itemize}':
                for line2 in problem[1]:
                    default_doc.append(NoEscape(line2))
                default_doc.append(NoEscape(line))
            else:
                default_doc.append(NoEscape(line))
        
        doc_class_line = NoEscape(default_doc[0])
        use_pkg_line = NoEscape(default_doc[1])
        opts = doc_class_line[doc_class_line.find('[')+1: doc_class_line.find(']')].split(',')
        args = NoEscape(doc_class_line[doc_class_line.find('{')+1: doc_class_line.find('}')])
        doc = Document(documentclass=Command('documentclass', options=opts, arguments=args))
        # load packages
        doc.packages = [Package(i) for i in use_pkg_line[use_pkg_line.find('{')+1: use_pkg_line.find('}')].split(',')]
        # position right after \begin{document}
        it = 4
        while default_doc[it].strip() != '\end{document}':
            doc.append(NoEscape(default_doc[it]))
            it += 1
        # sometimes I parsed wrong and I'm too tired to check
        doc.generate_pdf('default', compiler="pdflatex")
        # These are normal Linux commands that are used to convert the pdf
        # file created by pylatex into a snippet
        os.system("pdfcrop default.pdf")
        os.system("pdftoppm default-crop.pdf|pnmtopng > default.png")
        path = os.path.abspath('default.png')
        uploaded_image = Putnam._client.upload_image(path, title="LaTeX")
        return uploaded_image.link

