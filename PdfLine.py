# PdfLine.py

from PdfString import PdfString, PdfStringFN


class PdfLine( object):
	"""
	# a PdfLine is a collection of strings that are to be output on the same row.
	Properties
		row 
		col
		strings []
		length
	
	"""
	def __init__(self,  prow = None, pcol = None):
		"""
		properties
		self.row
		self.col the left most position of the line.
		self.strings = [] A collection of strings.
		self.length = 0  calculated after each change
		"""
		self.row  = prow
		self.col = pcol
		self.strings = []
		self.length = 0
		
			
		
	def setPos( self, r, c):
		"""
		Set self.row and self.col
		"""
		self.row = r
		self.col = c

		
	def addString(self, pString):
		"""
		add a PdfString to self.strings, and reset self.length. If this is the first string
		then remove leading spaces.
		"""
		assert  isinstance(pString,PdfString), "Expectring PdfString found "+ str(pString)
		if len(self.strings) == 0:
			pString.ltrim()
			
		self.strings.append( pString)
		self.length += pString.length
	
	def setLength(self):
		self.length = 0
		#if len(self.strings) > 0:
		#	self.strings[0].ltrim()
		for s in self.strings:
			self.length += s.length
			
			
	def depth(self):
		"""
		depth is the maximum height found in strings
		Without adjustment for space between lines (lineheightFactor). So it is the
		largest size of any fonts in the line strings []
		"""
		ret = 0
		for s in self.strings:
			ret = max(ret, s.fontsize)
		return ret
		
	def footnoteList(self):
		"""
		Return a list of the int values of the footnote indicators in the current line.
		A footnote will be of type PdfStringFN, and its content will be digits that can
		convert to int.
		"""
		ret = []
		for s in self.strings:
			if isinstance(s, PdfStringFN) :
				# print( 'found footnote '+s.string)
				assert s.string.isdigit()
				ret.append( int( s.string ))
		return ret
		
	def dump(self):
		# print out the combined strings in this line, each PdfString separated by ::
		p = ''
		for s in self.strings:
			p += s.string+'::'
		print( p )
		
	def dumpline(self):
		"""
		return the concatenated strings
		"""
		r = ''
		for s in self.strings:
			r = r   + '<' + s.string + '>'
		return r
		
	def printPdf(self, doc):
		"""
		print the line of text using the <doc> PdfDocument methods
		The row and column are calculated here.
		Column is the current column set in the line initiator or by line.setPos
		Row is the same, except an offset of -3 is set if it is a footnote. (why?)
		Column represents the left-most position of the line. So this might be
		fudged for mirroring margins (i.e. larger gutter, shorter outer margin)
		self.doc is a PdfDoc. doc.getPageNumber() returns the current page number.
		If page is odd then gutter is left margin; even then gutter is right margin.
		"""
		r = self.row
		c = self.col
		for s in self.strings:
			doc.setFont( s.fontkey,s.fontsize)
			#chapter.pdf.setFont( l.fontkey, l.fontsize )
			#chapter.pdf.write(chapter.pcol, chapter.prow , l.string, 'l','p')
			if isinstance(s, PdfStringFN):
				offset = -3
			else:
				offset = 0
			doc.write( c, r + offset, s.string,'l','p')
			c += s.length
		# document the line width - for testing
		# doc.writeCol( doc.getRightColumn('p'),f"{self.length:.4}",'r','p')
		# doc.writeCol(  doc.getRightColumn('p'), f"{self.wordCount():4}",'r','p')
	def wordCount(self):
		"""
		return the number of "words" - contiguous non-space characters bounded by
		either a beginning, an end or a space - in a line
		"""
		ret = 0
		ln = ''
		for s in self.strings:
			ln += s.string
		# now one single string.
		# every encounter with a character when no already in a word increments counter
		ctr=0
		inword = False
		for c in ln:
			if c != ' ' and not inword :
				ctr = ctr + 1
				inword = True
			elif c == ' ' and inword :
				inword = False
		return ctr
	def splitStrings(self, cnt ):
		"""
		This  splits a line into at least cnt strings if it can.
		"""
		
		gap = cnt - len(self.strings)

		while gap > 0:
			strs = []
			orig_gap = gap
			for s in self.strings:
				p = s.string[1:-1].find(" ")
				if p > 0 and gap > 0:
					strs.append( PdfString( s.getFont(), s.string[0:p+2]))
					strs.append( PdfString( s.getFont(), s.string[p+2:]))
					gap = gap - 1
				else:
					strs.append( s )
			self.strings = strs
			if gap == orig_gap:
				break
		self.setLength()
	def stretch( self, targetLength ):
		"""
		Stetch the line until length is target length. Used for justification.
		"""
		# print ('Stretching '+ self.dumpline() +' Current length '+str(self.length)+' target length '+str(targetLength))
		
		newStrings = []
		for s in self.strings:
			newStrings = newStrings + s.splitIntoWords()
		self.strings = newStrings
		self.setLength()			
		gap = targetLength - self.length
		# count the number of strings that are not footnotes, and subtract 1 (for the end)
		cnt = 0
		for s in self.strings:
			if type(s).__name__ == 'PdfString':
				cnt = cnt + 1
		if cnt <= 1:
			pass
		else:
			# adjust the length of all strings except the last, and except if followed
			# by a footnote
			# it might be negative if gap < 0. 
			
			adjustment = round( gap / (cnt - 1 ) ,2)
			for i in range(0, len( self.strings) - 1):
				if type(self.strings[i+1]).__name__ == 'PdfStringFN':
					pass
				else:
					self.strings[i].length += adjustment

		
		#while gap > 2.4:
		#	for s in self.strings:
		#		s.stretch(gap)
		#		# what is the new gap
		#		self.setLength()
		#		gap = targetLength - self.length
		#		if gap < 2.4:
		#			break
		#gap = int(targetLength) - int(self.length)
		
		

		#if gap >= 1 and self.wordCount() >= 2:
		#	# print('Using gap of '+str(gap))
		#	#print( str(gap) + " length incoming "+str(self.length))
		#	# self.dump()
		#	self.splitStrings( gap + 1 )
		#	
		#	#print('Length of strings '+str(len(self.strings)))
		#	if len(self.strings) > gap:
		#		# print( 'Strings '+str(len(self.strings))+' Gap '+str(gap))
		#		for i in range(0,gap ):
		#			self.strings[i].length += 1
		#		self.setLength()
		#	#print("Length outgoing "+str(self.length))		
		
			
		# print('Length is now '+str(self.length))
"""


from PdfChapter import TextFont
from PdfString import PdfString
from PdfLine import PdfLine
ln = PdfLine()

ln.addString( PdfString( TextFont('F3',8),"This is a test. " ))
ln.addString( PdfString( TextFont('F3I',8)," And so is this."))

print('Line length is '+ str(ln.length))
print('Line Word Count is '+str(ln.wordCount()))
print('Line text is ' + ln.dumpline())
print('Splitting into 5 strings')
ln.splitWords(5)
print('Line length is '+ str(ln.length))
print('Line Word Count is '+str(ln.wordCount()))
print('Line text is ' + ln.dumpline())

"""