# PdfChapter.py
"""
Classes for managing the production of formatted text, i.e. a chapter.
PdfChapter()
TextFont()
"""
from PdfDoc import PdfDocument
from PdfParagraph import PdfParagraph, PdfFootnoteParagraph
from PdfString import PdfString, PdfStringFN
from PdfPage import PdfPage
from PdfTextFont import TextFont

# function copied from stackoverflow
# https://stackoverflow.com/questions/28777219/basic-program-to-convert-integer-to-roman-numerals
from collections import OrderedDict
def _write_roman(num):
	roman = OrderedDict()
	roman[1000] = "M"
	roman[900] = "CM"
	roman[500] = "D"
	roman[400] = "CD"
	roman[100] = "C"
	roman[90] = "XC"
	roman[50] = "L"
	roman[40] = "XL"
	roman[10] = "X"
	roman[9] = "IX"
	roman[5] = "V"
	roman[4] = "IV"
	roman[1] = "I"
	def roman_num(num):
		for r in roman.keys():
			x, y = divmod(num, r)
			yield roman[r] * x
			num -= (r * x)
			if num <= 0:
				break
	return "".join([a for a in roman_num(num)]).lower()

class PdfChapter( object ):
	"""
	PdfChapter is the container for stand-alone amount of formatted text, such as a
	chapter of text.  It may have headings, multiple paragraphs, and changes of 
	font within a section of text such as a paragraph. It begins with a new page
	and terminates with an end page.
	
	PdfParagraphs are added to self.paragraphs list
	PdfPages are later constructed from the list of PdfParagraphs
	
	A chapter may have a standard header, stored as a paragraph in self.header
	
	A chapter may have a footer, set via a very limited method, and later converted
	into a paragraph.
	
	Footnotes are numbered sequentially within each chapter
	
	instance variables:
	
	
	
	"""

	
	def __init__( self, pdfdoc ):
		"""
		Initializer for PdfChapter
		The PDFDoc instance passed as <pdfdoc> should be already initialized.
		chapter printing starts at a new page
		"""
		self.pdf = pdfdoc
		self.paragraphs = []
		self.pages = []

		self.initialPageNumber = 0 # modify this to start with something other than 1
		self.runningPageNumber = 0	# this increments as pages are produced	
		# printed page number is initialPageNumber + runningPageNumber

		self.header = None  # a header is a PdfParagraph()
		self.headerSkip = None # flag to skip the first page when printing a header

		self.footerStyle = None
		self.footerFont = None
		
		
		self.footnoteNumber = 0
		self.footnotes = []  # arrays of PdfFootnoteParagraph isntances
		self.footnoteFont = TextFont('F3',7)
		self.superscriptFont = TextFont('F3',6)
		
		# dimensional info extracted from PdfDocument, may be overridden
		self.lineHeightFactor = pdfdoc.lineHeightFactor
		self.leftMargin = pdfdoc.getLeftMargin('p')
		self.rightMargin = pdfdoc.getRightMargin('p')
		self.lineWidth = pdfdoc.getLineWidth('p')
		self.topRow = 0 # pdfdoc.getTopMargin('p')
		self.bottomRow = pdfdoc.getBottomRow('p')
		# print('lineheightFactor is '+str(self.lineHeightFactor))
		# print('self.bottomRow is ' + str(self.bottomRow))
	def currentPageNumber(self):
		"""
		Return the current page number: self.initialPageNumber + self.runningPageNuber
		"""
		return self.initialPageNumber + self.runningPageNumber
		
	def nxtFootnoteNbr( self ):
		"""
		Return the next available footnote number.
		"""
		self.footnoteNumber += 1
		# print ( "Returning a new footnote number " + str(self.footnoteNumber))
		return self.footnoteNumber
		
	def addFootnote(self, footnote):
		"""
		Add a footnote , ie. a PdfFootnoteParagraph instance. Assign a number based
		on position in chapter.footnotes [].
		
		"""
		assert isinstance( footnote, PdfFootnoteParagraph )
		footnote.num = len(self.footnotes) + 1
		# construct and insert the superscript footnote number string
		ps = PdfStringFN( self.superscriptFont, str( footnote.num) )
		# insert into the beginning of the list of strings
		footnote.strings.insert( 0, ps )
		footnote.buildLines()
		self.footnotes.append( footnote )
		# print('added footnote number '+str(footnote.num))
		
		
		
	def getFooterParagraph(self):
		"""
		Construct a paragraph that will print the page footer
		Return None is there is no footer.
		Since page number may be printed, it must be called for each page.
		Typically called while building each page. Limited functionality.
		"""
		ret = None
		pageNumber = self.initialPageNumber + self.runningPageNumber
		if self.footerStyle is not None:
			para = PdfParagraph(self)
			para.tail = 0
			para.indent = 0
			if self.footerStyle == 'RomanRight':
				para.alignment = 'r'
				para.addString( self.footerFont, _write_roman( pageNumber))
			elif self.footerStyle == 'ArabicRight':
				para.alignment = 'r'
				para.addString( self.footerFont, str( pageNumber))
			
			para.buildLines()
			# print('returning a footer paragration with '+str(len(para.lines)))
			ret = para
			
		
		return para
		
	def setFooterStyle(self, pStyle, font):
		"""
		define the chapter footer, such as  
		setFooterStyle( 'RomanRight', TextFont('F3',9))
		"""
		assert pStyle in [ 'RomanRight','ArabicRight','None'], "Unknown footer style: "+pStyle
		assert isinstance(font, TextFont )
		self.footerStyle = pStyle
		self.footerFont = font
		
	def footerDepth( self ):
		"""
		Return the depth, in points, of the footer.
		"""
		ret = 0
		if self.footerStyle is not None:
			ret = 2 * self.footerFont.size * self.lineHeightFactor
		return ret
		
		
		
	def addParagraph( self, para):
		"""
		Add <para> to the list of paragraphs
		"""
		assert isinstance(para, PdfParagraph )
		para.buildLines()
		self.paragraphs.append( para )
		
	def addHeader( self, pheader, pskipFirst ):
		"""
		set the header - it is a paragraph repeated on each page, except maybe the first
		<pheadder> us a PdfParagraph
		<pskipfirst> is a boolean. i.e. skip the header on the first page of the chapter.
		These are attributes of the chapter and used when building pages
		"""
		assert isinstance(pheader, PdfParagraph)
		self.header = pheader
		self.headerSkip = pskipFirst
		self.header.buildLines()
			
	def headerDepth(self):
		"""
		return the number of points required for the optional header.
		A header is just a paragraph so is 
		"""
		if self.header is None:
			return 0
		else:
			self.header.depth()
			
	def newParagraph( self, palignment, pindent, ptail):
		"""
		Return a PdfParagraph instance, with the specified properties.
		
		para = chapter.newParagraph( 'j',36,10)
		
		"""
		assert palignment in ( 'l','c','r','j')
		ret = PdfParagraph( self, palignment, pindent, ptail)
		return ret
	def newFootnoteParagraph(self):
		"""
		return  new PdfFootnoteParagraph
		"""
		
		return PdfFootnoteParagraph( self )
		
	def getFootnoteParagraph( self, n ):
		"""
		return the <n>th footnote paragraph
		Footnote numbers begin with 1, and so are are n-1 within the list of footnotes
		"""	
		# print( 'getting footnote number '+str(n))
		assert n-1 >= 0 and n <= len(self.footnotes), "Footnote number "+str(n)+"?" + ' Found '+str(len(self.footnotes))
		return self.footnotes[n -1]
		
		
		
		



	def newPage(self):
		"""
		generate a new PdfPage. update page numbers, write headers and footers
		"""
		self.runningPageNumber += 1
		page = PdfPage( self)
		return page
		
	def addPageHeader(self, page):
		"""
		Add the header to the PdfPage instance
		Return the top available row
		"""
		r = self.topRow
		# add the header
		if self.header is not None and (self.runningPageNumber > 1 or not self.headerSkip):
			r += self.header.lead
			for ln in self.header.lines:
				page.addLine( r, ln)
				r += ln.depth() * self.header.getLineHeightFactor()
			r += self.header.tail
		return r
	def addPageFooter(self, page):
		"""
		Add the footer to the PdfPage instance, if defined
		return the bottom avaialble row
		"""	
		er = self.bottomRow - self.footerDepth()
		# add the footer
		if self.footerStyle is not None:
			para = self.getFooterParagraph()
			para.setTail(0)
			if len(para.lines) > 0:
				ln =  para.lines[0]
				page.addLine( er, ln)
				er -= para.depth()
				# print('Adsded a footerline at '+str(er))
			else:
				pass
				# print ('no footer lines')
		return er
						
	def buildPages(self):
		"""
		construct a list of PdfPage() instances
		for each page:
			create the instance.
			add the header, and footer lines.
			add lines from the paragraphs, and accumulating lines from footnotes if and as present.
			as the lines are added set their rows.
		Footnotes have to be added at the end, because we do not know, until the page is complete,
		how many footnotes will be on a page.
		"""
		self.pages = []
		self.runningPageNumber = 0
		done = False
		paraCtr = -1
		page = None
		
		# end row should be constant other than for footnotes
		pgFnList = []
		lnFnList = []
		pgFnDepth = 0
		lnFnDepth = 0	
		row = 0	
		for para in self.paragraphs:
		
			row += para.lead
			for ln in para.lines:
		
				if page is None:
					# we need a new page
					page = self.newPage()
					row = self.addPageHeader(page )
					fnDepth = 0
					er = self.addPageFooter( page)
					# print('Add a page with top at '+str(r)+ ' and bottom at '+str(er))
										
				# we are within a page.
				# are there footnotes in <ln>?
				lnFnList = ln.footnoteList()
				lnFnDepth = 0
				for n in lnFnList:
					#print(' footnote list '+str(fnList))
					# ln.dump()
					# n is a footnote number, i.e. 7
					lnFnDepth  += ( self.getFootnoteParagraph( n ).depth() *  self.lineHeightFactor)
				# so the space we need for footnotes is is
				pointsNeeded =  pgFnDepth + lnFnDepth
				if pointsNeeded > er - row:
					# then we do not have room on this page, so get a new one
					self.addPageFootnotes( page, pgFnList, er)					
					self.pages.append( page)
					page = self.newPage()
					row = self.addPageHeader(page)
					pgFnList = []
					pgFnDepth = 0
					er = self.addPageFooter(page)
				# then we have room for this line and any footnotes on the line
				page.addLine( row, ln)
				row += ln.depth() * self.lineHeightFactor
				if len(lnFnList) > 0:
					pgFnList = pgFnList + lnFnList
					pgFnDepth = pgFnDepth + lnFnDepth
					# print('calling addPageFootnotes')
			# for each line in paragraph
			row += para.tail	
		# for each para
		# finish up the last page by adding any footnotes
		self.addPageFootnotes( page, pgFnList, er)
		
		self.pages.append( page)
			
		
	def addPageFootnotes( self, page, fnList, endRow):
		"""
		Add the footnotes identified by the list of int values in <fnList> to the PdfPage <page>
		<endRow> is the bottom available row to right to.
		"""
		er = endRow
		for n in reversed(fnList):
			# print('Adding footnote: ' + str(n))
			fn = self.getFootnoteParagraph( n )
			for ln in reversed( fn.lines ):
				page.addLine(er, ln )
				# print('Added a foot note ' + str(ln)+' at row '+str(er))
				er -= ln.depth() * self.lineHeightFactor
		return er
		
		
	def printChapter(self):
		"""
		A paragraphs have been added. header and footer defined. Perform the sequence of
		steps to print.
		for each paragraph execute para.buildLines(), i.e. self.buildLines
		execute self.buildPages()
		for each page execute page.print()
		"""
		self.buildPages()
		for page in self.pages:
			self.pdf.newPage()
			self.pdf.setTextState()
			for ln in page.lines:
				ln.printPdf( self.pdf)
			self.pdf.endPage()			

	
			
