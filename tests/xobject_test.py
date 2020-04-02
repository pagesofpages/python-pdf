#! /usr/bin/python
# xobject_test.py

from PdfDoc import PdfDocument


doc = PdfDocument()
doc.setDefaultUnit('r')

doc.beginDoc('xobject_test.pdf')

# first do a page with the contents of the xobject
doc.newPage()
doc.setTextState()
doc.setFont('F2B',14)
doc.write(10,10,'CANCELLED','l','p')
doc.endPage()

# now define an xobject - make it like a watermark.

doc.newFormXObject('cancelled')
doc.setTextState()
doc.setFont('F2B',14)
doc.write(4,5,'CANCELLED','c','i')
doc.endFormXObject()

# now open a page, write some text, display the xobject several times,
# write some more text, and the page, and end the document.
for page in range(1,10):
	doc.newPage()
	doc.setTextState()
	doc.setFont('F2B',12)
	doc.writeCenteredInLine(2,'Page '+str(doc.getPageNumber()))
	doc.setFont('F2',10)
	#for i in range(0,60,10):
	doc.write(1,5 ,'XObject Test Row 5  before XObject use','l','p')
 	doc.showForm('cancelled')
	doc.write(1,20 ,'XObject Test Row 20 after XObject use','l','r')
	doc.endPage()
doc.endDoc()

print('Check for output in '+doc.getFileName())
