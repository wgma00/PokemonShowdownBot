import os
from pylatex import Document, Section, Subsection, Math, Quantity, Command, NoEscape

class latex(object):
    '''handles latex stuff'''
    def handleRequest(self, msg):
        doc = Document(documentclass='minimal')
        doc.append(NoEscape(msg))
        doc.generate_pdf('full')
        os.system("pdfcrop full.pdf")
        os.system("pdftoppm full-crop.pdf|pnmtopng > full.png")
        return 'uploaded to server'
    def validateRequest(self, msg):
        return msg.startswith('$') and msg.endswith('$')
