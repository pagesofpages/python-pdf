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
doc.setFont('F3',8)

doc.write(10,10,'This is an 8 point font')
doc.setDefaultUnit('r')
doc.write(0,0,'This is 0,0 with an 8 point font','l','r')
br = doc.getBottomRow('r')
rc = doc.getRightColumn('c')
doc.write(rc,br,'This is '+str(rc)+','+str(br)+' with an 8 point font','r','r')
br = doc.getBottomRow('p') - 10
rc = doc.pageWidth - doc.leftMargin 
doc.write( rc, br,'One line up, the actual raw right margin', 'r','p')
doc.write(doc.getBottomRow() - 3, doc.getRightColumn(),'X','l','c')
ruler = ''

for i in range(0,20):
	ruler = ruler + '1234567890'

	
doc.write(0,20,ruler,'l','r')
doc.write(117,21,'X','l','r')	

doc.write(0,30,'Bottom Row '+str(doc.getBottomRow()),'l')
doc.write(0,31,'Right Column '+str(doc.getRightColumn()),'l')
doc.endPage()


doc.newPage()
doc.setPageSize(8.5, 11.0, 'i')
doc.setTextState()
doc.setFont('F3',8)

doc.write(10,10,'This is an 8 point font')
doc.setDefaultUnit('r')
doc.write(0,0,'This is 0,0 with an 8 point font','l','r')
br = doc.getBottomRow('r')
rc = doc.getRightColumn('c')
doc.write(rc,br,'This is '+str(rc)+','+str(br)+' with an 8 point font','r','r')
br = doc.getBottomRow('p') - 10
rc = doc.pageWidth - doc.leftMargin 
doc.write( rc, br,'One line up, the actual raw right margin', 'r','p')
doc.write(doc.getBottomRow() - 3, doc.getRightColumn(),'X','l','c')
ruler = ''

for i in range(0,20):
	ruler = ruler + '1234567890'

	
doc.write(0,20,ruler,'l','r')
doc.write(doc.getRightColumn(),21,'X','l','r')	

doc.write(0,30,'Bottom Row '+str(doc.getBottomRow()),'l')
doc.write(0,31,'Right Column '+str(doc.getRightColumn()),'l')
doc.endPage()




doc.endDoc()


print "See font_test.pdf"