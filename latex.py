import os

from pylatex import Document, Section, Subsection, Math, Quantity, Command, NoEscape
import pyimgur  

class latex(object):
    '''handles latex stuff'''
    def __init__(self):
        client_id = '' # you will need your own verification from imgur
        self.client = pyimgur.Imgur(client_id) 

    def handleRequest(self, msg):
        doc = Document(documentclass='minimal')
        doc.append(NoEscape(msg))
        doc.generate_pdf('full')
        os.system("pdfcrop full.pdf")
        os.system("pdftoppm full-crop.pdf|pnmtopng > full.png")
        path = os.path.abspath('full.png')
        uploaded_image = self.client.upload_image(path, title="Uploaded with pyimgur")
        return uploaded_image.link

    def validateRequest(self, msg):
        return msg.startswith('$') and msg.endswith('$')
