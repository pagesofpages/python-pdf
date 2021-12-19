# PdfParagraph.py

from PdfString import PdfString, PdfStringFN
from PdfLine import PdfLine



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
	def __init__( self, chapter, alignment = 'l', indent = 0, tail = 10 ):
		"""
		all elements in a PdfParagraph share the same justification.
		<indent> is used for the first line of text. It is in points. See setIndent()
		<tail> moves the chapter row counter down tail points
		<lead> is space above the paragraph; assumed less common, and defaulted to 0. See setLead()
		"""
		assert alignment in [ 'l','c','r','j']
		
		self.chapter = chapter
		self.alignment = alignment
		self.indent = indent
		self.tail = tail
		self.lead = 0
		self.strings = []
		self.lineHeightFactor = None 
		self.leftMargin = 0
		self.rightMargin = 0

		
		self.lines = None
		
	def setIndent(self, pIndent):
		self.indent = pIndent
	def setAlignment(self, pAlignment):
		assert pAlignment in [ 'l','c','r','j']
		self.alignment = pAlignment
	def setLineHeightFactor( self, pLineHeightFactor ):
		"""
		To override the chapter.lineHeightFactor value, for this paragraph
		"""
		self.lineHeightFactor = pLineHeightFactor
	def setTail(self, pTail):
		self.tail = pTail
	def setLead(self, pLead):
		"""
		set the lead property - i.e. space in points before the paragraph starts.
		"""
		self.lead = pLead
		
	def setMargins( self, pleftMargin, prightMargin):
		"""
		To Override the left and right margins of the chapter, for this paragraph only
		
		"""
		self.leftMargin = pleftMargin
		self.rightMargin = prightMargin
	def getLineWidth(self):
		"""
		return the line width, which will be the chapter's linewidth unless the left and
		right margins have been overridden for this paragraph
		"""
		return self.chapter.lineWidth - self.leftMargin - self.rightMargin + 1		
	def getLineHeightFactor(self):
		"""
		return the lineHeightFactor, which is the chapter's unless overridden at the paragraph
		"""	
		return self.chapter.lineHeightFactor if self.lineHeightFactor is None else self.lineHeightFactor
	def depth( self):
		if self.lines is None:
			self.buildLines()
		ret = 0
		for ln in self.lines:
			ret += ln.depth() * self.getLineHeightFactor()
		ret +=  (self.tail + self.lead)
		return ret
		
	
		
	def addString(self, pfont, pstring):
		"""
		Construct a PdfString from the parameters and add to the strings list
		A '^' character marks a footnote indicator.
		Uses chapter.nxtFootnoteNbr().
		The footnote text needs to be added later, as a footnote paragraph.
		"""
		#assert isinstance( pfont , TextFont )
		
		ndx = pstring.find('^')
		while ndx >= 0:
			# print( "Found a footnote in "+pstring)
			if ndx > 0:
				# split off whatever is in front of the ^
				self.strings.append(PdfString(pfont, pstring[0:ndx]))
				# print('Footnote After '+pstring[0:ndx])
			# now add a footnote string 
			num = self.chapter.nxtFootnoteNbr()
			# add the superscript
			self.strings.append( PdfStringFN( self.chapter.superscriptFont, str(num)))
			# now reset pstring
			if ndx < len(pstring) - 1:
				pstring = pstring[ndx+1:]
				ndx = pstring.find('^')
			else:
				pstring = ''
				ndx = -1
		# now is anything left of pstring?
		if len(pstring) > 0:
			# print('Adding <'+pstring+'<')
			self.strings.append( PdfString( pfont, pstring))
			
		#self.documentStrings()
			
			
		
	
		
	
	def buildLines( self ):
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
		
		workingLine = PdfLine(None, self.indent + self.leftMargin)
		self.lines = []
		
		linewidth = self.getLineWidth()
		# print('Setting line width to '+str(linewidth))
		
		workingLen = 0
		# spaceLen = metrics.strLength(self.fontkey, self.fontsize, ' ')
		ctr = 0
		ps = None
		# the first line of a paragraph may have an indent.
		targetlen = linewidth - self.indent
		lm =  self.leftMargin
		for s in self.strings:
			if isinstance( s, PdfStringFN):
				# print( 'found a PdfStringFN:' +s.string)
				# this is a footnote. Add no matter what and go on to the nexdt string
				workingLine.addString( s )
				targetLen = targetlen - s.length
				continue
			ps = s.split2( targetlen )
			if ps is None:
				continue

			workingLine.addString(ps)
			
			targetlen = targetlen - ps.length
			# print('added '+ps.string+' new targetlen is '+str(targetlen))
			# we are at the end if a line when s.length > 0
			# is s.length == 0 then the current line may not be full
			while s.length > 0:
				self.lines.append( workingLine )
				lm = self.leftMargin
				workingLine = PdfLine( None, lm)
				targetlen = linewidth
				ps = s.split2( targetlen )
				targetlen = targetlen - ps.length	
				workingLine.addString( ps )
			# at this point s is consumed. targetlen is reduced as necessary, The
			# next string - perhaps in a different font - may fit, in full or in part
			# on the same line
			if targetlen < 10:
				self.lines.append( workingLine )
				workingLine = PdfLine( None, lm)
				targetlen = linewidth
				
		if len(workingLine.strings) > 0:
			self.lines.append( workingLine )
		
		#for i in range( 0, len(self.lines)):
		#	print(str(i)+':' )
		#	self.lines[i].dump()
		# now fully populated para.lines with PdfLine() instances
		# now set the alignment/justification
		# print ( 'starting paragraph with alignment '+self.alignment)
		self.align()
		"""
		for i in range( 0, len(self.lines)):
			ln = self.lines[i]
			# is there a trailing space?
			ln.strings[-1].trim()
			gap = linewidth - ln.length
			if i == 0:
				gap = gap - self.indent
				# print('fap reduced by '+str(self.indent))
				
			# print('target width '+str(self.chapter.lineWidth)+' Current '+str(ln.length)+' Gap '+str(gap))
			if self.alignment == 'l':
				pass
			elif self.alignment == 'r':
				ln.col = gap
			elif self.alignment == 'c':
				ln.col = gap  / 2
			elif self.alignment == 'j' and gap >= 2.25:
				# full justification
				# print( 'Stretching ')
				# ln.dump()
				if i < len(self.lines) - 1:
					ln.stretch( gap )
				#print ('length now '+str(ln.length))
		"""	
		#print('Paragraph line with '+ str(self.getLineWidth()))	
		#self.documentLines()	
	def rightAlign(self):
		"""
		Right-align the lines in the paragraph. 
		set line.col to the target length - the length of the lime
		"""		
		linelength = self.getLineWidth()
		# say actual line length is 335
		# indent is 36
		# target length is 380
		# set col to 380 - 335 because the indent will have been considered when constructing
		# the original line
		for ln in self.lines:
			ln.col = linelength - ln.length
	def centerAlign(self):
		"""
		center the line
		"""	
		linelength = self.getLineWidth()
		for ln in self.lines:
			ln.col = (linelength - ln.length) / 2
	def justify(self):
		"""
		Justify the text. Each line begins on the left margin (plus indent for first line)
		Each line end on the right margin, i.e. ln.col is indent + left margin, or left margin,
		Does not modify the last line.
		"""	
		ctr = 0
		targetLength = self.getLineWidth()
		# print('Target length is ' + str(targetLength))
		for ln in self.lines[0: len(self.lines)-1]:
			ctr = ctr + 1
			if ctr == 1:
				ln.stretch( targetLength - self.indent)
			elif ctr < len(self.lines):
				ln.stretch( targetLength )
			
			
		
			
	def align(self):
		"""
		align or justify the lines.
		"""
		assert len(self.lines) > 0
		# core rules:
		# 1. No line should begin with a space.
		# 2. No line should end with a space
		for ln in self.lines:
			ln.strings[0].ltrim()
			ln.strings[-1].trim()
		if self.alignment == 'l':
			pass
		elif self.alignment == 'r':
			self.rightAlign()
		elif self.alignment == 'c':
			self.centerAlign()
		elif self.alignment == 'j':
			self.justify()
		
	def documentLines(self):
		
		"""
		print out the complete lines with total length for each
		"""	
		for ln in self.lines:
			s = '<'
			x = 0
			for l in ln.strings:
				s += l.string
				x += l.length
			print( str(ln.col)+'-'+ "{:4.0f}".format(x)+": "+s+'>')
	def documentStrings(self):
		"""
		print out all strings, 1 to a row
		"""
		print('--- PdfParagraph.documentStrings()---')
		for s in self.strings:
			print( type(s).__name__+' '+s.string)
	
