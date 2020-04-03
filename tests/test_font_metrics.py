#! /usr/bin/python
# test_font_metrics.py

from PdfDoc import PdfDocument
from PdfFontMetrics import PdfFontMetrics

f = PdfFontMetrics()
f.readFontMetrics()


doc = PdfDocument()
doc.beginDoc("test_font_metrics.pdf")
doc.newPage()
doc.setFont('F2',10)
doc.setTextState()


s = 'Now is the time for all good men to come to the aid of their country'

doc.write(5,2,'String: ' + s, 'l', 'r'  )

doc.write(5,4, 'Character length is ' + str(len(s) ),'l','r')

doc.write(5,6,'F1 10 point length: ' + str( f.strLength('F1',10, s) ),'l','r')

doc.write(5,8,'F2 10 point length: ' + str( f.strLength('F2',10,  s) ),'l','r')

doc.write(5,10,'F3 10 point length: ' + str( f.strLength('F3', 10, s) ),'l','r')

row = 12
for c in s:
	row = row + 1
	doc.write(10,row, 'Char ' + c + ' Font F2 10 point Length ' + str( f.strLength('F2',10, c)),'l','r')
	if doc.getFreeRows() < 3:
		doc.endPage()
		doc.newPage()
		row = 12

doc.endPage()
doc.endDoc()
		
print( "check test_font_metrics.pdf")		
		
	