#! PdfDoc.py
#! classes for pdf generation
import datetime
import binascii

#! point class for internal use only
class _point( object ):
	"""
	#! initialize with 2 numeric values, presumably an xy coordinate.	
	"""
	def __init__( self, x, y):
		self.x = x
		self.y = y
		
	def __str__(self):
		return '(x:'+str(self.x)+',y:'+str(self.y)+')'

#! pdfFont maintains a few attributes for each font. See PdfFontMetrics for more
#! detailed information.		
class PdfFont( object ):

	# <key>: F1 though F5 are the keys to the built-in fonts, assigned by Adobe
	def __init__( self, key, name, pFixedOrVar, pAvgSize):
		""" Very minimal information on fonts.
		Attributes:
			key = <key>
			name = <name>
			fixedOrVar = <pFixedOrCar>
			aveSize = <pAgeSize>
		"""
		self.key = key
		self.name = name
		self.fixedOrVar = pFixedOrVar
		self.avgSize = pAvgSize
		
class PdfPage( object ):
	""" 
	Data structure for a single page. Do not have multiple pages in progress
	at the same time. Some methods should be moved to this class.
	Attributes:
		pageObjNo = 0
		streamObjNo = 0
		sizeObjNo = 0
		parentOjbNo = 0
		pageNo = 0
		fontList = ''
		xObjectList = ''
		graphicsStream = []
		name = ''
		textStream = []
	"""
	def __init__(self):
		self.pageObjNo = 0
		self.streamObjNo = 0
		self.sizeObjNo = 0
		self.parentObjNo = None
		self.pageNo = 0
		self.fontList = ''
		self.xObjectList = ''
		self.graphicsStream = []
		self.name = ''
		self.textStream = []

class XObject( object):
	""" data structure for an XObject - which is a lot like a page, but
		may have different dimensions, and may be used multiple times. 
	Attributes:
		name = ''
		objectNo = 0
		width = 0
		height = 0
		device = []
		imageLib = ''
		imageMask = ''
	
	"""
	def __init__(self):
		self.name = ''
		self.objectNo = 0
		self.width = 0
		self.height = 0
		self.device = ''
		self.imageLib = ''
		self.imageMask = ''


