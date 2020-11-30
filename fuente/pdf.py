"""
Módulo para el manejo de documento en formato PDF.

Este modulo hace uso de la librería reportlab.
"""

import textwrap

from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes




class PDFError(BaseException):
    """
    Excepción del módulo pdf.
    """



class PDF(object):
    """
    Documento en PDF con reportlab.

    https://www.reportlab.com/docs/reportlab-userguide.pdf
    """
    def __init__(self, filename):
        
        self.canvas = canvas.Canvas(filename, pagesizes.letter)
        self.pagesize = (0, 0)

    def __getattribute__(self, name):
        
        if (name == "width"):
            return self.pagesize[0]
        
        elif (name == "height"):
            return self.pagesize[1]
        
        return super().__getattribute__(name)

    def SetCanvas(self, filename=None, pagesize=pagesizes.letter, *args, **kwargs):
        """
        Establece el atributo self.canvas, según los parámetros aceptados para 
        la clase reportlab.pdfgen.canvas.Canvas
        """
        self.canvas = canvas.Canvas(filename=filename, pagesize=pagesize, *args, **kwargs)

    def SetPageSize(self, size=None):
        """
        Establece el tamaño de la página indicada.

        Parameters:
            size (str or tuple or list): 'A4', 'letter', (with, height)...
        """
        if (isinstance(size, (tuple, list))):
            if len(size != 2):
                raise PDFError(f"{type(size)} size debe ser de 2 elementos," \
                    "pero se ha indicado {len(size)}. {size}")
            self.pagesize = tuple(size)
        
        elif isinstance(size, str):
            self.pagesize = getattr(pagesizes, size)
        
        raise PDFError(f"El size debe ser un str, tuple o list; pero se indicó {type(size)}")
    
    def drawString(self, x, y, text, mode=None, charSpace=0, direction=None, wordSpace=None):
        """
        Dibuja el texto indicado, en el formato actual.
        """
        self.canvas.drawString(x, y, text, mode, charSpace, direction, wordSpace)

    def showPage(self):
        self.canvas.showPage()
    
    def save(self):
        self.canvas.save()
