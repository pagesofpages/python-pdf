# PdfTextFont.py
"""
Contains class TextFont
"""
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
		Properties are
		self.name
		self.size
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
		return TextFont( self.name[0:2]+'B', self.size)	
			
	def asNormal(self):
		"""
		Return a copy of self as a plain font, not italic or bold
		"""
		return TextFont( self.name[0:2], self.size)	
			
	def asBoldItalic(self):
		"""
		return a copy of the current font face as bold and italic
		"""
		return TextFont( self.name[0:2]+'IB', self.size)	