class PdfDocument( object ):
	"""
	PdfDocument is the main class for dynamically generating pdf documents
	Output is assumed to be a file (they could be distributed by other means
	such served to a web browser, sent as email attachments, and so on.)
	
	A minimal pdfdocument can be generated with:
	
	from PdfDoc import PdfDocument
	doc = PdfDocument()
	doc.beginDoc("hello_world.pdf")
	doc.newPage()
	doc.setTextState()
	doc.write(30,20,'Hello World','l','r')
	doc.endPage()
	doc.endDoc()
	
	Output will be found in hello_world.pdf
	
	The main public-facing methods are below.
	
	Document Control
	beginDoc(self,  name = None)
	endDoc(self)
	getFileName(self)
	setFileName(self, pName)

	
	Page Control
	newPage(self)
	endPage(self)
	setTextState(self, pCharSpace = 0, pWordSpace = 0, pScale = 100, pLeading = 0, pRender = 0, pRise = 0):
	( the methods below are optiona, for overriding default values.)	
	setPageNumber(self, pNumber)
	getPageNumber(self)
	setPageSize( self, pHeight, pWidth, pUnits = None)
	getLeftMargin(self, pUnit = None)
	setLeftMargin(self, pMargin, pUnit = None)
	setRightMargin(self, pMargin, pUnit = None)
	getRightMargin(self, pUnit = None)
	getRightColumn( self, pUnit = None)
	setTopMargin(self, pMargin, pUnit):
	getTopMargin(self, pUnit = None):
	setBottomMargin(self, pMargin, pUnit = None):
	getBottomMargin(self, pUnit ):
	


	
	Text Output Procedures
	write( self, pX, pY, pString, pAlign = 'l', pUnit = None)
	writeOut( self, pString)
	writeNext(self, pX, pString, pAlign = 'l', pUnit = None)
	writeCol(self,  pX, pString, pAlign = 'l',pUnit = None)
	writeCenteredInLine( self, pY, pString, pUnit = None)
	waterMark(self, pText):


	Font Control
	The font families are [F1: Courier] [F2: Helvetica] [F3: Times-Roman]
	
	setDefaultFont(self, pFontKey, pFontSize)
	findFontByKey(self, pFontKey)
	getFontKey(self, pFontName)
	setFont(self, pFontKey, pFontSize)
	setCharWidth( self, pPoints )
	setLineHeight( self, pHeight, pUnit = None)
	getLineHeight(self, pUnit = None)
	setLineHeightFactor( factor )
	setCharWidthFactor( factor )
	-- save and restore font, setting aw font at the same time.
	-- uses a stack, self.fontStack
	pushFont( pFontKey, pFontSize)
	popFont()
	
	

	xObjects
	newFormXObject( self, pName)
	endFormXObject(self)
	showForm(self,  pName):
	findXObject(self, pName):

	Images
	defineImageXObject( self, hexStrings, pName, pWidth, pHeight, pBitsPerComponent, pColorSpace = None, pImageMask = None, pImageLib = None, pFilter = None):
	showImage(self, pName, pX, pY, pUnit = None, pScaleX = None, pScaleY = None, pSkewX = 0, pSkewY = 0, pGrayScale = 0):
	readImage(self,  name):
	

	Graphics
	setGrayScale( self, pScale = 0)
	shade( self, pX1, pY1, pX2, pY2, pScale = 0.9, pUnit = None)
	grayBar( self, pY, pUnit = None)
	drawLine( self, pX1, pY1, pX2, pY2, pUnit = None, pWidth = None)
	rectangle( self, pX, pY, pWidth, pHeight, pUnit = None, pLineWidth = None)
	lineAcrossPage(self, pY, pUnit = None)
	verticalPageLine(self, pX, pUnit = None)
	pageBorder(self)
	ellipse(self, pX, pY, pRadiusX, pRadiusY, pUnit = None, pLineWidth = None)

	Positioning
	
	PDF Documents use "points" for positioning within a page. A point is 1/72nd of an
	inch. Internally points are relative to the bottom left of the sheet of paper.  Inside
	this class positioning is done relative to the top left of the sheet of paper, and
	the y coordinate is converted behind the scenes. 
	
	Many methods have a <pUnit> parameter; this identifies what unit of measurement is to be
	used. Values are 
		p: point  
		r or c: row or column, basically interchangeable,  
		i: inch
		m: millimeter
	
	While it may be convenient to use rows and columns for positioning, bear in mind that
	the meaning of row and column changes whenever the current font is changed.  If 
	generating forms it will be necessary to use one of the absolute units of measurements,
	such as inch or millimeter or point.
	
	Different units of measurement can be used at will.
	
	The internal values for the current position are always stored in points.
	
	setDefaultUnit( self, pUnit)
	getDefaultUnit(self)
	convertUnits(self, pUnits, pFrom, pTo)
	getCurrentRow(self, pUnit = None)
	getCurrentCol(self, pUnit = None)
	setCurrentRow(self, pValue, pUnit = None)
	setCurrentCol(self, pValue, pUnit = None)
	getFreeRows(self)
	setLineHeight( self, pHeight, pUnit = None)
	getLineHeight(self, pUnit = None)
	strLength(self, pFontKey, pFontSize, pString)
	getBottomRow(self, pUnit = None)
	getRightColumn(self, pUnit = None)







	
	"""

	#! a PdfDocument
	def __init__(self):
		"""
		__init__ sets a large number of attributes to default values, and loads
		basic information about the default fonts F1, F2 and F3 with I, B, and IB flavors.
		Attributes.
		fileName  - the name of the pdf file to be generated. Set by the beginDoc method
		currentFontKey  default F1
		currentFontSize  default 12
		defaultUnit 'p' 
		-- All the internal setting below are in points. All have get and set methods.
		lineHeight   
		charWidth    
		pageHeight 11 * 72 
		pageWidth 8.5 * 72
		topMargin 0.4 * 72
		leftMargin 0.4 * 72
		rightMargin 0.4 * 72
		bottomMargin 0.4 * 72
		
		"""
		self.currentFontKey   = 'F1'
		self.currentFontSize  = 12
		self.fontStack = []
		#! Note setting of defaultUnit.
		self.defaultUnit      = 'p'   	#-- default unit of measurement
                                    # p point, r row c col,i inches
		self.output = 1
		self.offset  = 0,           # tracks position in overall stream
		self.currentPageNo  = 0       # physical page number
		self.nextObjNo  =  1         # next available object number 
		self.currentParentNo  = 3    # parent object# of current page
		self.page = None                     # Current page a PdfPage Objec
		self.name = None              # File Name, etc
		self.lineHeightFactor = 1.25  # multiply ties fontSize for lineHeight in points.
		self.charWidthFactor = 1.1  # 
		self.lineHeight  = 11      # average line height,current font, in points  
		self.charWidth  = 7.1      # average character width,current font, in points
		self.pageHeight  = 11 * 72 # page height is in points
		self.pageWidth  = 8.5 * 72 # page width is in points
		self.topMargin  = 0.4 * 72    #  starting point. Rows are relative to top margin.
		self.leftMargin  = 0.4 * 72  # Columns are relative to this point.
		self.rightMargin  = 0.4 * 72   # typical non-printable area
		self.bottomMargin  = 0.4 * 72
		self.handle = None	#file handle
		self.target = None              # email address, etc
		self.pageObjList = []    # Table of Number ObjectNumberTable,
		self.pageParentList = []  # ObjectNumberTable,
		self.fontKeyList = []		# RegisteredFontKeys,
		self.fontObjNoList = []  # ObjectNumberTable,
		#-- components for cross reference table
		self.xRefOffset = []	# OffsetTable table of number(10),
		self.xRefLabel= []		#  XRefLableTable table of varchar2(25),
		self.fileName = None
		self.currentRow = None      # INTERNAL USE: Current Y position, in points
		self.currentCol = None      # INTERNAL USE: Current X positon, in points
		self.currentState = None      # INTERNAL USE, tracking status of document numer(1)
		
		self.pvFontTable = []
		self.pvXObjectTable = []
		# add the available fonts
		self.addFont('Courier','F1','F',600)
		self.addFont('Courier-Bold','F1B','F',600)
		self.addFont('Courier-Oblique','F1I','F',600)
		self.addFont('Courier-BoldOblique','F1IB', 'F', 600)
		self.addFont('Helvetica','F2','V', 583)
		self.addFont('Helvetica-Bold','F2B','V',613)
		self.addFont('Helvetica-Oblique','F2I','V', 583)
		self.addFont('Helvetica-BoldOblique','F2IB','V',613)
		self.addFont('Times-Roman','F3','V', 563)
		self.addFont('Times-Bold','F3B','V',597)
		self.addFont('Times-Italic','F3I','V', 538)
		self.addFont('Times-BoldItalic','F3IB','V', 565)
		self.addFont('Symbol','F4','F',600)  # don't really care
		self.addFont('ZapDingbats','F5','F',600)
		
		
		
  
		
	#! resolveUnit is primarily to deal with the context-sensitive values of r and c
	#! i.e. row and column. A point is a point, an inch is an inch, but a row and a 
	#! column, used together, translate into different point values.	
	#R Return <pUnit> unless <pUnit> is r or c and <pContext> is the other part of the 
	#!  r|c pair.
	#! if <pUnit> is None then it is set to self.defaultUnit
	def resolveUnit(self, pUnit, pContext):
		""" 
		Primarily to deal with the mixed use of r and c, and the conversion to and from
		row/column coordinates and the other units of measurement. If pUnit is None then
		self.defaultUnit is used.
		
		"""
		if pUnit is None:
			vUnit  = self.defaultUnit
		else:
			vUnit = pUnit
		if vUnit in [ 'r','c' ]:
			if pContext in [ 'r','c' ]:
				vUnit = pContext
		return vUnit
		
	def getLineWidth(self, pUnit = None):
		"""
		get the page size minus left and right margins. Return in the
		current default unit of measure unless <pUnit> is specified. 
		Returns the width of a line, which is
		the page with with minus left and right margins.
		"""
		vUnit = self.resolveUnit(pUnit,'c')
		vReturn = self.pageWidth - self.leftMargin - self.rightMargin
		vReturn = self.convertUnits(vReturn,'p',vUnit)
		return vReturn
		
	def getNextObjNo(self):
		"""
		Primarily internal use.
		Returns the next available object number. Maintains a counter for the PdfDocument
		instance, and increments it after each call.
		"""
		vReturn = self.nextObjNo
		self.nextObjNo = self.nextObjNo + 1
		return vReturn
		
	def put( self, pMessage):
		"""	
		put writes out a string to the ongoing textStream. Strips leading and trailing spaces
		does encoding to 'ascii' (???), appends '\r\n' to the end, (per pdf specs)
		and updates an offset attribute with the total output length.
		Outfacing methods such as write make use of put.
		Seealso: putAsIs()
		"""
		vMessage = pMessage.strip()
		vLength = len(vMessage)+ 2
		# writing to a file
		self.handle.write( vMessage.encode('ascii') +  b'\r\n')
		self.offset = self.offset + vLength 

	def putAsIs( self, pMessage):
		"""
	  	put with no encoding, does not strip leading or trailing whitespace.
		can be used to output binary strings (such as a bytearray)
		Seealso: put()
		python3 issues
		"""
		self.handle.write( pMessage )
		self.offset = self.offset + len( pMessage )
	
	#! this is an internal function.   				
	#! <pNum> is the object number
	#! <offset> is the offset from the start of the file
	#! <pLabel> is, I think, unused. Originated as a debugging aid
	# ord pos is pNum - 1, 
	#! these can be added in any sequence
	#! number 2 goes in [1] because lists start at 0
	def addxRef(self, pNum, pOffset, pLabel):
		while len(self.xRefOffset) < pNum:
			self.xRefOffset.append(None)
		while len(self.xRefLabel) < pNum:
			self.xRefLabel.append(None)
		pOrd = pNum - 1
		self.xRefOffset[pOrd] = pOffset
		self.xRefLabel[pOrd] =  pLabel
		# debug point here		

	#! registers a font for use in the document. Ok to call
	#! multiple times.
	#R returns the font's index in the document fontOjbNoList list.
	def registerFont(self, pFontKey):
		""" internal use 
		Writes sufficient font information to the pdf file for the font to be usable.
		"""
		vPtr = -1
		if len(self.fontKeyList) > 0:
			for i in range(0, len(self.fontKeyList)):
				if self.fontKeyList[i] == pFontKey:
					vPtr = i
		vFontPtr = None
		if vPtr == -1:
			# then the font has not been registred
			vFontPtr = self.findFontByKey( pFontKey)
			assert vFontPtr > -1,'Invalid font key '+ pFontKey
			self.fontKeyList.append( pFontKey )			
			vPtr = len( self.fontKeyList) - 1
			self.fontObjNoList.append( self.getNextObjNo())
			self.addxRef( self.fontObjNoList[-1], self.offset,'font')
			self.put(str(self.fontObjNoList[vPtr]) + ' 0 obj')
			self.put('<< /Type /Font')
			self.put('   /Subtype /Type1')
			self.put('   /Name /' +  self.fontKeyList[vPtr])
			self.put('   /BaseFont /' + self.pvFontTable[vFontPtr].name)  # ; -- Courier');
			self.put('   /Encoding /WinAnsiEncoding');
			self.put('>>');
			self.put('endobj');
		vObjectNo = self.fontObjNoList[vPtr]
		return vObjectNo   
		
	def setDefaultFont(self, pFontKey, pFontSize):
		""" set the currentFontkey and currentFontSize attributes of the PdfDocument 
		.. seealso:: setFont()
		"""
		self.currentFontKey = pFontKey
		self.currentFontSize = pFontSize
		
	def writeHeader( self ): 
		""" write the beginning of the pdf file. Writes the current date to the header,
		and my name as well.
		"""
		_vBucket = 0
		self.offset = 0
		self.put('%PDF-1.2')

		#  -- Try some high order bytes on the second line. This is a convention
		#  -- to prevent some programs from treating this as an ascii text file,
		#  -- and possibly converting eol characters
		bytes = bytearray([ 37, 37,  25, (15 * 16) + 2, (15 * 16) + 3, (13 * 16) + 15, (14 * 16 ) + 3, 13, 10])
		#self.put('%%'+chr(25)+chr((15*16)+2)+chr((15*16)+3)+chr((13*16)+15) + chr( (14 * 16) + 3)) 
		self.putAsIs( bytes )
		#self.put('%%')
		#  -- Write the catalog. Pages in object 3
		self.addxRef(1,self.offset,'Catalog')
		self.put('1 0 obj')
		self.put('<<')
		self.put('/Type /Catalog')
		self.put('/Pages 3 0 R')
		self.put('/Outlines 2 0 R')
		self.put('>>')
		self.put('endobj')
		self.addxRef(2,self.offset,'Outlines')
		self.put('2 0 obj')
		self.put('<<')
		self.put('/Type /Outlines')
		self.put('/Count 0')
		self.put('>>')
		self.put('endobj')
		#-- add a procset
		self.addxRef(4,self.offset,'ProcSet')
		self.put('4 0 obj')
		self.put('  [/PDF /Text /ImageB /ImageC]')
		self.put('endobj')
		# -- Add some information
		self.addxRef(5,self.offset,'General Info')
		self.put('5 0 obj')
		self.put('<<')
		self.put('/CreationDate (D:' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + ')')
		self.put('/Author (Gary Menchen)')
		self.put('/Producer (Gary Menchen''s PDF Code)')
		self.put('>>')
		self.put('endobj')
		self.nextObjNo  = 6


	def writePages(self, pObject, pParent = None):
		"""
		Internal use.
		#-- Goal is to have about 6 page objects as children of a page object.
		#-- The parent number is assigned to each /page object by the GetNewPage
		#-- function. For each page.parentobj# value we write a single /pages object,
		#-- write the /Page object numbers to the kids list,and, if we are not at
		#-- the end of the list of page objects, add the parentobj# of the subsequent
		#-- page. As a result each /Pages object will have a kids list that contains
		#-- up to 6 /Page objects.  The kids list will end with a reference to another
		#-- /Pages object if we are not at the end of the list of /Page objects.
		#  -- Note that the parameters after pDoc are not used.
		"""
		vParent = None
		vObject = None
		i  = None
		vLine = ''
		vPageCtr  = 0 #-- number of /page objects listed in a /pages object
		vTotalPages = len( self.pageObjList )
		i = 0
		while i  < len(self.pageObjList):
			#-- begin the pages object
			vObject = self.pageParentList[i]
			self.addxRef(vObject,self.offset,'Pages')
			self.put(str(vObject) + ' 0  obj')
			self.put('<< /Type /Pages')
			if i > 0: 
				self.put('/Parent ' + str(vParent)+ ' 0 R')
			vLine = '/Kids ['
			vPageCtr = 0
			while i <    len(self.pageObjList) and vObject == self.pageParentList[i]:
				vLine = vLine + str(self.pageObjList[i]) + ' 0 R '
				vPageCtr = vPageCtr + 1
				i = i + 1;
			#	-- Check if we need to add a /Pages object to the end of the kids list
			if i < len(self.pageObjList) :
				vLine = vLine + str(self.pageParentList[i]) + ' 0 R '
				vParent = vObject
			# --'Parent changed to ' || to_Char(vParent));
			vLine = vLine + ']'
			self.put( vLine)
			self.put( '/Count ' + str(vTotalPages))
			self.put('>>')
			self.put('endobj')
			vTotalPages = vTotalPages - vPageCtr
		# end of main loop
	# end writePages
	
	def writexRef(self):
		"""
		
		#! write the cross-reference table and the trailer at the end of the document
		"""
		self.writePages(3,None)	
		vOffset = self.offset
		self.put('xref')
		vNext = self.getNextObjNo()
		self.put('0 ' + str(vNext))
		self.put( str(0).zfill(10)  +' '+str(65535).zfill(5)+' f' )

		for i in range(0, len(self.xRefOffset) ):
			self.put( str( self.xRefOffset[i]).zfill(10) +' '+str(0).zfill(5)+' n')

		self.put('trailer')
		self.put('<< /Size ' + str(vNext))
		self.put('   /Root 1 0 R')
		self.put('   /Info 5 0 R')
		self.put('>>')
		self.put('startxref')
		self.put(str(vOffset))
		self.put( '%%EOF')


	def checkMeasurementUnit(self, pUnit):
		""" validate the unit of measurement: r, c, i, p or m """ 
		assert pUnit in [ 'r','c','i','p','m'],'Invalid Unit :'+ pUnit+':'
	

	def addFont( self, fontName, fontKey, pFixedOrVar, pAvgSize):
		""" add a font to the pvFontTable attribute. Primarily for internal use. """
		font = PdfFont( fontKey, fontName, pFixedOrVar, pAvgSize )
		self.pvFontTable.append( font  ) 


	def beginDoc(self,  name = None):
		""" 
		Initialize a new document. In general <name> should be passed as a parameter.
		This method opens the output file for writing. If name is not passed as a parameter,
		and the attribute has not been previously set, then an error will be generated.
		seealso: setFileName(self, pName)
		"""
		if name is not None:
			self.fileName = name
		assert self.fileName is not None
		# open the file
		self.handle = open( self.fileName,'wb')
		self.writeHeader(  )
		self.setDefaultFont('F1',10)

	def endDoc(self)	:
		""" after all pages are ended. Finish the document, close the file """
		self.writexRef()
		self.handle.close()	
		
	def getFileName(self):
		""" Return the name of the file. appends .pdf if no extension has been specified."""
		if self.fileName is None or len(self.fileName) == 0:
			vReturn = 'pdftest.pdf'
		else:
			vReturn = self.fileName
		if not '.' in vReturn:
			vReturn = vReturn  + '.pdf'
		return vReturn
		
	def setFileName(self, pName):
		""" set the fileName attribute 
		"""
		self.fileName = pName
		

	def newFormXObject( self, pName, pWidth = 8.5 * 72, pHeight = 11.0 * 72, pUnit = 'p'):
		""" 
		Generates a new XObject and appends to the pvObjectTable list.
		An XObject may be moveable, depending upon the relationship between
		the /BBox bounding box and the tm text Matrix.
		Positioning in an XObject must be within the bounds of the /BBox.
		Currently the /BBox is 0 0 :pWidth: :pHeight:
		seealso: endFormXObject()
		"""
		vPage = PdfPage()
		vPage.name = pName
		vPage.pageObjNo = self.getNextObjNo()
		
		vUnit = self.resolveUnit(pUnit, 'c')
		vWidth = self.convertUnits( pWidth, vUnit, 'p')
		vUnit = self.resolveUnit(pUnit, 'r')
		vHeight = self.convertUnits(pHeight, vUnit,'p')
		
		# use of XForm object is in transition
		vObject = XObject()
		vObject.name = pName
		vObject.objectNo = vPage.pageObjNo
		vObject.width = vWidth
		vObject.height = vHeight
		vPage.width = vWidth
		vPage.height = vHeight
		
		
		
		self.pvXObjectTable.append( vObject )
		self.page = vPage
		self.setFont( self.currentFontKey, self.currentFontSize)
		self.currentRow = 0
		self.currentCol = 0


	def newPage(self):
		"""
		Initialize a new page - required for each page of output.
		Tracks the page hierarchy, internally.
		"""
		vPage = PdfPage()
		vPage.pageObjNo = self.getNextObjNo()
		vPage.streamObjNo = self.getNextObjNo()
		vPage.sizeObjNo = self.getNextObjNo()
		self.currentPageNo = self.currentPageNo + 1
		vPage.pageNo = self.currentPageNo
		
		self.pageObjList.append( vPage.pageObjNo  )

		vPtr = len(self.pageObjList)
		if vPtr % 6 == 0:
			# switch to a new parent
			self.currentParentNo = self.getNextObjNo()
		self.pageParentList.append( self.currentParentNo ) 
		vPage.parentObjNo = self.currentParentNo
		# I don';t think there is a good reason for the font, and the row/col
		# information to be attributes of the document instead of the page
		self.page = vPage;    
		self.setFont( self.currentFontKey,self.currentFontSize)
		self.currentRow = 0;
		self.currentCol = 0;  

	def endFormXObject(self):
		"""
		End an XObject - much like a page must be ended
		Adds an entry to the xref table for the xobject, via addxRef()
		writes out the actual xobject form entry
		writes aout any graphics stream
		writes out any textstream
		"""
		self.addxRef(self.page.pageObjNo, self.offset,'For Xobject '+self.page.name)
		self.put(str(self.page.pageObjNo) + ' 0 obj')   
		self.put('<</Type /XObject')
		self.put('  /Subtype /Form')
		self.put('  /FormType 1')
		# 792 612 is the outer dimension of a standard page
		t = '[ 0    0    '+str(self.page.height)+'   '+str(self.page.width )+ ' ]'
		self.put('  /BBox ' + t )
		self.put('  /Matrix [1   0   0   1   0   0  ]')
		self.put('  /Resources << /Procset [ /PDF ] ')
		self.put('  /Font << ' + self.page.fontList +' >>')
		self.put('>>');

		vLen = 0
		if len(self.page.graphicsStream) > 0:
			for s in self.page.graphicsStream:
				vLen = vLen + len(s) + 2
		for s in self.page.textStream:
			vLen = vLen + len(s) + 2
			
		vLen = vLen + 8 #-- For Begintext and endtext (2/6 changed from 6)
		self.put('  /Length ' + str(vLen))
		self.put('>>');
		self.put('stream')
		if  len(self.page.graphicsStream) > 0:
			for s in self.page.graphicsStream:
				self.put(s)
		self.put('BT')
		for s in self.page.textStream:
			self.put(s)
		self.put('ET')
		self.put('endstream')
		self.put('endobj')

	def endPage(self):
		"""
		required at the end of each page of output. hWrites output to the pdf file,
		and sets the page to None.
		* uses addxRef() to add the page object number to the xref table
		* writes the page object
		* writes the stream as a separate object
		* writes the length of the stream as a separate object. 
		"""
		self.addxRef(self.page.pageObjNo, self.offset, 'Page ' + str(self.page.pageNo))
		self.put(str(self.page.pageObjNo) + ' 0 obj')
		self.put('<< /Type /Page')
		self.put('   /Parent ' + str(self.page.parentObjNo) + ' 0 R')
		self.put('  /MediaBox [0 0 ' + str(self.pageWidth)+  ' ' + str(self.pageHeight)+']' )

		self.put('   /Contents ' +  str(self.page.streamObjNo)+' 0 R')
		self.put('   /Resources << /ProcSet 4 0 R ')
		if len(self.page.xObjectList) > 0:
			self.put('   /XObject << ' +  self.page.xObjectList +' >>')

		self.put('                 /Font << ' +  self.page.fontList + ' >>')
		self.put('              >>')
		self.put('>>')
		self.put('endobj')
		#-- now the stream
		
		self.addxRef(self.page.streamObjNo,self.offset,'Stream ' + str(self.page.pageNo))
		self.put(str(self.page.streamObjNo) + ' 0 obj')
		self.put('<< /Length ' + str(self.page.sizeObjNo) + ' 0 R >>')
		self.put('stream')
		vLen = 0
		if len(self.page.graphicsStream ) > 0:
			for s in self.page.graphicsStream:
				self.put(s)
				vLen = vLen + len(s) + 2
		self.put('BT')
		for s in self.page.textStream:
			self.put( s)
			vLen = vLen + len(s) + 2
		self.put('ET');
		vLen = vLen + 8 # -- For BT and ET
		self.put('endstream')
		self.put('endobj')
		#-- Now write the length object
		self.addxRef(self.page.sizeObjNo,self.offset,'Size ' +  str(self.page.pageNo))
		self.put(str(self.page.sizeObjNo) + ' 0 obj')
		self.put('  ' + str(vLen - 2) )
		self.put('endobj')
		self.page = None


	def setDefaultUnit( self, pUnit):
		""" Set the defaultUnit attribute """
		self.defaultUnit = pUnit
		
	def getDefaultUnit(self):
		"""return the current value of the defaultUnit attribute """
		return self.defaultUnit
		
	def convertUnits(self, pUnits, pFrom, pTo):
		"""
		Convert between any of the different units of measurement.
		Units may be i: inches r: row c: col p: points. Default is p
		r and c use charWidth and lineHeight
		"""
		# 1 millimeter = 0.0393701 inches
		self.checkMeasurementUnit( pFrom )
		self.checkMeasurementUnit( pTo)
		if pFrom == 'i':
			vPoints = pUnits * 72
		elif pFrom == 'r':
			vPoints = pUnits * self.lineHeight
		elif pFrom == 'c':
			vPoints = pUnits * self.charWidth
		elif pFrom == 'p':
			vPoints = pUnits
		elif pFrom == 'm':
			vPoints  = pUnits * 0.0393701 / 72.0
		else:
			vPoints = pUnits
			
		if pTo == 'i':
			vReturn = vPoints / 72.0
		elif pTo == 'r' :
			vReturn	= vPoints / ( 1.0 * self.lineHeight	)
		elif pTo == 'c':
			vReturn = vPoints / (1.0 * self.charWidth)
		elif pTo == 'm':
			# 1 inch = 25.4 millimeters
			vReturn = vPoints / 72.0 * 25.4
		else:
			vReturn = vPoints
		return vReturn
		
	def findFontByKey(self, pFontKey):
		"""
		search the pvFontTable list for the font identified by <pFontKey>, and return its
		offset into that list. Returns -1 if not present. Does not return the actual font
		object.
		"""
		vReturn = -1
		
		for i in range(0, len(self.pvFontTable)):
			if self.pvFontTable[i].key == pFontKey:
				vReturn = i
				break
		return vReturn
		
	def getFontKey(self, pFontName):
		""" 
		looks up the font name in the pvFontTable list, and returns the corresponding font key.
		Returns None if not found.
		"""
		vReturn = None
		for font in self.pvFontTable:
			if font.name == pFontName:
				vReturn = font.key
				break
		return vReturn
		
	def setLineHeightFactor(self,  factor):
		"""
		the lineHeightFactor is multiplied times the font size to set the lineHeight.
		lineHeight is reset at every setFont() call. 
		"""
		self.lineHeightFactor = factor
	
	def charWidthFactor(self,  factor ):
		"""
		mmultiplier used to determine a character width for a font size. 
		charWidth becomes font.avgSize * charWidthFactor * fontSize / 1000
		"""
		self.charWidthFactor = factor
		
	def setFont(self, pFontKey, pFontSize):
		"""
		setFont sets the current font to the values in the parameters.
		Invokes registerFont if necessary.
		Resets the following attributes:
		currentFontSize - pFontSize
		currentFontKey -  pFontKey
		lineHeight - lineHeightFactor * pFontSize
		charWidth  - 1.05 * vFont.avgSize * pFontSize  1000
		charWidth is an approximation, at best.
		Each page tracks the fonts set during it's construction. A
		command is added to the page's textstream to set the font and size.
		
		"""
		
	
		vPtr = self.findFontByKey( pFontKey)
		assert vPtr > -1 , 'unable to locate font key '+pFontKey
		vFont = self.pvFontTable[vPtr]
		vFontObjNo = self.registerFont( pFontKey)
		t = '/' + vFont.key +' '+ str( pFontSize)+' Tf'
		self.page.textStream.append( t )


		vString = '/' + pFontKey+' '+str(vFontObjNo)+' 0 R'
		if self.page.fontList is None or len(self.page.fontList) < 1:
			self.page.fontList = vString
		else:
			if vString not in self.page.fontList:
				self.page.fontList = self.page.fontList + ' '+ vString
		self.currentFontSize = pFontSize
		self.currentFontKey = pFontKey
		
		# typically lineHeight is 1.5 times the point size
		# and character with 1.1 times?  lets try it
		# string with is the sum of each charcater width * point size  / 10000
		self.lineHeight = self.lineHeightFactor * pFontSize
		self.charWidth = vFont.avgSize  * self.charWidthFactor * pFontSize / 1000

	def pushFont( self, pFontKey, pFontSize):
		""" Save the current font on a stackm and invoke setFont( pFontKey, pFontSize)"""
		self.fontStack.append( { "fontKey": self.currentFontKey, "fontSize" : self.currentFontSize} )
		self.setFont( pFontKey, pFontSize)
	def popFont(self ):
		""" restore the font at the top of self.fontStack, passing its contents to setFont()"""
		font = self.fontStack.pop()
		self.setFont( font["fontKey"], font["fontSize"])

	def setCharWidth( self, pPoints ):
		""" Set the charWidth attribute, in points ( i.e at 72/ince) """
		self.charWidth = pPoints

	#--
	#-- Write routines
	#--
	#--@ Write
	#--@ because the positioning begins at the bottom right, the current row
	#--@ is the point value of the row subtracted from the page height( along with
	#--@ the top margin).

	def write( self, pX, pY, pString, pAlign = 'l', pUnit = None):
		"""
		write is the standard way to generate text at a specific position on a page.
		If <pUnit> is not specified then the documents defaultUnit attribute will be used.
		<pX> is the x-axis coordinate: the column
		<pY> is the y-axis coordinate: the row
		In general, when you must be specific its best to use points or inches.
		Note that this method resets the internal positioning (of the pdf engine, not of
		this instance) to the origin of 0,0.
		"""
		vUnit = self.resolveUnit( pUnit, 'r')
		vLength = self.strLength(self.currentFontKey, self.currentFontSize, pString)
		self.currentRow = self.convertUnits(pY,vUnit,'p')
		
		vUnit = self.resolveUnit(pUnit,'c')
		self.currentCol = self.convertUnits(pX,vUnit,'p')
			
		if pAlign == 'c':
			self.currentCol = self.currentCol - ( vLength / 2.0)
		elif pAlign == 'r':
			self.currentCol = self.currentCol - vLength
		nString = ''
		for c in pString:
			if c == '(':
				nString = nString + '\\' + c
			elif c == ')':
				nString = nString + '\\' + c
			else:
				nString = nString + c
		t = str(self.leftMargin + self.currentCol) + ' '+ str((self.pageHeight - self.topMargin) - self.currentRow) + ' Td'
		self.page.textStream.append( t )
		self.page.textStream.append('(' + nString + ') Tj')
		self.page.textStream.append( '1 0 0 1 0 0 Tm' )
		self.currentCol = self.currentCol + vLength

	def writeOut( self, pString):
		""" write text at the current position: currentRow and CurrentCol """
		self.write( self.currentCol, self.currentRow, pString, None, 'p')

	def writeNext(self, pX, pString, pAlign = 'l', pUnit = None):
		""" write text at the specified column position <pX> and the next row """
		vUnit = self.resolveUnit( pUnit, 'c')
		self.write( self.convertUnits(pX,vUnit,'p'), self.currentRow + self.lineHeight, pString, pAlign, 'p')


	def writeCol(self,  pX, pString, pAlign = 'l',pUnit = None):
		""" write in the current row at the specified column position <pX> """
		vUnit = self.resolveUnit( pUnit,'c')		
		self.write( self.convertUnits(pX,vUnit,'p'),self.currentRow,pString, pAlign, 'p')


	def writeCenteredInLine( self, pY, pString, pUnit = None):
		""" write text centered in the row identified by <pY> """
		vUnit = self.resolveUnit(pUnit, 'r')
		# what is the column position of the center of the line
		vCol = self.getLineWidth('p') / 2.0
		self.write(vCol, self.convertUnits(pY, vUnit,'p'), pString, 'c','p')

	def getCurrentRow(self, pUnit = None):
		""" return the current row, in the specified (or default) unit of measurement,
			base upon the current font and size."""
		vUnit = self.resolveUnit(pUnit,'r')
		return self.convertUnits(self.currentRow,'p',vUnit)
		
	def getCurrentCol(self, pUnit = None):
		""" return the current col, in the specified ( or default) unit of measurement
			This is different from the position tracker internal to pdf.
		"""
		vUnit = self.resolveUnit(pUnit,'c')
		return self.convertUnits(self.currentCol,'p',vUnit)

	def setCurrentRow(self, pValue, pUnit = None):
		""" set the attribute that tracks current row position """
		vUnit = self.resolveUnit(pUnit,'r')
		self.currentRow = self.convertUnits(pValue,vUnit, 'p')
		
		
	def setCurrentCol(self, pValue, pUnit = None):
		""" set the attribute that tracks current column position."""
		vUnit = self.resolveUnit(pUnit,'c')
		self.currentCol = self.convertUnits(pValue, vUnit,'p')
				
	def getBottomRow(self, pUnit = None):
		""" return the bottom row, in the specified or default unit of measurement.
			pageHeight - top and bottom margins divided by lineHeight
		
			while self.getCurrentRow('r') < self.getBottomRow('r'):
				self.writeNext(  < a line of output > )
		
		"""
		
		vReturn = (self.pageHeight - ( self.topMargin + self.bottomMargin)) / self.lineHeight
		vUnit = self.resolveUnit(pUnit,'r')
		return self.convertUnits( vReturn, 'r', vUnit)

	def getFreeRows( self ):
		""" rows available after the current row """
		return (self.getBottomRow('p') - self.getCurrentRow('p')) / self.getLineHeight('p')
		
	def getRightColumn( self, pUnit = None) :
		vUnit = self.resolveUnit(pUnit,'c')
		vReturn = (self.pageWidth - self.rightMargin - self.leftMargin ) / self.charWidth
		return self.convertUnits( vReturn, vUnit)
		


	def setTarget(self, pTarget):
		"""  obsolete """
		self.target = pTarget
		
	def getTarget(self):
		return self.target
		

	def setPageNumber(self, pNumber):
		self.currentPageNo = pNumber
		
	def getPageNumber(self):
		return self.currentPageNo
		

	def setPageSize( self, pHeight, pWidth, pUnits = None):
		""" set the shape of the page however you like
		Margins are not modified by this method.
		"""
		vUnits = self.resolveUnit(pUnits,'r')
		self.pageHeight = self.convertUnits(pHeight, vUnits,'p')
		vUnits = self.resolveUnit(pUnits,'c')
		self.pageWidth = self.convertUnits(pWidth, vUnits, 'p')


	def getLeftMargin(self, pUnit = None):
		vUnit = self.resolveUnit(pUnit,'c')
		return self.convertUnits(self.leftMargin,'p',vUnit)


	def setLeftMargin(self, pMargin, pUnit = None):
		vUnit = self.resolveUnit(pUnit,'c')
		self.leftMargin = self.convertUnits(pMargin,vUnit,'p')
		

	def setRightMargin(self, pMargin, pUnit = None):
		vUnit = self.resolveUnit(pUnit,'c')
		self.rightMargin = self.convertUnits( pMargin, vUnit, 'p')


	def getRightMargin(self, pUnit = None):
		vUnit = self.resolveUnit(pUnit,'c')
		return self.convertUnits( self.rightMargin,'p',vUnit)


	def getRightColumn( self, pUnit = None):
		vUnit = self.resolveUnit(pUnit,'c')
		vPoints = self.pageWidth - (self.leftMargin )
		return self.convertUnits(vPoints,'p',vUnit)


	def setTopMargin(self, pMargin, pUnit):
		vUnit = self.resolveUnit( pUnit,'r')
		self.topMargin = self.convertUnits(pMargin,vUnit,'p')
		
				
	def getTopMargin(self, pUnit = None):
		vUnit = self.resolveUnit( pUnit,'r')
		return self.convertUnits(self.topMargin,'p',vUnit)
		
	def setLineHeight( self, pHeight, pUnit = None):
		""" Set the lineHeight attribute. Use to override the value set by the last setFont call. 
		
		"""
		vUnit = self.resolveUnit(pUnit,'r')
		self.lineHeight = self.convertUnits(pHeight,vUnit,'p')
		

	def getLineHeight(self, pUnit = None):
		""" returns the current line height, in the specified or default unit of measurement.
			It would be expected that the lineHeight, for the Unit r or c, would be 1.
		"""
		vUnit = self.resolveUnit(pUnit,'r')
		return self.convertUnits(self.lineHeight, 'p',vUnit)
		

	def setBottomMargin(self, pMargin, pUnit = None):
		""" Set the bottomMargin attribute """
		vUnit = self.resolveUnit(pUnit,'r')
		self.bottomMargin = self.convertUnits(pMargin, vUnit,'p')
		

	def getBottomMargin(self, pUnit ):
		""" return the size of the bottom margin """ 
		#! makes no sense not to specify the unit
		vUnit = self.resolveUnit(pUnit,'r')
		return self.convertUnits(self.bottomMargin,'p',vUnit)

	def setTextState(self, pCharSpace = 0, pWordSpace = 0, pScale = 100, pLeading = 0, pRender = 0, pRise = 0):
		""" Initializes the textStream environment. Should be reset for each page. """
		t = str(pCharSpace) + ' Tc ' + str(pWordSpace) + ' Tw '
		t = t + str(pScale) + ' Tz ' + str(pLeading) + ' TL '
		t = t + str(pRender) + ' Tr ' + str(pRise) + ' Ts '
		self.page.textStream.append( t )
		

		

	def strLength(self, pFontKey, pFontSize, pString):
		"""
		This strLength method returns a rough approximation of the length of a string.
		Each font has an average character size. If it is a fixed font then that average
		size will also be the size (width) of every character in its character set, and the
		length of the string calculated by this method should be accurate. However, for
		proportional fonts - such as F2 and F3 - this will be a crude approximation. See
		the PdfFontMetrics class for more precise string lengths.
		Returns a width, in points.
		Returns points.
		
		"""
		vPtr = self.findFontByKey(pFontKey)
		avgSize = self.pvFontTable[vPtr].avgSize
		return (pFontSize * len( pString) *  avgSize ) / 1000.0
		#! there is data available on the width of each character in the variable fonts.
		#! is it worth the time?
	
	def setGrayScale( self, pScale = 0):
		"""
		Sets the density of printed output. 0 is black, 0.9 is a light transparent gray.
		"""
		s = "%6.2f" % pScale
		self.page.textStream.append(  s + ' g')
		
		
	def waterMark(self, pText):
		"""
		This method generates a watermark, with <pText> in a large F3I font, in the center
		of row 10. It would be better, for large documents, to create a reusable XObject.
		This writes to the current page. Current font is saved at the start and restored
		at the end.
		"""
		self.setGrayScale( 0.80)
		vSaveFontSize = self.currentFontSize
		vSaveFontKey = self.currentFontKey
		self.setFont('F3I',40)
		self.writeCenteredInLine(10,pText,'r')
		self.setFont(vSaveFontKey, vSaveFontSize)
		self.setGrayScale( 0 )

	def defineImageXObject( self, hexStrings, pName, pWidth, pHeight, pBitsPerComponent, pColorSpace = None, pImageMask = None, pImageLib = None, pFilter = None):
		"""
		define an image XObject, that can later be invoked by <pName>.
		hexStrings - See readImage() for info on the :hexStrings: parameter - which is a list of ascii characters
		pWidth and pHeight is the size to display the image
		pBitsPerComponent depends on the graphics format. 8 for jpg
		pColorSpace  DeviceRGB for jpeg
		pImageMask
		pImageLib ImageB for jpg
		pFilter - DCTDecode for jpg
		self.defineImageXObject( hexStrings,'Sh1', 274,283,8,'DeviceRGB',None,'ImageB','DCTDecode')
		No matrix or bounding box is defined, but width and height are specified.

		"""
		vObject = self.getNextObjNo()
		vObjLen = self.getNextObjNo()
		self.addxRef(vObject,self.offset, 'Image ' +  pName)
		self.put( str(vObject) + ' 0 obj')
		self.put('<< /Type /XObject /Subtype /Image')
		self.put('   /Width ' + str(pWidth) + ' /Height ' + str(pHeight))
		if pColorSpace is not None:
			self.put('   /ColorSpace /' + pColorSpace)
		if pImageMask is not None:
			self.put('   /ImageMask ' +  pImageMask)

		self.put('   /Name /' +  pName)
		self.put('   /BitsPerComponent ' +  str(pBitsPerComponent))
		self.put('   /Length ' +  str(vObjLen) +  ' 0 R ')
		if pFilter is not None:
			self.put('   /Filter [/ASCIIHexDecode /' + pFilter + '] >>')
		else:
			self.put('  /Filter /ASCIIHexDecode >>')
   
		self.put('stream')
		vLength = 0
		hexStrings[-1] = hexStrings[-1] + '>'
		for s in hexStrings:
			self.put(s)
			vLength = vLength + len(s) + 2
		self.put('endstream')
		self.put('endobj')
		#  Now write the length object

		self.addxRef(vObjLen, self.offset,'image size')
		self.put( str(vObjLen) + ' 0 obj')
		self.put('  '  + str(vLength) )
		self.put('endobj')

		# now add this to the xobject tabl
		
		newXObject = XObject()
		newXObject.name = pName
		newXObject.objectNo = vObject
		newXObject.width = pWidth
		newXObject.height = pHeight
		newXObject.device = pColorSpace
		newXObject.imageLib = pImageLib
		newXObject.imageMask = pImageMask
		
		self.pvXObjectTable.append( newXObject)		

	def findXObject(self, pName):
		"""
		Search for an entry in the pvXObjectTable list, return its offset in the list.
		Return -1 if <pName> is not located
		"""
		vReturn = None
		for i in range( 0, len(self.pvXObjectTable)):
			if self.pvXObjectTable[i].name == pName:
				vReturn = i
				break
		assert vReturn > -1,'Unable to find XObject '+ pName
		return vReturn
		




	def showImage(self, pName, pX, pY, pUnit = None, pScaleX = None, pScaleY = None, pSkewX = 0, pSkewY = 0, pGrayScale = 0):
		"""
		for an image already recorded in the pvXObjectTable list (see defineImageXObject)
		this method places it in the current page, and the position specified by <pX> and <py>
		Optionally, dimensionally scaled as specified by <pScaleX> and <pScaleY>
		Optionally skewed as defined by <pSkewX> and pSkewY>
		and with optional grayscaling, <pGrayScale>.
		The image to output is identified by <pName>
		"""
		vImage = self.findXObject( pName)
		vUnit = self.resolveUnit( pUnit, 'r')
		vX = self.convertUnits(pX, vUnit,'p') + self.leftMargin
		vUnit = self.resolveUnit(pUnit,'c')
		vY = self.convertUnits( pY,  vUnit, 'p')
		vY = self.pageHeight - (self.topMargin + vY)
		if pScaleX is None:
			vScaleX = self.pvXObjectTable[vImage].width
		else:
			vScaleX = pScaleX
		if pScaleY is None:
			vScaleY = self.pvXObjectTable[vImage].height
		else:
			vScaleY = pScaleY
		
			
		# "%4.2f" % 0
		# vLine = 'q ' +  str(pGrayScale,'990.99')+ ' g ' + str (vScaleX)
		vGrayScale = "%6.2f" % pGrayScale
		vLine = 'q ' +  vGrayScale + ' g ' + str (vScaleX)
		vLine = vLine + '   ' + str( pSkewX) + '   ' + str(pSkewY) + '   '
		vLine = vLine + str(vScaleY) + '   ' + str(vX) + '   ' + str(vY) + ' cm /'+pName+' Do Q'
		
		self.page.graphicsStream.append( vLine )

		if not '/'+ pName in self.page.xObjectList:
			self.page.xObjectList = self.page.xObjectList + '/' + pName+' '+ str(self.pvXObjectTable[vImage].objectNo)+ ' 0 R'			

	def showForm(self,  pName ):
		"""
		A simple method to display a form XObject, such as a template that is reused on 
		multiple pages. This is a page overlay, it is not moved around on the page
		
		"""
		#if pUnit is None:
		#	vUnit = self.defaultUnit
		#else:
		#	vUnit = pUnit
		#vUnit = self.resolveUnit(vUnit,'c')
		#vX = self.convertUnits( pX, vUnit,'p')
		#vUnt = self.resolveUnit(vUnit,'r')
		#vY = self.convertUnits( pY, vUnit,'p')
		vPtr = self.findXObject(pName)
		self.page.graphicsStream.append( '1   0   0   1   0   0  cm /' + pName + ' Do  ' )
		# self.page.graphicsStream.append( '1   0   0   1 100 100 cm  /' + pName + ' Do  ' )		
		if not pName in self.page.xObjectList:
			self.page.xObjectList = self.page.xObjectList + ' /'+pName + ' ' + str( self.pvXObjectTable[vPtr].objectNo) + ' 0 R'


	def readImage(self,  name):
		"""
		read an image into a bytearray
		:name: is the filename, passed to the open function.
		Uses binascii.hexlify() to conver it to a hex string (twice as long)
		The results are split itno a list of strings each with a length of 40 - until end
		The functionm return that list. Used to write binary data to a pdf file. 
		seealso: defineImageXObject()
		"""
		b = open(name,'rb').read()
		c = binascii.hexlify( b )
		clines = []
		vlen = 60
		p = 0
		while p < len(c):
			clines.append( c[p: p + vlen])
			p = p + vlen
		return clines
			
		
	#
	# Graphics routines
	# shade
	# grayBar
	# drawLine
	
	def shade( self, pX1, pY1, pX2, pY2, pScale = 0.9, pUnit = None):
		"""
		GrayScale the rectagular area defined by the two points.
		See grayBar() for an example.
		"""
		#! grayscale the rectanbular area defined by the pX & pY parameters
		vUnit = self.resolveUnit( pUnit, 'r')
		vY1 = self.convertUnits(pY1, vUnit, 'p')
		vY2 = self.convertUnits(pY2, vUnit, 'p')
		vUnit = self.resolveUnit(pUnit, 'c')
		vX1 = self.convertUnits(pX1, vUnit, 'p')
		vX2 = self.convertUnits(pX2, vUnit, 'p')
		vScale = "%6.2f" % pScale
		self.page.graphicsStream.append( vScale + ' g')
		vLine = str(self.leftMargin + vX1) + ' '+str(self.pageHeight - self.topMargin - vY1)+' '
		vLine = vLine + str(vX2 - vX1) + ' ' +str( vY2 - vY1) + ' re'
		self.page.graphicsStream.append( vLine )
		self.page.graphicsStream.append( 'f 0 g' )
	
	def grayBar( self, pY, pUnit = None):
		"""
		set the background for one row across the page to a light gray.
		pUnit is resolved to row, identified by pY, which is then shaded
		to a height of lineHeight. Uses shade() to draw the bar.
		"""
		vUnit = self.resolveUnit( pUnit,'r')
		vRow = self.convertUnits( pY, vUnit, 'r')
		self.shade(1, vRow + 0.15, self.getLineWidth('c'), vRow + 0.9, 0.9,'r')
		
	def drawLine( self, pX1, pY1, pX2, pY2, pUnit = None, pWidth = None):
		""" Draw a line between two points 
			
		"""
		if pWidth is not None:
			self.page.graphicsStream.append( str(pWidth)+ ' w')			
		if pUnit is None:
			vUnit = self.defaultUnit
		else:
			vUnit = pUnit
		if vUnit in [ 'r','c']:
			vRowUnit = 'r'
			vColUnit = 'c'
		else:
			vRowUnit = vUnit
			vColUnit = vUnit
						
		vX1 = self.leftMargin + self.convertUnits( pX1, vColUnit, 'p')
		vY1 = self.pageHeight - self.topMargin - self.convertUnits(pY1, vRowUnit, 'p')
		vX2 = self.leftMargin + self.convertUnits( pX2, vColUnit,'p')
		vY2 = self.pageHeight - self.topMargin - self.convertUnits(pY2, vRowUnit, 'p')
		self.page.graphicsStream.append( str(vX1) + ' '+str(vY1)+' m '+str(vX2)+' '+str(vY2)+' l s') 

	def rectangle( self, pX, pY, pWidth, pHeight, pUnit = None, pLineWidth = None):
		""" draw 4 lines, forming a rectangle. """
		self.drawLine(pX,pY,pX + pWidth, pY,pUnit,pLineWidth )  # top line
		self.drawLine(pX,pY + pHeight,pX + pWidth, pY + pHeight,pUnit,pLineWidth) # bottom line
		self.drawLine(pX,pY,pX, pY + pHeight,pUnit,pLineWidth) # left side
		self.drawLine(pX + pWidth,pY,pX + pWidth, pY + pHeight,pUnit,pLineWidth) #  right side

	def lineAcrossPage(self, pY, pUnit = None):
		""" draw a line across the page, to intersect a page border, if present
		sets the current row to pY, current col to 0
		 """
		vUnit = self.resolveUnit( pUnit, 'r')
		vRow = self.convertUnits( pY, vUnit, 'p')
		self.currentRow = vRow
		self.drawLine(0, vRow, self.getLineWidth('p') + 5, vRow, 'p')
		
	def verticalPageLine(self, pX, pUnit = None):
		""" vertical line the full height of a page, intersecting a page border if present
		sets the current column to Px
		 """
		vUnit = self.resolveUnit(pUnit, 'c')
		vCol = self.convertUnits( pX, vUnit, 'p')
		self.currentCol = vCol
		self.drawLine( vCol, 0, vCol, self.pageHeight - self.bottomMargin - self.topMargin + 5, 'p')

	def pageBorder(self):
		""" draw lines around the page, offset by margins, and based on page size. """
		vBottom = self.getBottomRow('p') + 5
		vRight = self.getLineWidth('p') + 5
		
		self.drawLine(0,0, vRight , 0, 'p') # top of page
		self.drawLine(0, vBottom, vRight, vBottom, 'p') # bottom of page
		self.drawLine(0,0,0, vBottom,'p') # left side
		self.drawLine(vRight, 0, vRight, vBottom,'p') # right side

	def addGraphic( self, pText ):
		""" primitive to add <pText> to the page graphic stream """
		self.page.graphicsStream.append( pText )



	#an ellipse is drawn with 4 bezier curves.
	#see http://www.codeguru.com/gdi/ellipse.shtml
	#                   //                        /
	#                   //        2___3___4       /
	#                   //     1             5    /
	#                   //     |             |    /
	#                   //     |             |    /
	#                   //     0,12          6    /
	#                   //     |             |    /
	#                   //     |             |    /
	#                   //    11             7    /
	#                   //       10___9___8       /
	#                   //                        /
	#                   //------------------------*

	def ellipse(self, pX, pY, pRadiusX, pRadiusY, pUnit = None, pLineWidth = None):
		"""
		#! draw an ellipse centered at <pX>, <pY>
		#! with a horizontal radius of <pRadiusX> and a vertical radius of <pRadiusY>
		#! best to use inches or points as the unit here
		#! if the X radius and the Y radius are equal then its a circle
		This routine draws 4 arcs.
		"""
		vMagic = 0.2761423749154
		self.addGraphic( 'q')
		if pLineWidth is not None:
			self.addGraphic( str(pLineWidth)+ ' w')
		self.addGraphic('1 i')
		if pUnit is None:
			vUnit = self.defaultUnit
		else:
			vUnit = pUnit
		if vUnit in [ 'r','c']:
			vRowUnit = 'r'
			vColUnit = 'c'
		else:
			vRowUnit = vUnit
			vColUnit = vUnit
		vX = self.convertUnits( pX, vColUnit, 'p')
		vY = self.convertUnits( pY, vRowUnit, 'p')
		
		vCenter = _point( vX + self.leftMargin, self.pageHeight - self.topMargin - vY )
		
		# self.write(vCenter.x, vCenter.y,'X','l','p')
		vRadius = _point( self.convertUnits(pRadiusX, vColUnit,'p'), self.convertUnits(pRadiusY,vRowUnit,'p'))	
		
		vOffset = _point( 2 * vRadius.x * vMagic, 2 * vRadius.y * vMagic)
		# now we need a list with elements 0:12
		vXy = []
		for i in range(0,13):
			vXy.append( _point(0,0))
	
		# we now have the center point, vCenter
		# the horizontal radius vX, and the vertical radius vY = vRadius

		vXy[0].x = vCenter.x - vRadius.x
		vXy[1].x = vXy[0].x
		vXy[11].x = vXy[0].x
		vXy[12].x = vXy[0].x
		
		vXy[5].x = vCenter.x + vRadius.x
		vXy[6].x = vXy[5].x
		vXy[7].x = vXy[5].x
		
		vXy[2].x = vCenter.x - vOffset.x
		vXy[10].x = vXy[2].x
		
		vXy[3].x = vCenter.x
		vXy[9].x = vCenter.x
		
		vXy[4].x = vCenter.x + vOffset.x
		vXy[8].x = vXy[4].x
	
		vXy[2].y = vCenter.y + vRadius.y
		vXy[3].y = vXy[2].y
		vXy[4].y = vXy[2].y
		
		vXy[8].y = vCenter.y - vRadius.y
		vXy[9].y = vXy[8].y
		vXy[10].y = vXy[8].y
		
		vXy[0].y = vCenter.y
		vXy[1].y = vCenter.y + vOffset.y
		vXy[11].y = vCenter.y - vOffset.y
		vXy[12].y = vCenter.y
		
		vXy[5].y = vCenter.y + vOffset.y
		vXy[6].y = vCenter.y
		vXy[7].y = vCenter.y - vOffset.y
		#for i in range(0,13):
		#	self.write(5,20 + i, str(i)+': '+str(vXy[i]),'l','r')

		#  move to the left point.
		self.addGraphic( str( vXy[0].x)  + ' ' + str(vXy[0].y) + ' m')
		# draw the four arcs, each arc with 3 points
		for p in [1,4,7, 10]:
			t = str(vXy[p].x)+' '+ str(vXy[ p].y) +' ' 
			t = t + str(vXy[p + 1].x) +' '+ str(vXy[p + 1].y) + ' ' 
			t = t + str(vXy[p + 2].x) + ' '+ str(vXy[p + 2].y) + ' c'
			self.addGraphic(t)
		self.addGraphic('S Q')
		            
	def helloWorld(self):
	
		self.beginDoc('hello_world.pdf')
		self.newPage()
		self.setTextState()
		self.writeCol(20,'this is writeCol at 20')
		self.writeNext(20,'this is writeNext at 20')
		self.writeCenteredInLine(15,'writeCenteredInLine at row 15')
		self.write( 10,10,'write','l','r')
		self.setFont('F3',8)
		self.write(20,30,'This is a different font')
		for row in range(30,50):
			self.write(20,row,'This is row '+str(row),'l','r' )
		self.waterMark('WaterMark!')
		
		self.endPage()
		
		for i in range(0, 50):
			self.newPage()
			self.setTextState()
			self.setFont('F3',16)
			self.write( 20, 40,'This is page number '+ str(self.currentPageNo) )
			self.write( 30, 50,'This is page number '+ str(self.page.pageNo) )
			self.waterMark(str(i))
			self.endPage()
		self.endDoc()
	
	def pageLayout(self):
		self.beginDoc('pagelayout.pdf')
		self.setDefaultUnit('r')
		
		for font in [ 'F1','F2','F3']:
			for size in [ 8, 10, 12, 14, 16, 18 ]:
				self.newPage()
				self.setTextState()
				self.setFont( font, size)
				self.writeCenteredInLine( 1, 'Font '+ font + ' Size ' + str(size))
				self.write(10,2,'0123456789012345678901234567890')
				self.write(50,2,'abcdefghijklmnopqrstuvwxyz')
				for i in range(10,40):
					self.write(i,3,str(i%10),'l')
				alpha = 'abcdefghijklmnopqrstuvwxyz'
				for i in range(0,26):
					self.write(50 + i, 3, alpha[i],'l')
				
				for row in [10,20,30,40,50,60,70,80]:
					for col in [ 10, 20, 30, 40, 50, 60, 70, 80]:
						self.write(col, row, 'x@r'+str(row)+':c'+str(col))
				self.write( 10, self.getBottomRow(),'This is the bottome row: '+str(self.getBottomRow()),'l')
				self.endPage()
		self.endDoc()		

	def testJpeg( self ):
		hexStrings = self.readImage('image.jpg')

		self.beginDoc('image_test.pdf')
		self.setDefaultUnit( 'r' )
		# 	def defineImageObject( self, hexStrings, pName, pWidth, pHeight, pBitsPerComponent, pColorSpace = None, pImageMask = None, pImageLib = None, pFilter = None):
		self.defineImageXObject( hexStrings,'Sh1', 274,283,8,'DeviceRGB',None,'ImageB','DCTDecode')
		# pdfDoc.defineimagexobject(vDoc,vJpg,'Sh1',74,83,8,'DeviceGray',null,'ImageB','DCTDecode');

		self.newFormXObject('W1') 
		self.waterMark('WATERMARK')
		for i in range(0, 10):
			self.write(10,i,'This is xObject Row ' + str(i))
		self.endFormXObject() 

		self.newPage()
		self.write(10,5,'column 10 row 5','l','r')
		self.showImage('Sh1',10,10,'r',80,80)
		self.showImage('Sh1',10,20,'r',90,90)
		self.showImage('Sh1',10,40,'r',100,100)
		self.showImage('Sh1',10,80,'r',120,120)
		self.write(10,25,'column 10 row25','l','r')
		self.showForm('W1')
		self.endPage()
		self.endDoc()



'''
from PdfDoc import PdfDocument
p = PdfDocument()
p.helloWorld()


from PdfDoc import PdfDocument
p = PdfDocument()
p.testJpeg()

from PdfDoc import PdfDocument
p = PdfDocument()
p.pageLayout()


'''
