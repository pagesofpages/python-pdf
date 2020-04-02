import io
import os
import json

'''
[
	{ "key": "F2", "chars" : []
]
	

'''


class PdfFontMetrics( object):
	"""
	PdfFontMetrics loads detailed character-specific size information for
	the built-in variable fonts in a standard version 1.2/1.3 pdf file:
	Helvetica regular, oblique, bold, and bold-oblique: F2 F2I F2B F2IB
	Times regular, oblique, bold and bold-oblique (or italic) F3 F3B F3I F3IB
	These sizes can be used as the basis for calculating a string length
	for the proportional fonts.
	
	It can be used to replace the strLength method of the PdfDocument class, when more
	precise string lengths are needed.  There are no cross-dependencies between the 
	two classes.
	
	This class depends upon a json file: pdfFontMetrics.json, which has the structure:
	[
		{ "key": "F2", "chars" : 
			[
				...
				{"char": " ", "width": 278 }, 
				{ "char": "!",  "width": 278 }, 
				...
			]
		}
		...
	]
	This "chars" contains 133 elements, but is populated only for the standard ascii
	characters.  The entry for the space character, ascii 32, is at chars[32].
	
	If a character is out of range then the default character width of 600 is used. 
	
	Standard use is simply:
	
	from PdfFontMetrics import PdfFontMetrics
	metrics = PdfFontMetrics()
	sizeInPoints = metrics.strLength( 'F2',14,'Four score and seven years ago...')
	
		
	
	
	
	"""
	def __init__(self):
		"""
		Calls readFontMetrics to load the font data.
		"""
		self.defaultCharWidth = 600
		self.fileName = '/Users/garymenchen/python/pdf/pdfFontMetrics.json'
		self.fonts = []
		self.readFontMetrics()
		
	def findFont(self, pFontKey):
		""" Internal function used to extract data for a specific font """
		vReturn = None
		for font in self.fonts:
			if font['key'] == pFontKey:
				vReturn = font
				break
		return vReturn

	def addChar( self, pFontKey, pAscii, pChar, pWidth):
		""" Internal function used when maintaining the json file """
		font = self.findFont( pFontKey )
		if font is None:
			dict = {}
			dict['key'] = pFontKey
			l = []
			for i in range(0,132):
				l.append( None)
			dict['chars'] = l
			self.fonts.append( dict )		
		font = self.findFont( pFontKey )
		assert font is not None, 'What happened with font ' + pFontKey
		font['chars'][pAscii] = { "char": pChar, "width": pWidth } 
		
	def readFontMetrics(self):
		""" Internal function called by the __init__ method """
		with open( self.fileName ) as json_file:
			entries = json.load( json_file )
			self.fonts = entries
			
	def writeFontMetrics(self):
		""" Internal function used when maintaining the json file """
		entries = self.fonts
		with open( self.fileName, 'w') as outfile:
			json.dump( entries, outfile, indent=2)
			

	def strLength(self, pFontKey, pFontSize,  pString):
		"""
		strLength calculates the length of a string, in pdf document points. So it
		(a) Sums the lengths of the individual characters in <pString>
		(b) Multiplies by <pFontSize>
		(c) Divides by 1000.
		And returns that result.
		If a font is not identified, or if a character has no entry, then the default
		character width is used.
		"""
		vReturn = None
		font = self.findFont( pFontKey )
		if font is None:
			vReturn = len( pString) *  ( self.defaultCharWidth ) 
		else:
			vReturn = 0
			for s in pString:
				if ord(s) <= len(font['chars']) and font['chars'][ord(s)] is not None:
					vReturn = vReturn +font['chars'][ord(s)]['width']
				else:
					vReturn = vReturn + self.defaultCharWidth
		return vReturn * pFontSize / 1000.0



