#! /usr/bin/python
# graphics_test.py

from PdfDoc import PdfDocument

p = PdfDocument()

p.beginDoc('graphics_test.pdf')


# test the shade procedure 
p.newPage()
p.setTextState()
p.writeCenteredInLine(1, 'PDF Graphics Test Routines - shade')
p.write(2,1,'shade( 10, 10, 15, 40, \'r\') ')
# 	def shade( self, pX1, pY1, pX2, pY2, pScale = 0.1, pUnit = None):
# X is row; Y is column
p.shade(10, 10, 40, 15, 0.9,'r')
p.setTextState()
p.write(2,10,'shade( 40, 20, 60, 25) r')
p.shade(40, 20, 60, 25, 0.9,'r')

p.write(2,25,'Testing grayscale ranges from 0.0 to 1.00','l','r')


p.write(10,27,'0.0','l','r')
p.shade(10,30,40,32,0.0,'r')


p.write(50,27,'0.6','l','r')
p.shade(50,30,65,32,0.6,'r')



p.write(10,33,'0.1','l','r')
p.shade(10,35,40,37,0.1,'r')

p.write(50,33,'0.7','l','r')
p.shade(50,35,65,37,0.7,'r')


p.write(10,37,'0.2','l','r')
p.shade(10,39,40,40,0.2,'r')

p.write(10,41,'0.3','l','r')
p.shade(10,43,40,44,0.3,'r')

p.write(10,45,'0.4','l','r')
p.shade(10,47,40,48,0.4,'r')

p.write(50,45,'0.9','l','r')
p.shade(50,47,65,48,0.9,'r')

p.write(10,51,'0.5','l','r')
p.shade(10,53,40,54,0.5,'r')

p.write(50,51,'1.0','l','r')
p.shade(50,53,65,54,1.0,'r')



p.endPage()

p.newPage()
p.setTextState()
p.writeCenteredInLine(1, 'PDF Graphics Test Routines - grayBar')

for row in [ 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]:
	p.grayBar(row, 'r')
	p.write(10,row,'This is text in row '+ str(row), 'l','r')
p.endPage()


p.newPage()
p.setTextState()
p.writeCenteredInLine(1, 'PDF Graphics Test Routines - drawLine')

for row in [ 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]:
	#	def drawLine( self, pX1, pY1, pX2, pY2, pUnit = None, pWidth = None):
	p.write(10,row - 1,'This is text the row above the line at ' + str(row), 'l','r')
	p.drawLine( 10,row,p.getLineWidth('c') - 10, row, 'r')
	
p.endPage()


p.newPage()
p.setTextState()
p.writeCenteredInLine(2 , 'PDF Graphics Test Routines - rectangle, lineAcrossPage, pageBorder, verticalPageLine','r')
p.write( 5, 10, 'rectangle( 20, 12, 40, 20, r)', 'l','r')
# 	def rectangle( self, pX, pY, pWidth, pHeight, pUnit = None, pLineWidth = None):
p.rectangle( 20, 12, 40, 20, 'r')
# 	def lineAcrossPage(self, pY, pUnit = None):
p.write( 5, 20, 'lineAcrossPage( 40 , r )','l','r')
p.lineAcrossPage(40,'r')
p.verticalPageLine(40,'c')
p.pageBorder()
p.endPage()


p.newPage()
p.setTextState()
p.writeCenteredInLine(2,'PDF Graphics Test Routines - ellipse','r')

p.write(5,10,'ellipse()','l','r')
p.write(5,11,'	def ellipse(self, pX, pY, pRadiusX, pRadiusY, pUnit = None, pLineWidth = None)','l','r')
p.write(5,12,'	p.ellipse( 4, 4, 2, 1, i, None)','l','r')
p.ellipse(4,4,2,1,'i',2)

p.ellipse( 2,5,1,1,'i',3)
p.write( 2, 5,'A Circle','l','i')
p.endPage()



p.endDoc()

print( "See graphics_test.pdf" )

