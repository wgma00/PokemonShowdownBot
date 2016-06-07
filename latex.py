# The MIT License (MIT)
#
# Copyright (c) 2015
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import os

import pyimgur
from pylatex import Document, Section, Subsection, Math
from pylatex import Quantity, Command, NoEscape


class latex(object):
    '''Handles LaTeX related queries.'''

    def __init__(self):
        '''(latex) -> None
           Initliazes imgur client requirements. More information can be found
           on the public API.
        '''
        # you will need your own verification id from imgur
        client_id = '59fdf359ff5011e'
        self.client = pyimgur.Imgur(client_id)

    def handleRequest(self, msg):
        '''(latex, str) -> str
           Uploads proper LaTeX formated equations to imgur and returns a
           link to it.
           >>> handle_request("$\int \sqrt{1+\cos x + \sin x} dx$")
           http://i.imgur.com/0tEeuyH.png
           >>> handle_request("$\int \sqrt{1 + \sin x} dx$")
           http://i.imgur.com/aKSUTgJ.png
        '''
        # create a barebones latex document with only the one line
        # specified from the user in the document.
        doc = Document(documentclass='minimal')
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
        '''(latex, str) -> Bool
           Basic check if user input is a valid math mode LaTeX command.
           >>> validateRequest("$\int \sqrt{1+\cos x + \sin x} dx$")
           True
           >> validateRequest("\int \sqrt{1+\cos x + \sin x} dx")
           False
        '''
        print(msg)
        return msg.startswith('$') and msg.endswith('$') and len(msg) > 2

