#! /usr/bin/python
# font_test.py
"""
Output fragments of text in a variety of fonts.
"""

from PdfDoc import PdfDocument
from PdfFontMetrics import PdfFontMetrics
metrics = PdfFontMetrics()

doc = PdfDocument()
doc.beginDoc('font_test.pdf')

doc.newPage()
doc.setTextState()

for fontsize in range(8,14):
	doc.setFont('F3',fontsize)
	doc.write(10,fontsize,"this is a "+str(fontsize)+" point font at 10,"+str(fontsize),'l','r')
doc.endPage()	





doc.endDoc()


print( "See font_test.pdf" )
