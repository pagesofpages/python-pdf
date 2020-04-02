#! /usr/bin/python
# graphics_test.py
"""
This simplest of tests produces a one page pdf with the text "Hello World"
written at column 30 row 20,in Times-Roman 12 point.
"""

from PdfDoc import PdfDocument

doc = PdfDocument()
doc.beginDoc("hello_world.pdf")
doc.newPage()
doc.setTextState()
doc.setFont('F3',12)
doc.write(30,20,'Hello World','l','r')
doc.endPage()
doc.endDoc()


print "Look for the file hello_world.pdf"