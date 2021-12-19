# PdfString.py

from PdfFontMetrics import PdfFontMetrics
from PdfTextFont import TextFont 
metrics = PdfFontMetrics()

class PdfString( object ):
	"""
	PDFString is a continuous bit of text in a common font. It may contain
	with a footnote identified as ^
	Attributes:
	self.fontkey
	self.fontsize
	self.string
	self.length
	"""

	def __init__( self, pfont, pstring):
		"""
		Initialize a new string, invoke setLength()
		"""
		#assert isinstance(pfont, TextFont)
		self.fontkey = pfont.name
		self.fontsize = pfont.size
		self.string = pstring
		
		self.setLength()
	@classmethod
	def repeater( cls, pFont, pString, slen ):
		"""
		Return a new instance of PdfString, with <pString> repeated as many
		times as necessary to be the maximum length that is less than
		or equal to <slen>. But at least one iteration
		"""
		s = pString
		un = cls( pFont, s)
		lun = cls( pFont,s)
		while un.length <= slen:
			un.setString( un.string + pString)
			if un.length <= slen:
				lun.setString( un.string)
		return lun
	
	def __str__(self):
		"""
		Override the string method. 
		{ F3, 8} L=nnn ::string::
		"""
		return '{ '+self.fontkey+' '+str(self.fontsize)+'} L='+str(self.length)+'::'+self.string+"::"
	def getFont(self):
		return TextFont( self.fontkey, self.fontsize )
		
	def ltrim(self):
		"""
		Remove leading spaces
		"""
		self.string = self.string.lstrip()
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
	def trim(self):
		"""
		remove trailing whitespace from string.
		Reset length
		"""	
		self.string = self.string.rstrip()
		self.setLength()

		
	def splitIntoWords(self):
		"""
		Divide the string into multiple strings, with each string containing a single word,
		and, often, associated spaces.
		1. If a string begins with one or more spaces, those spaces are placed into a single new
		string.
		2. If a group of non-space characters is followed by a space it is included with the word.
		3. If non-space characters are followed by more than one space, those other space characters
		will be treated by rule 1.
		Return value is a list of PdfString. For descendents of PdfString it just returns the original
		string in a list with 1 element.
		"""	
		rawlist = self.string.split(' ')
		retlist = []
		# example
		# "  123 345 6.  8 9 10. ".split(" ")
		# ['', '', '123', '345', '6.', '', '8', '9', '10.', '']
		# "  123 345 6.  8 9 10.".split(" ")
		# ['', '', '123', '345', '6.', '', '8', '9', '10.']
		# "  123 45 67.  89abcer fg.  ".split(" ")
		# ['', '', '123', '45', '67.', '', '89abcer', 'fg.', '', '']
		i = 0
		spaces = 0
		while i < len(rawlist):
			if len(rawlist[i]) == 0:
				# then this represents a single space character
				spaces = spaces + 1
			else:
				if spaces > 0:
					retlist.append( PdfString( self.getFont(), " " * spaces))
					spaces = 0
				if i < len(rawlist) - 1:
					appendage = ' '
				else:
					appendage = ''
				retlist.append( PdfString( self.getFont(), rawlist[i] + appendage))
			i = i + 1
		if spaces > 0:
			retlist.append( PdfString( self.getFont(), " " * (spaces- 1)))
			# print('T')
		return retlist
		
					
				
		
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
		This is useful when building lines with a fixed maximum length from one
		or more strings.
		"""
		#print ("in split2 with "+self.string)
		#print('length is '+str(self.length)+' amount to split ' + str(strLen))
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
				if nxtLen == 0:
					break
				elif newLen + nxtLen <= strLen:
					newStr += nxtStr
					newLen += nxtLen
					wrkStr = wrkStr[ wrkStr.find(' ')+1 :] 
					#print('newStr: '+newStr)
					#print('wrkStr: '+wrkStr)
				else:
					#print('Could not fit in' + str(nxtLen))
					break
			ret = PdfString( TextFont( self.fontkey, self.fontsize ) , newStr)
			ret.setLength()
			self.setString( wrkStr)
			
				
				
		
		return ret

	def stretch(self, amt):
		"""
		loop though self.string once, adding spaces to existing spaces, until
		the string has been traversed or each space has been padded once. So
		will not necessarily stretch the string to the full amount.	The <amt>
		to be added may be spread among multiple strings, so it only traverses once.
		"""
		spaceLen = metrics.strLength( self.fontkey, self.fontsize, ' ')	
		added = 0
		newStr = ''
		if amt < spaceLen:
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
		
class PdfStringSpacer( PdfString):
	"""
	a descendent of PdfString that serves as a spacer. Only real attribute is length. 
	It does require a font as a parameter to the initiator. It sets .string to
	a number of spaces equal to the desired lengt
	space = PdfStringSpacer( mainFont, 72 * 3)
	"""	
	def __init__(self, pfont, plength):
		slength = metrics.strLength( pfont.fontkey, pfont.fontsize, ' ')
		cnt = math.floor( plength / slength )
		txt = " ".replace(" "," "*cnt,1)
		PdfString.__init__(self,pfont,txt )
		self.length = plength
	def setLength():
		"""
		Overridden in PdfStringSpacer to be a nop; the length is specified in the
		initiator.
		"""
		pass
	def setString(self, t):
		"""
		reset the string property with <t> and invoke self.setLength()
		"""
		self.string = t
		self.setLength()
	def trim(self):
		"""
		pass
		"""	
		pass		
	def ltrim(self):
		"""
		pass
		"""
		pass	
	
		
	
	
			
class PdfStringFN( PdfString):
	"""
	This serves to identify a string as containing a footnote indicator, i.e. an integer value
	"""
	def __init__(self, pfont, pstring):
		"""
		just call the parent initiator
		"""
		PdfString.__init__(self, pfont,pstring)
	def splitIntoWords(self):
		"""
		Override parent method.
		Return a clone of self in a list with just 1 element
		"""
		ret = []
		ret.append( PdfStringFN( self.getFont(), self.string))
		return ret
		
	
class FixedPdfString( PdfString):
	"""
	A FixedPdfString is one with preset row and column values. It is inserted into FixedParagraphs
	and is not subject to justification.  Each string as a preset row and column value
	(in points). The row values are relative to the top (after lead) and left margins
	of the FixedPdfParagraph
	"""
	def __init__(self, prow,pocol,pfont,pstring):
		"""
		Initializer for a FixedPdfString. the row and column value are in points. The
		row is relative to the paragraph row, and the column relative to the paragraph
		left margin. They are held in FixedPdfParagraphs only,
		"""
		PdfString.__init__(self, pfont, string)
		self.row = prow
		self.col = pcol
	def splitIntoWords(self):
		"""
		Override parent method
		Return a clone of self in a list with just 1 element
		"""
		ret = []
		ret.append( PdfString( self.getFont(), self.string))
		return ret
			
