#! /usr/bin/python
# xobject_image.py

# requires a jpg file named image.jpg

from PdfDoc import PdfDocument


doc = PdfDocument()

doc.setDefaultUnit('i')

doc.beginDoc('xobject_image.pdf')

imageStrings = doc.readImage('image.jpg')
doc.defineImageXObject( imageStrings,'Sh1', 274,283,8,'DeviceRGB',None,'ImageB','DCTDecode')

doc.newPage()
doc.setTextState()
doc.write( 5, 2, 'Image at position 2,9 in inches, no scaling','l','r')
doc.write(5,3,"doc.showImage('Sh1',  2, 9, 'i' )","l","r")

doc.showImage('Sh1',  2, 9, 'i' )


doc.endPage()

doc.newPage()
doc.setTextState()
doc.write( 5, 2, 'Image at position 2,5 in inches,  scaling 0.50','l','r')
doc.write(5,3, "doc.showImage('Sh1',  2, 5, 'i' ,0.5, 0.5)","l","r")

doc.showImage('Sh1',  2, 5, 'i' ,0.5, 0.5)


doc.endPage()

doc.newPage()
doc.setTextState()
doc.write( 5, 2, 'Image at position 2,5 in inches,  scaling 0.50, skew 100, 0','l','r')
doc.write(5,3, "doc.showImage('Sh1',  2, 5, 'i' ,0.5, 0.5,100,0)","l","r")

doc.showImage('Sh1',  2, 5, 'i' ,0.5, 0.5,100,0)

doc.endPage()



doc.newPage()
doc.setTextState()
doc.write(5,2,"Display image multiple times on page",'l','r')

doc.showImage('Sh1',  2, 5, 'i' ,0.5, 0.5)
doc.showImage('Sh1',  4, 5, 'i' ,0.5, 0.5)
doc.showImage('Sh1',  6, 5, 'i' ,0.5, 0.5)

doc.endPage()

doc.endDoc()



