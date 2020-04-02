#! /usr/bin/python
# pdf_file.py
""""
this test script writes PdfDoc.py file as as pdf file.

"""

fileName = 'PdfDoc.py'
fileLocation = '../'
outputFile = 'PdfDoc.pdf'

from PdfDoc import PdfDocument

with open(fileLocation + fileName,"r") as f: 
	lines=f.readlines()
	
	
	
def beginReport():	
	p = PdfDocument()
	p.beginDoc( outputFile )
	p.setLineHeightFactor(1.0)
	p.setDefaultUnit('r')
	p.setDefaultFont('F1',8)
	return p
	

def beginPage(p):
	p.newPage()
	p.setFont('F1B',12)
	p.writeCenteredInLine( 1, 'PdfDoc.py')
	p.setFont('F1',8)
	p.setCurrentRow(3)


def printLine(p,line):
	if line.strip().startswith('def ') or line.strip().startswith('class '):
		p.setFont('F1B',8)
		p.writeCol(3,line,'l')
		p.setFont('F1',8)

	else:
		p.writeCol(3,line,'l')
	p.setCurrentRow( p.getCurrentRow() + 1)

	
def endPage(p):
	p.setFont('F1I',6)
	p.write(1, p.getBottomRow(), 'PdfDoc.py','l')
	p.write( p.getLineWidth(),  p.getBottomRow(),'Page '+str(p.getPageNumber()),'r')
	p.endPage()
	

p = beginReport()

for line in lines:
	if p.page is None:
		beginPage(p)
	
	printLine(p, line)
	
	if p.getFreeRows() < 3:
		endPage(p)
			
p.endDoc()
print( "Check output " + outputFile )	
		
