# PdfText.py
"""
Classes for managing the production of formatted text, i.e. a chapter.
PdfChapter()
PdfParagraph()
PdfString()
"""
from PdfDoc import PdfDocument
from PdfFontMetrics import PdfFontMetrics
import math

# global
metrics = PdfFontMetrics()
FNfontkey = 'F3'
FNfontsize = 5
FONTMarker = '^'

# function copied from stackoverflow
# https://stackoverflow.com/questions/28777219/basic-program-to-convert-integer-to-roman-numerals
from collections import OrderedDict
def write_roman(num):
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

class TextFont( object ):
	"""
	Simple data structure to hold font name and size
	Fonts are the standard pdf fonts F1, F2, F3, with I and B varians,
	Times Roman F3 Italic F3I Bold F3B
	F1: Courier] [F2: Helvetica] [F3: Times-Roman]
	"""
	def __init__(self, pname, psize):
		"""
		Example: f = TextFont('F3',10)
		"""
		self.name  = pname
		self.size = psize
	def __str__( self):
		return 'TextFont("' + self.name+'",'+str(self.size)+')'
	def asItalic( self):
		"""
		Return a new TextFont, which is a italic version of self
		"""
		return TextFont( self.name[0:2]+'I', self.size)		
	def asBold(self):
		"""
		Return a copy of self as a bold font
		"""
		return TextFont( self.name[0:2]+'I', self.size)		
	def asNormal(self):
		"""
		Return a copy of self as a plain font, not italic or bold
		"""
		return TextFont( self.name[0:2], self.size)		
		
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
	
	instance variables:
	
	
	
	"""

	
	def __init__( self, doc ):
		"""
		Initializer for PdfChapter
		The PDFDoc instance passed as <doc> should be already initialized.
		chapter printing starts at a new page
		"""
		self.pdf = doc
		self.paragraphs = []
		self.pages = []

		self.initialPageNumber = 0 # modify this to start with something other than 1
		self.runningPageNumber = 0	# this increments as pages are produced	
		# printed page number is initialPageNumber + runningPageNumber

		self.header = None  # a header is a PdfParagraph()
		self.headerSkip = None # flag to skip the first page when printing a header

		self.footerStyle = None
		self.footerFont = None
		self.footer = None		
		
		self.footnotes = []  # 
		self.footnoteFont = TextFont('F3',7)
		self.superscriptFont = TextFont('F3',5)
		
		# dimensional info extracted from PdfDocument, may be overridden
		self.lineHeightFactor = doc.lineHeightFactor
		self.leftMargin = doc.getLeftMargin('p')
		self.rightMargin = doc.getRightMargin('p')
		self.lineWidth = doc.getLineWidth('p')
		self.topRow = doc.getTopMargin('p')
		self.bottomRow = self.getBottomMargin('p')
		

	def nxtFootnoteNbr( self ):
		"""
		Return the next available footnote number.
		"""
		return len(self.footnotes) + 1
	def addFootnote(self, fnote):
		"""
		Add a PdfFoontnote() to the chapter list
		"""
		assert fnote is PdfFootnote
		self.footnotes.append( fnote )
		
	def getFootnote(self, nbr):
		"""
		Get the <nbr>th footnote.  Footnote 2 is expected to be in self.footnotes[1]
		"""
		assert len(self.footnotes) >= nbr - 1
		assert self.footnotes[ ngr - 1].fnNum == nbr
		
		return self.footnotes[nbr - 1]

	def footnoteParagraph(self, fnNbr):
		"""
		Construct a paragraph from the chapter's <fnNbr>th footnote.
		generate an exception if it does not exist
		"""
		fn = self.getFootnote( nbr)
		para = PdfParagraph( self )
		para.indent = 0
		para.lead = 0
		para.tail = 0
		
		
		
	def footerParagraph(self, pageNumber):
		"""
		Construct a paragraph that will print the footer
		Return None is there is no footer.
		Since page number may be printed, it must be called for each page.
		"""
		ret = None
		if self.footerStyle is not None:
			para = PdfParagraph()
			para.tail = 0
			para.indent = 0
			if self.footerType == 'RomanRight':
				para.alignment = 'r'
				para.addString( self.footerFont, write_roman( page_number))
			para.buildLines(self)
		
		return para
		
	def setFooterStyle(self, pStyle, font):
		"""
		define the chapter footer, such as  
		setFooterStyle( 'RomanRight', TextFont('F3',9))
		"""
		assert pStyle in [ 'RomanRight','None'], "Unknown footer style: "+pStyle
		assert font is TextFont
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
		assert para is PdfParagraph
		self.paragraphs.append( para )
		
	def setHeader( self, pheader, pskipFirst ):
		"""
		add the header - it is a paragraph repeated on each page, except maybe the first
		"""
		assert header is PdfParagrah
		self.header = pheader
		self.headerSkip = pskipFirst
			
	def headerDepth(self):
		"""
		return the number of points required for the optional header.
		A header is just a paragraph so is 
		"""
		if self.header is None:
			return 0
		else:
			self.header.depth()
	def lineWidth(self):
		"""
		return the width of a line (without paragraph-specific modifications) for a chapter
		"""
		ret = self.pdf.getLineWidth('p')
	
			
	def buildPages():
		"""
		construct a list of PdfPage()
		"""
		self.pages = []
		self.runningPageNumber = 0
		done = False
		paraCtr = -1
		page = None
		
		r = self.topRow
		# end row should be constant other than for footnotes
		er = self.bottomRow - self.footerDepth()
		
		for para in self.paragraphs:
		
			if page is None:
				# we need a new page
				self.runningPageNumber++
				fnDepth = 0
				page = PdfPage( self, self.runningPageNumber + self.initialPageNumber)
				# add the header
				for ln in 
						
							
			
				
			
		while not done:
			self.runningPageNumber++
			page = PdfPage( self, self.runningPageNumber + self.initialPageNumber)
			fnDepth = 0 # track footnote depth as footnotes are added to the page
			# the page hdrLines and ftrLines are populated
			# the first addressable body line is the bottom hdrline + header.tail
			# now start to consume paragraphs
			r = self.topRow + self.headerDepth()
			# end row is the start of the footer, adjusted for optional footnotes
			# (when implemented)
			er = chapter.bottomRow - self.footerDepth()
						
			
		
		
	def print(self):
		"""
		A paragraphs have been added. header and footer defined. Perform the sequence of
		steps to print.
		for each paragraph execute para.buildLines(), i.e. self.buildLines
		execute self.buildPages()
		for each page execute page.print()
		"""
		for para in self.paragrahs:
			para.buildLines(self)
		self.header.buildLines()
		
			
		self.buildLines()
		self.buildPages()
		self.printPages()
	
			
	# ******
		
	def prepare( self ):
		# calculate the total length, in points, of all strings in all paragraphs.
		linewidth = self.pdf.getLineWidth('p') 
		# print(' Building lines of length '+ str( linewidth ))
		for para in self.paragraphs:
			# length of each string. Probably redundant. 
			for s in para.strings:
				s.length = metrics.strLength( s.fontkey, s.fontsize, s.string )
			# now within each paragragh, build lines - which may be multiple strings or
			# more often may be subsections of strings. 
			para.buildLines( linewidth )
			
	def newPage(self ):
		"""
		uses Chapter().pdf to invoke a new page in the pdf document.
		Increments pagenumber
		sets chapter prow and pcol to 0
		"""
		self.pdf.newPage()
		# is there a header string?
		self.pageNumber += 1
		self.prow = 0
		self.pcol = 0
		
	def endPage(self, footNotesCtr = 0, fnOrd = 1):
		if footNotesCtr > 0:
			print('printing footnotes')
			self.footnotes.printFootNotes( footNotesCtr, fnOrd, self.prow )
			# ef printFootNotes( self, qty, firstNum,  pRow):
		if self.footerStyle is None:
			pass
		elif self.footerStyle == 'RomanRight':
			s = write_roman(self.pageNumber)
			br = self.pdf.getBottomRow('p')
			rc = self.pdf.getLineWidth('p')
			self.pdf.write( rc,br, s,'r','p')
		self.pdf.endPage()
		
	def process(self ):
		"""
		PdfChapter.process( PdfDoc )
		Print the chapter. Start a new page at the beginning. End whatever page is current
		at the end
		"""
		
		
		# self.newPage( )
		self.pdf.setTextState()
		
		# go paragraph by paragraph, lines by lines.
		
		initial = True
		
		self.lineIncrement = self.pdf.lineHeight * self.pdf.lineHeightFactor
	

		
		
		for para in self.paragraphs:
			para.printParagraph( self )
		self.endPage( )
			
		
	def stretch(self,  lns,  amt):
		"""
		insert spaces until the length of the set to strings has been
		increased by <amt> points.
		"""
		ret = []
		amtToAdd = amt
		while amtToAdd > 2:
	
			for l in lns:
				ol = l.length
				
				l.stretch( amtToAdd )
				# retuce amtToAdd by the increase in length of the string
				amtToAdd = amtToAdd - ( l.length - ol )
				
				if amtToAdd <= 2 :
					break;
		return lns		
		
		
		
		
		

class PdfParagraph( object  ):
	"""
	PdfParagraph represents a body of text. It may be one-line, such as a chapter (or section)
	header, it may be a long paragraph.  It contains  of a list of PdfString objects- it may contain one string, it
	may contain many.  For all of its components, they are produced sequentially and share the
	same justification: left, center, right, full l c r f
	A chapter heading would often be one short line of text, in a larger or more distinct font,
	and centered.
	Properties:
	alignment  [ 'l','c','r','j']
	indent  points
	tail    points
	lead	points
	strings = []
	lines = None or []
	
	"""
	def __init__( self, chapter, lineHeightFactor = 1.2, alignment = 'l', indent = 0, tail = 10 ):
		"""
		all elements in a PdfParagraph share the same justification.
		<indent> is used for the first line of text. It is in points.
		<tail> moves the chapter row counter down tail points
		"""
		assert alignment in [ 'l','c','r','j']
		assert chapter is PdfChapter
		self.chapter = chapter
		self.lineHeightFactor = lineHeightFactor
		self.alignment = alignment
		self.indent = indent
		self.tail = tail
		self.lead = 0
		self.strings = []
		
		self.lines = None
		
	def setIndent(self, pIndent):
		self.indent = pIndent
	def setAlignment(self, pAlignment):
		self.alignment = pAlignment
	def setJustification( self, pJustification):
		self.justification = pJustification
	def setLineHeightFactor( self, pLineHeightFactor ):
		self.lineHeightFactor = pLineHeightFactor
	def setTail(self, pTail):
		self.tail = pTail
	def setLead(self, pLead):
		self.lead = plead
		
		
	def depth( self):
		if self.lines is None:
			self.buildLines()
		ret = 0
		for ln in self.lines:
			ret += ln.depth() * self.lineHeightFactor
		ret +=  (self.tail + self.lead)
		return ret
		
	
		
	def addString(self, pfont, pstring, pfootnotes = None):
		"""
		Construct a PdfString from the parameters and add to the strings list
		<pfootnotes> may be None (the dault) or a list of strings.
		Uses chapter.nxtFootnoteNbr()
		"""
		assert pfont is TextFont
		if pfootnotes is None:
			self.strings.append( PdfString( pfont, pstring )
		else:
			# split the string on the ^ charactert
			txt = pstring.split('^')
			# the string should  be in a list with 1 more element than there are footnotes
			assert len(txt) = len(pfootnotes) + 1
			i = None
			for i in range(0,len(pstring))
				# the first string is split
				self.strings.append( PdfString(pfont, txt[i]))
				num = self.chapter.nxtFootnoteNbr()
				# add the superscript
				self.strings.append( PdfStringFN( chapter.superscriptFont, str(num)))
				fn = PdfFootnote( num, pstring[i]
			# add the ending string is it exists
			if len(txt[-1]) > 0:
				self.strings.append( PdfString( pfont, txt[-1]))
			
		
	
		
	
	def buildLines( self,  chapter ):
		"""
		This method takes all of the strings and breaks them up fit within individual lines. 
		The end result is an array of PdfLine() lines that each fit on a single line regardless of font
		changes (within reason). It does this by splitting PdfStrings that overflow a line
		into multiple shorter PdfStrings. And combing short strings.
		Each PdfLine contains one or more PdfStrings, so be printed on the
		same line. 
		
		The lines[] attribute contains a list of PdfLines.
		These will have the col value set, the row will  be None while owned by a PdfParagraph.
		
		Within a paragraph the first line may have an indent, and therefore e shorter
		If the next string is a PdfStringFN then it is added no matter what.
		"""	
		
		workingLine = PdfLine(None, chapter.leftMargin - self.indent)
		self.lines = []
		
		linewidth = chapter.lineWidth
		
		workingLen = 0
		# spaceLen = metrics.strLength(self.fontkey, self.fontsize, ' ')
		ctr = 0
		ps = None
		# the first line of a paragraph may have an indent.
		targetlen = linewidth - self.indent
		worklingLine.col = lm
		for s in self.strings:
			ps = s.split2( targetlen )
			workingLine.addString(ps)
			
			targetlen = targetlen - ps.length
			# print('added '+ps.string+' new targetlen is '+str(targetlen))
			# we are at the end if a line when s.length > 0
			# is s.length == 0 then the current line may not be full
			while s.length > 0:
				self.lines.append( workingLine )
				lm = chapter.leftMargin
				workingLine = PdfLine( None, chapter.lm)
				targetlen = chapter.lineWidth
				ps = s.split2( targetlen )
				targetlen = targetlen - ps.length	
				workingLine.addString( ps )
			# at this point s is consumed. targetlen is reduced as necessary, The
			# next string - perhaps in a different font - may fit, in full or in part
			# on the same line
			if targetlen < 10:
				self.lines.append( pdfLine )
				workingLine = PdfLine( None, chapter.leftMargin)
				targetlen = chapter.lineWidth
				
		if len(workingLine.strings) > 0:
			self.lines.append( workingLine )
	# now fully populated para.lines with PdfLine() instances
	
	def documentLines(self):
		
		"""
		print out the complete lines with total length for each
		"""	
		for ln in self.lines:
			s = ''
			x = 0
			for l in ln.strings:
				s += l.string
				x += l.length
			print( "{:4.0f}".format(x)+": "+s)
	
	def printParagraph(self, chapter):
		"""
		<chapter> is a PdfChapter. It is needed because it has access to endPage() and newPage()
		methods. And it tracks the chapter page number.
		chapter().pdf is a pdfDoc which is used for the printing.
		This method prints the paragraphs, beginning at the current row and at column 0.
		If there is insufficient room for one or more rows then the chapter.endPage()
		and chapter.newPage() methods are invoked.
		"""
		# self.documentLines()
		if self.lines is None:
			self.buildLines(doc.getLineWidth('p'))
		self.pcol = self.indent
		firstLine = True
		lineCount = len( self.lines )
		lineCtr = 0
		fnCtr = 0 # footnote counter
		for ln in self.lines:
			lineCtr += 1
			if  chapter.prow >= chapter.pdf.getBottomRow('p') - (chapter.footerLines() * (chapter.lineIncrement)) - chapter.footnotes.height(fnCtr):
				chapter.endPage( fnCtr  )
				fnCtr = 0
				chapter.newPage(  )
			if firstLine:
				chapter.pcol = self.indent
				firstLine = False
			else:
				chapter.prow += chapter.lineIncrement
				if firstLine:
					chapter.pcol = self.indent
					firstLine = False
				else:
					chapter.pcol = 0
			# how many point in this line
			lnlen = 0
			# calculate the length of the line, after removing any trailing spaces
			# from the end of the ln
			ln[-1].setString( ln[-1].string.rstrip())
			for l in ln:
				lnlen += l.length
			gap = chapter.pdf.getLineWidth('p') - lnlen
			if lineCtr == 1:
				gap = gap - self.indent
			if self.alignment == 'c':	
				# bump pcol by half the difference between string length and line length
				chapter.pcol = gap / 2
			elif self.alignment == 'r':
				chapter.pcol = gap
			elif self.alignment == 'j':
				# need to allocate gap among Strings
				# unless it is the last line
				if lineCtr < lineCount:
					ln = chapter.stretch( ln, gap)								
					
			for l in ln:
				# each line [ ln ] in self.lines is a list of 1 or more print statements, all to
				# be on the same line. If there are multiple print statements they probably
				# use different fonts
				# set position to next Line
				f = l.string.count('^')
				if f > 0:
					print('footnote found in '+l.string)
				chapter.pdf.setFont( l.fontkey, l.fontsize )
				chapter.pdf.write(chapter.pcol, chapter.prow , l.string, 'l','p')
				chapter.pcol += l.length
		if self.tail > 0:
			chapter.prow += self.tail * chapter.lineIncrement

		
	

			
			
	
class PdfString( object ):
	"""
	PDFString is a continuous bit of text in a common font. It may end
	with a footnote.
	"""

	def __init__( self, pfont, pstring):
		"""
		Initialize a new string, invoke setLength()
		"""
		assert pfont is TextFont
		self.fontkey = pfont.name
		self.fontsize = pfont.size
		self.string = string
		self.setLength()
		
	
	def setLength(self):
		"""
		set the length property based on metrics.strLenth
		"""
		self.length = metrics.strLength( self.fontkey, self.fontsize, self.string)
	def depth(self):
		"""
		the depth of a string - not very useful - is simply the fontize
		"""
		return self.fontsize
		
	def setString(self, t):
		"""
		reset the string property with <t> and invoke self.setLength()
		"""
		self.string = t
		self.setLength()
		
		
	def split2(self, strLen):
		"""
		Splits a string. Returns a new PdfString that has a string <= strLen
		Modifes self, removing that portion of the string.  
		1. if the length of the string is 0 then it returns None
		2. If the length is < <strLen> then it returns a clone of itself,
		   and sets itself to an empty string of length 0
		3. If there is no space in self.string then the same as #2 above
		4. If the very first word in self.string is longer than strLen then
			it returns a PdfString with that first word. So if self.string
			is not empty then it returns a string of some length that may
			be greater than strLen
		"""
		ret = None
		if len(self.string) == 0:
			return None
		elif self.length <= strLen:
			ret = PdfString( TextFont(self.fontkey, self.fontsize), self.string)
			self.setString('')
		elif self.string.find(' ') < 0:
			ret = PdfString( TextFont(self.fontkey, self.fontsize), self.string)
			self.setString('')
		else:
			# build a new string.
			wrkStr = self.string
			
			newStr = ''
			newLen = 0
			
			# if there is some content and at least 1 space return the characters
			# up to and including the first space no matter now long
			newStr = wrkStr[ 0: wrkStr.find(' ')+ 1]	
			wrkStr = wrkStr[ wrkStr.find(' ')+ 1 :]		
			newLen = metrics.strLength( self.fontkey, self.fontsize, newStr)
			while newLen < strLen and len(wrkStr) > 0:
				nxtStr = wrkStr[ 0: wrkStr.find(' ')+1]
				nxtLen = metrics.strLength(self.fontkey,self.fontsize, nxtStr)
				if newLen + nxtLen <= strLen:
					newStr += nxtStr
					newLen += nxtLen
					wrkStr = wrkStr[ wrkStr.find(' ')+1 :] 
				else:
					# print('Could not fit in' + str(nxtLen))
					break
			ret = PdfString( TextFont( self.fontkey, self.fontsize ) , newStr)
			ret.setLength()
			self.setString( wrkStr)
			
				
				
		self.setLength()
		return ret
class PdfStringFN( PdfString ):
	"""
	Inherits from PdfString.
	Font is set
	"""
	def __init__( self, pfont, pstring):
		"""
		passes through to super class
		"""
		PfdString.__init__(self, pfont,pstring)
		
		

class PdfLine( object):
	"""
	# a PdfLine is a collection of strings that are to be output on the same row.
	Methods:
		footnoteCount()
		getFootNote(<nPos>)
		setPos(r,c)
		addString( pdfString )
		height()
		print()
	Properties
		row 
		col
		strings []
		length
	
	"""
	def __init__(self,  prow = None, pcol = none):
		"""
		properties
		self.row
		self.col
		self.strings = []
		self.length = 0
		"""
		self.row  = pRow
		self.col = pCol
		self.strings = []
		self.length = 0
	def footnoteCount(self):
		"""
		Return the count of footnotes present in the line. Footnotes are identified 
		by being a PdfStringFN type
		"""
		ret = 0
		for s in self.strings:
			if s is PdfStringFN:
				ret++
		return ret
	def getFootnote( nPos ):
		"""
		Returns an int, or None
		Return the footnote number of the footnote in the <nPos> position.
		The first footnote by position in a string might be footnote number 7, if it
		is the 7th footnote registered in the chapter. 
		The value is returned as an int.
		"""
		ret = None
		ctr = 0
		for s in self.strings:
			if s is PdfStringFN:
				ctr++
				if ctr == nPos:
					ret = int(s.string)
					break
		return ret
		
		
	def setPos( self, r, c):
		"""
		Set self.row and self.col
		"""
		self.row = r
		self.col = c
		
	def addString(self, pdfString):
		"""
		add a PdfString to self.strings, and reset self.length
		"""
		assert pdfString is PdfString
		self.strings.append( pdfString)
		self.length += pdfString.length
	
		
	def height(self):
		"""
		height is the maximum height found in strings
		"""
		ret = 0
		for s in self.strings:
			ret = max(ret, s.fontsize)
		return ret
	def print(self, doc):
		"""
		print the line of text using the <doc> PdfDocument methods
		"""
		r = self.row
		c - self.col
		for s in self.strings
			doc.write( c, r, s.string,'l','p')
			c += s.length
	
	
		
		
	# #####
			
		
	def findChars(self,  c ):
		"""
		return a list of the indexes of all occurrences of <c> in self.string.
		May be useful for full justification
		"""
		ret = []
		for i in range(0,  len(self.string)):
			if self.string[i] == c:
				ret.append(i)
		return ret
			
		
	def stretch(self, amt):
		"""
		loop though self.string once, adding spaces to existing spaces, until
		the string has been traversed or each space has been padded once. So
		will not necessarily stretch the string to the full amount.	The <amt>
		to be added may be spread among multiple strings.
		"""
		spaceLen = metrics.strLength( self.fontkey, self.fontsize, ' ')	
		added = 0
		newStr = ''
		if amt < 2:
			return self
		elif self.length < 10:
			return self
		for c in self.string:
			if c == ' ' and added < amt :
				newStr += c + ' '
				added += spaceLen
			else:
				newStr += c

		self.setString( newStr )
				
class PdfPage(object):
	"""
	a single printable page
	"""	
	def __init__(self, chapter, pageNumber):
		"""
		Initializes a new pasge.
		writes out hdrlines to self.hdrLines, starting at chapter.topRow
		writes out foot lines at chapter.bottomRow
		bdyLines is an empty list.
		<pageNUmber> is the number to print.
		"""
		self.footnoteCount = 0
		self.pageNumber = pageNumber
		self.bdyLines = []
		self.hdrLines = []
		self.ftrLines = []
		# add the header lines. Starting point is chapter.topRow
		lctr = 0
		for ln in self.header.lines:
			lctr++
			ln.row = chapter.topRow + lctr - 1
			self.hdrLines.append( ln )
		# create a footer paragraph
		if self.footerStyle is not None:
			para = chapter.footerParagraph( self.pageNumber )
			for ln in para.lines:
				ln.row = chapter.bottomRow
				self.ftrLines.append( ln)	
									
			
class PdfFootNote( PdfParagraph):
	"""
	Inherits from PdfParagraph(), but hard-codes most spacing properties	
	
	"""		
	def __init__(self, chapter, fnNum):
		"""
		fnNum is the footnote number
		That is created in chapter.superscriptFont as the first string in the paragraph.
		"""
		self.chapter = chapter
		self.fnNum = fnNum
		self.lead = 0
		self.tail = 0
		self.indent = 0
		self.alignment = 'l'
		self.strings = []
		self.lines = []	
		self.strings.append	( PdfString(  self.chapter.superscriptFont, str(fnNum)) )
		
	def addString(self, pString):
		"""
		Add a string to a footnote
		"""
		self.strings.append( PdfString(self.chapter.footnoteFont, pString))
		
	def addItalic( self, pString):
		"""
		Add an italic string to a footnote
		"""
	
		self.strings.append( PdfString(self.chapter.footnoteFont.asItalic(), pString))
		 
	def addBold( self, pString):
		"""
		Add a bold font string to a footnote
		"""
		self.strings.append( PdfString(self.chapter.footnoteFont.asBold(), pString))
		
	
	
		
		




