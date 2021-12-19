# PdfPage.py
"""
PdfPage is a single printable page. 
"""



class PdfPage(object):
	"""
	a single printable page. A container for a list off PdfLines().
	"""	
	def __init__(self, chapter ):
		"""
		only property is lines []
		"""
		self.lines = []
	def addLine( self, prow, ln):
		"""
		Add a PdfLine to the page list of lines, setting the line.row at the same time
		<ln> is a PdfLine
		"""
		ln.row = prow
		self.lines.append( ln )
	def dumpPage(self):
		"""
		debugging aid: print contents to console.
		"""
		for ln in self.lines:
			s = ''
			for st in ln.strings:
				s += st.string
			print( str(ln.row)+','+str(ln.col)+': '+s)
		
