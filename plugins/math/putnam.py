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
from pylatex import Section
from pylatex import Subsection
from pylatex import Math
from pylatex import Quantity
from pylatex import Command
from pylatex import NoEscape
from pylatex import Package
import urllib.request
import yaml
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


class Putnam(object):
    """Generates a random putnam problem and upload the problem to imgur.  

    This class will take in commands of the form ".putnam" and It will
    randomly generate a random putnam problem from the following problem
    archive:  http://kskedlaya.org/putnam-archive/ .

    Attributes:
       client: client object that interacts with the imgur host.
       details: map which holds values for sensitive variables i.e. api keys.
       problem_archive: a map, maps an integer year to a list of problems for
                        that specific year in TeX format.
    """

    def __init__(self):
        """Initliazes imgur client requirements."""
        with open("details.yaml", 'r') as yaml_file:
            self.details = yaml.load(yaml_file)
            client_id = self.details['imgur_apikey']
            self.client = pyimgur.Imgur(client_id)
            self.download_putnam_problems()
            self.problem_archive = {}
            self.parse_tex_files()
    
    def download_putnam_problems(self):
        """Download the necessary .tex files"""
        global URLS
        global FILE_PATH
        for i in range(len(URLS)):
            path_prefix = '' if __name__ == '__main__' else 'plugins/math/'
            if not os.path.isfile(path_prefix+FILE_PATH[i]):
                urllib.request.urlretrieve(URLS[i], path_prefix+FILE_PATH[i])

    def parse_tex_files(self):
        """Parses and splits a TeX file into its boilerplate and problem code"""
        global URLS
        global FILE_PATH
        path_prefix = '' if __name__ == '__main__' else 'plugins/math/'
        for i in FILE_PATH: 
            file = open(path_prefix+i)
            file_list = []
            latex_template = []
            latex_problems = []
            problem = 0 
            year = int(i[11:15])
            # convert to easier format
            for line in file:
                line = line.strip()
                file_list.append(line)
            # get template from start
            start = 0
            for it in range(len(file_list)):
                if file_list[it].strip() == '\\begin{itemize}':
                    latex_template.append(file_list[it])
                    start = it
                    break
                else:
                    latex_template.append(file_list[it])
            # get template from end
            end = 0
            stack = []
            for it in range(len(file_list)-1,-1,-1):
                if file_list[it].strip() == '\end{itemize}':
                    latex_template.append(file_list[it])
                    end = it
                    while len(stack) != 0: 
                        latex_template.append(stack.pop())
                    break
                else:
                    stack.append(file_list[it])
            # parse the meat of the problem
            temp_problem = []
            for it in range(start+1, end+1):
                line = file_list[it]
                if((line.startswith('\\item') and re.search('^[A-Z]', line[6:]))
                    or it == end ):
                    if(len(temp_problem) != 0):
                        latex_problems.append(temp_problem)
                        temp_problem = [line] 
                else:
                    temp_problem.append(line)
            # now construct them
            self.problem_archive[year] = []
            for problem in latex_problems:
                self.problem_archive[year].append((latex_template, problem))
        

    def random_problem(self):
        global START_YEAR
        global END_YEAR
        random_year = random.randint(START_YEAR, END_YEAR-1) 
        random_problem =  random.choice(self.problem_archive[random_year])
        return random_problem

    def upload_random_problem(self):
        """Uploads a random problem to imgur.

        Selects a random problem from the putnam exam, then uploads that problem
        to imgur.

        Returns:
            A URL to the uploaded document.
        Raises:
           LatexParsingException: There was likely an issue with my parsing and
                                  it didn't compile.
        """
        problem = self.random_problem()
        default_doc = [] 
        # populate doc with the appropriate problem 
        for line in problem[0]:
            if line == '\\end{itemize}':
                for line2 in problem[1]:
                    default_doc.append(NoEscape(line2))
                default_doc.append(NoEscape(line))
            else:
                default_doc.append(NoEscape(line))
        
        opts = options=default_doc[0][default_doc[0].find('[')+1:
                                      default_doc[0].find(']')].split(',')
        args= NoEscape(default_doc[0][default_doc[0].find('{')+1:
                                      default_doc[0].find('}')])
        doc = Document(documentclass=Command('documentclass',
                                             options=opts, arguments=args))
        # load packages
        doc.packages = [Package(i) for i in default_doc[1][default_doc[1].find('{')+1:default_doc[1].find('}')].split(',')]
        it = 4 # position right after \begin{document}
        while(default_doc[it].strip() != '\end{document}'):
            doc.append(NoEscape(default_doc[it]))
            it+=1
        # sometimes I parsed wrong and I'm too tired to check
        try:
            doc.generate_pdf('default')
        except:
            raise LatexParsingException(doc.dumps())
        # These are normal Linux commands that are used to convert the pdf
        # file created by pylatex into a snippet
        os.system("pdfcrop default.pdf")
        os.system("pdftoppm default-crop.pdf|pnmtopng > default.png")
        path = os.path.abspath('default.png')
        uploaded_image = self.client.upload_image(path, title="LaTeX")
        return uploaded_image.link
                                                                                 
if __name__ == '__main__':                                                      
    p = Putnam()
    print('')
    print(p.upload_random_problem())