class PdfFootnoteParagraph( PdfParagraph ):
	"""
	A subclass of PdfParagraph. Differs in that the
	indent, lead and tail are all set to 0. Does not call super __init__
	It has a new attribute: num the footnote number set when the 
	footnote is added to the chapter.
	
	
	"""
	def __init__( self, chapter):
		PdfParagraph.__init__(self, chapter)
		self.lead = 0
		self.tail = 0
		self.indent = 0
		self.num = None

		
class FixededPdfParagraph( PdfParagraph ):
	"""
	This subclass of PdfParagraph holds FixedPdfStrings. As such it is not
	subject to justification. It has the rule it must fit on a single PdfPage
	from its starting point. 
	Its addString() method accepts only FixedPdfString which already have their
	row and column set.
	"""
	def __init__(self, chapter):
		"""
		The initiator receives only the PdfChapter parameter. Lead and Tail must be
		set by methods setLead() and setTail()
		"""
		PdfParagraph.__init__(self, chapter)
		self.lead = 0
		self.tail = 0
		self.indent = 0
	def depth(self):
		"""
		The depth of a FixedPdfParagraph is the sum of the lead, the tail, and
		the maximum row value found among its strings.
		"""
		ret = 0
		for s in self.strings:
			ret = max(ret, s.row)
		return ret + self.lead + self.tai
	def addString(self, pstring):
		"""
		FixedPdfParagraph accepts ony FixedPdfString vales
		"""
		assert isinstance( pstring, FixedPdfString )
		self.strings.append( pstring )
		
class ImageParagraph( PdfParagraph ):
	"""
	A type of paragraph without lines - they only have images - 1 or a row - with 
	optional captions. BuildLines is a noop.
	
	Paragraph must fit on the page. see depth()
	
	"""
	def __init__(self, chapter , alignment = 'l', indent = 0, tail = 10 ):
		"""
		initializer. Calls parents.  alignment will be ignored. Position of images is
		absolute relative to its top.
		"""
		PdfParagraph.__init__(self, chapter , alignment, indent, tail)
		self.images = []
		self.height = 0
	def depth():
		return self.height + self.lead + self.tail
	def buildLines():
		pass
	def addImage(self, imageName, width, height, caption, xPos):
		dct = { "name": imageName, "width": width, "height": height, "caption": caption, "x": xPos}
		self.height = max(self.height, height)
		self.images.append( dct )
		
	