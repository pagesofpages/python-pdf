#! /usr/bin/python
# load_fonts.py

import io
import os
import json

'''
[
	{ "key": "F2", "chars" : []
]
	

'''


class PdfFontMetrics( object):
	def __init__(self):
		self.defaultCharWidth = 600
		self.fileName = 'pdfFontMetrics.json'
		self.fonts = []
	def findFont(self, pFontKey):
		vReturn = None
		for font in self.fonts:
			if font['key'] == pFontKey:
				vReturn = font
				break
		return vReturn

	def addChar( self, pFontKey, pAscii, pChar, pWidth):
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
		with open( self.fileName ) as json_file:
			entries = json.load( json_file )
			self.fonts = entries
	def writeFontMetrics(self):
		entries = self.fonts
		with open( self.fileName, 'w') as outfile:
			json.dump( entries, outfile, indent=2)
			

	def strLength(self, pFontKey, pString):
		vReturn = None
		font = self.findFont( pFontKey )
		if font is None:
			vReturn = len( pString) ( self.defaultCharWidth )		
		else:
			vReturn = 0
			for s in pString:
				if ord(s) <= len(font['chars']):
					vReturn = vReturn +font['chars'][ord(s)].width
				else:
					vReturn = vReturn + self.defaultCharWidth
		return vReturn



f = PdfFontMetrics()			
f.addChar('F2',32,' ',278)
f.addChar('F2',33,'!',278)
f.addChar('F2',34,'"',355)
f.addChar('F2',35,'#',556)
f.addChar('F2',36,'$',556)
f.addChar('F2',37,'%',889)

f.addChar('F2',39,'\'',222)

f.addChar('F2',40,'(',333)

f.addChar('F2',41,')',333)

f.addChar('F2',42,'*',389)

f.addChar('F2',43,'+',584)

f.addChar('F2',45,'-',333)

f.addChar('F2',46,'.',278)

f.addChar('F2',50,'2',556)

f.addChar('F2',51,'3',556)

f.addChar('F2',52,'4',556)

f.addChar('F2',54,'6',556)

f.addChar('F2',56,'8',556)

f.addChar('F2',57,'9',556)

f.addChar('F2',58,':',278)

f.addChar('F2',59,';',278)

f.addChar('F2',61,'=',584)

f.addChar('F2',62,'>',584)

f.addChar('F2',63,'?',556)

f.addChar('F2',64,'@',1015)

f.addChar('F2',65,'A',667)

f.addChar('F2',69,'E',667)

f.addChar('F2',70,'F',611)

f.addChar('F2',72,'H',722)

f.addChar('F2',74,'J',500)

f.addChar('F2',75,'K',667)

f.addChar('F2',77,'M',833)

f.addChar('F2',78,'N',722)

f.addChar('F2',79,'O',778)

f.addChar('F2',80,'P',667)

f.addChar('F2',82,'R',722)

f.addChar('F2',83,'S',667)

f.addChar('F2',84,'T',611)

f.addChar('F2',85,'U',722)

f.addChar('F2',88,'X',667)

f.addChar('F2',89,'Y',667)

f.addChar('F2',90,'Z',611)

f.addChar('F2',91,'[',278)

f.addChar('F2',93,']',278)

f.addChar('F2',95,'_',556)

f.addChar('F2',96,'`',222)

f.addChar('F2',97,'a',556)

f.addChar('F2',98,'b',556)

f.addChar('F2',99,'c',500)

f.addChar('F2',101,'e',556)

f.addChar('F2',102,'f',278)

f.addChar('F2',103,'g',556)

f.addChar('F2',104,'h',556)

f.addChar('F2',105,'i',222)

f.addChar('F2',106,'j',222)

f.addChar('F2',107,'k',500)

f.addChar('F2',108,'l',222)

f.addChar('F2',109,'m',833)

f.addChar('F2',111,'o',556)

f.addChar('F2',112,'p',556)

f.addChar('F2',113,'q',556)

f.addChar('F2',114,'r',333)

f.addChar('F2',115,'s',500)

f.addChar('F2',116,'t',278)

f.addChar('F2',117,'u',556)

f.addChar('F2',118,'v',500)

f.addChar('F2',120,'x',500)

f.addChar('F2',121,'y',500)

f.addChar('F2',123,'{',334)

f.addChar('F2',124,'|',260)

f.addChar('F2',125,'}',334)

f.addChar('F2',126,'~',584)


f.addChar('F2B',32,' ',278)

f.addChar('F2B',34,'"',474)

f.addChar('F2B',36,'$',556)

f.addChar('F2B',38,'&',722)

f.addChar('F2B',39,'\'',278)

f.addChar('F2B',40,'(',333)

f.addChar('F2B',41,')',333)

f.addChar('F2B',43,'+',584)

f.addChar('F2B',44,',',278)

f.addChar('F2B',45,'-',333)

f.addChar('F2B',46,'.',278)

f.addChar('F2B',48,'0',556)

f.addChar('F2B',49,'1',556)

f.addChar('F2B',50,'2',556)

f.addChar('F2B',53,'5',556)

f.addChar('F2B',55,'7',556)

f.addChar('F2B',56,'8',556)

f.addChar('F2B',57,'9',556)

f.addChar('F2B',58,':',333)

f.addChar('F2B',61,'=',584)

f.addChar('F2B',62,'>',584)

f.addChar('F2B',63,'?',611)

f.addChar('F2B',64,'@',975)

f.addChar('F2B',65,'A',722)

f.addChar('F2B',66,'B',722)

f.addChar('F2B',67,'C',722)

f.addChar('F2B',68,'D',722)

f.addChar('F2B',69,'E',667)

f.addChar('F2B',70,'F',611)

f.addChar('F2B',71,'G',778)

f.addChar('F2B',72,'H',722)

f.addChar('F2B',73,'I',278)

f.addChar('F2B',74,'J',556)

f.addChar('F2B',75,'K',722)

f.addChar('F2B',76,'L',611)

f.addChar('F2B',77,'M',833)

f.addChar('F2B',78,'N',722)

f.addChar('F2B',81,'Q',778)

f.addChar('F2B',82,'R',722)

f.addChar('F2B',83,'S',667)

f.addChar('F2B',85,'U',722)

f.addChar('F2B',86,'V',667)

f.addChar('F2B',87,'W',944)

f.addChar('F2B',88,'X',667)

f.addChar('F2B',89,'Y',667)

f.addChar('F2B',90,'Z',611)

f.addChar('F2B',91,'[',333)

f.addChar('F2B',92,'\\',278)

f.addChar('F2B',93,']',333)

f.addChar('F2B',94,'^',584)

f.addChar('F2B',95,'_',556)

f.addChar('F2B',96,'`',278)

f.addChar('F2B',98,'b',611)

f.addChar('F2B',99,'c',556)

f.addChar('F2B',100,'d',611)

f.addChar('F2B',101,'e',556)

f.addChar('F2B',102,'f',333)

f.addChar('F2B',103,'g',611)

f.addChar('F2B',105,'i',278)

f.addChar('F2B',106,'j',278)

f.addChar('F2B',107,'k',556)

f.addChar('F2B',108,'l',278)

f.addChar('F2B',109,'m',889)

f.addChar('F2B',111,'o',611)

f.addChar('F2B',112,'p',611)

f.addChar('F2B',115,'s',556)

f.addChar('F2B',116,'t',333)

f.addChar('F2B',117,'u',611)

f.addChar('F2B',119,'w',778)

f.addChar('F2B',123,'{',389)

f.addChar('F2B',124,'|',280)

f.addChar('F2B',125,'}',389)

f.addChar('F2B',126,'~',584)


f.addChar('F2IB',32,' ',278)

f.addChar('F2IB',33,'!',333)

f.addChar('F2IB',34,'"',474)

f.addChar('F2IB',35,'#',556)

f.addChar('F2IB',36,'$',556)

f.addChar('F2IB',37,'%',889)

f.addChar('F2IB',38,'&',722)

f.addChar('F2IB',39,'\'',278)

f.addChar('F2IB',40,'(',333)

f.addChar('F2IB',42,'*',389)

f.addChar('F2IB',43,'+',584)

f.addChar('F2IB',44,',',278)

f.addChar('F2IB',45,'-',333)

f.addChar('F2IB',46,'.',278)

f.addChar('F2IB',48,'0',556)

f.addChar('F2IB',49,'1',556)

f.addChar('F2IB',50,'2',556)

f.addChar('F2IB',51,'3',556)

f.addChar('F2IB',52,'4',556)

f.addChar('F2IB',53,'5',556)

f.addChar('F2IB',54,'6',556)

f.addChar('F2IB',55,'7',556)

f.addChar('F2IB',56,'8',556)

f.addChar('F2IB',58,':',333)

f.addChar('F2IB',59,';',333)

f.addChar('F2IB',60,'<',584)

f.addChar('F2IB',62,'>',584)

f.addChar('F2IB',63,'?',611)

f.addChar('F2IB',64,'@',975)

f.addChar('F2IB',67,'C',722)

f.addChar('F2IB',70,'F',611)

f.addChar('F2IB',73,'I',278)

f.addChar('F2IB',74,'J',556)

f.addChar('F2IB',76,'L',611)

f.addChar('F2IB',77,'M',833)

f.addChar('F2IB',78,'N',722)

f.addChar('F2IB',81,'Q',778)

f.addChar('F2IB',83,'S',667)

f.addChar('F2IB',84,'T',611)

f.addChar('F2IB',85,'U',722)

f.addChar('F2IB',87,'W',944)

f.addChar('F2IB',88,'X',667)

f.addChar('F2IB',90,'Z',611)

f.addChar('F2IB',91,'[',333)

f.addChar('F2IB',92,'\\',278)

f.addChar('F2IB',94,'^',584)

f.addChar('F2IB',95,'_',556)

f.addChar('F2IB',96,'`',278)

f.addChar('F2IB',99,'c',556)

f.addChar('F2IB',101,'e',556)

f.addChar('F2IB',102,'f',333)

f.addChar('F2IB',103,'g',611)

f.addChar('F2IB',106,'j',278)

f.addChar('F2IB',108,'l',278)

f.addChar('F2IB',109,'m',889)

f.addChar('F2IB',110,'n',611)

f.addChar('F2IB',112,'p',611)

f.addChar('F2IB',114,'r',389)

f.addChar('F2IB',116,'t',333)

f.addChar('F2IB',117,'u',611)

f.addChar('F2IB',118,'v',556)

f.addChar('F2IB',119,'w',778)

f.addChar('F2IB',120,'x',556)

f.addChar('F2IB',121,'y',556)

f.addChar('F2IB',122,'z',500)

f.addChar('F2IB',123,'{',389)

f.addChar('F2IB',124,'|',280)

f.addChar('F2IB',125,'}',389)

f.addChar('F2IB',126,'~',584)


f.addChar('F2I',32,' ',278)

f.addChar('F2I',33,'!',278)

f.addChar('F2I',35,'#',556)

f.addChar('F2I',36,'$',556)

f.addChar('F2I',37,'%',889)

f.addChar('F2I',39,'\'',222)

f.addChar('F2I',40,'(',333)

f.addChar('F2I',41,')',333)

f.addChar('F2I',43,'+',584)

f.addChar('F2I',44,',',278)

f.addChar('F2I',45,'-',333)

f.addChar('F2I',46,'.',278)

f.addChar('F2I',48,'0',556)

f.addChar('F2I',49,'1',556)

f.addChar('F2I',50,'2',556)

f.addChar('F2I',53,'5',556)

f.addChar('F2I',54,'6',556)

f.addChar('F2I',57,'9',556)

f.addChar('F2I',58,':',278)

f.addChar('F2I',60,'<',584)

f.addChar('F2I',62,'>',584)

f.addChar('F2I',64,'@',1015)

f.addChar('F2I',65,'A',667)

f.addChar('F2I',66,'B',667)

f.addChar('F2I',69,'E',667)

f.addChar('F2I',70,'F',611)

f.addChar('F2I',71,'G',778)

f.addChar('F2I',72,'H',722)

f.addChar('F2I',73,'I',278)

f.addChar('F2I',74,'J',500)

f.addChar('F2I',76,'L',556)

f.addChar('F2I',77,'M',833)

f.addChar('F2I',78,'N',722)

f.addChar('F2I',79,'O',778)

f.addChar('F2I',80,'P',667)

f.addChar('F2I',81,'Q',778)

f.addChar('F2I',82,'R',722)

f.addChar('F2I',83,'S',667)

f.addChar('F2I',84,'T',611)

f.addChar('F2I',85,'U',722)

f.addChar('F2I',86,'V',667)

f.addChar('F2I',88,'X',667)

f.addChar('F2I',89,'Y',667)

f.addChar('F2I',90,'Z',611)

f.addChar('F2I',91,'[',278)

f.addChar('F2I',93,']',278)

f.addChar('F2I',94,'^',469)

f.addChar('F2I',95,'_',556)

f.addChar('F2I',96,'`',222)

f.addChar('F2I',97,'a',556)

f.addChar('F2I',98,'b',556)

f.addChar('F2I',99,'c',500)

f.addChar('F2I',100,'d',556)

f.addChar('F2I',101,'e',556)

f.addChar('F2I',102,'f',278)

f.addChar('F2I',103,'g',556)

f.addChar('F2I',104,'h',556)

f.addChar('F2I',106,'j',222)

f.addChar('F2I',107,'k',500)

f.addChar('F2I',108,'l',222)

f.addChar('F2I',110,'n',556)

f.addChar('F2I',111,'o',556)

f.addChar('F2I',112,'p',556)

f.addChar('F2I',114,'r',333)

f.addChar('F2I',115,'s',500)

f.addChar('F2I',118,'v',500)

f.addChar('F2I',120,'x',500)

f.addChar('F2I',123,'{',334)

f.addChar('F2I',124,'|',260)
f.addChar('F3',32,' ',250)

f.addChar('F3',33,'!',333)

f.addChar('F3',35,'#',500)

f.addChar('F3',36,'$',500)

f.addChar('F3',37,'%',833)

f.addChar('F3',38,'&',778)

f.addChar('F3',39,'\'',333)

f.addChar('F3',40,'(',333)

f.addChar('F3',41,')',333)

f.addChar('F3',42,'*',500)

f.addChar('F3',43,'+',564)

f.addChar('F3',44,',',250)

f.addChar('F3',45,'-',333)

f.addChar('F3',46,'.',250)

f.addChar('F3',47,'/',278)

f.addChar('F3',48,'0',500)

f.addChar('F3',50,'2',500)

f.addChar('F3',51,'3',500)

f.addChar('F3',52,'4',500)

f.addChar('F3',53,'5',500)

f.addChar('F3',54,'6',500)

f.addChar('F3',55,'7',500)

f.addChar('F3',56,'8',500)

f.addChar('F3',57,'9',500)

f.addChar('F3',59,';',278)

f.addChar('F3',60,'<',564)

f.addChar('F3',61,'=',564)

f.addChar('F3',62,'>',564)

f.addChar('F3',63,'?',444)

f.addChar('F3',64,'@',921)

f.addChar('F3',67,'C',667)

f.addChar('F3',68,'D',722)

f.addChar('F3',69,'E',611)

f.addChar('F3',70,'F',556)

f.addChar('F3',71,'G',722)

f.addChar('F3',72,'H',722)

f.addChar('F3',73,'I',333)

f.addChar('F3',75,'K',722)

f.addChar('F3',76,'L',611)

f.addChar('F3',78,'N',722)

f.addChar('F3',79,'O',722)

f.addChar('F3',82,'R',667)

f.addChar('F3',83,'S',556)

f.addChar('F3',85,'U',722)

f.addChar('F3',87,'W',944)

f.addChar('F3',88,'X',722)

f.addChar('F3',89,'Y',722)

f.addChar('F3',90,'Z',611)

f.addChar('F3',92,'\\',278)

f.addChar('F3',93,']',333)

f.addChar('F3',94,'^',469)

f.addChar('F3',95,'_',500)

f.addChar('F3',96,'`',333)

f.addChar('F3',98,'b',500)

f.addChar('F3',99,'c',444)

f.addChar('F3',100,'d',500)

f.addChar('F3',102,'f',333)

f.addChar('F3',104,'h',500)

f.addChar('F3',107,'k',500)

f.addChar('F3',108,'l',278)

f.addChar('F3',109,'m',778)

f.addChar('F3',110,'n',500)

f.addChar('F3',112,'p',500)

f.addChar('F3',113,'q',500)

f.addChar('F3',115,'s',389)

f.addChar('F3',117,'u',500)

f.addChar('F3',118,'v',500)

f.addChar('F3',122,'z',444)

f.addChar('F3',123,'{',480)

f.addChar('F3',124,'|',200)

f.addChar('F3',125,'}',480)
f.addChar('F3B',33,'!',333)

f.addChar('F3B',34,'"',555)

f.addChar('F3B',35,'#',500)

f.addChar('F3B',36,'$',500)

f.addChar('F3B',37,'%',1000)

f.addChar('F3B',40,'(',333)

f.addChar('F3B',41,')',333)

f.addChar('F3B',42,'*',500)

f.addChar('F3B',43,'+',570)

f.addChar('F3B',44,',',250)

f.addChar('F3B',45,'-',333)

f.addChar('F3B',46,'.',250)

f.addChar('F3B',47,'/',278)

f.addChar('F3B',48,'0',500)

f.addChar('F3B',49,'1',500)

f.addChar('F3B',51,'3',500)

f.addChar('F3B',52,'4',500)

f.addChar('F3B',53,'5',500)

f.addChar('F3B',54,'6',500)

f.addChar('F3B',56,'8',500)

f.addChar('F3B',57,'9',500)

f.addChar('F3B',59,';',333)

f.addChar('F3B',62,'>',570)

f.addChar('F3B',63,'?',500)

f.addChar('F3B',64,'@',930)

f.addChar('F3B',67,'C',722)

f.addChar('F3B',68,'D',722)

f.addChar('F3B',69,'E',667)

f.addChar('F3B',72,'H',778)

f.addChar('F3B',73,'I',389)

f.addChar('F3B',74,'J',500)

f.addChar('F3B',76,'L',667)

f.addChar('F3B',77,'M',944)

f.addChar('F3B',78,'N',722)

f.addChar('F3B',81,'Q',778)

f.addChar('F3B',82,'R',722)

f.addChar('F3B',83,'S',556)

f.addChar('F3B',85,'U',722)

f.addChar('F3B',86,'V',722)

f.addChar('F3B',87,'W',1000)

f.addChar('F3B',88,'X',722)

f.addChar('F3B',90,'Z',667)

f.addChar('F3B',92,'\\',278)

f.addChar('F3B',93,']',333)

f.addChar('F3B',95,'_',500)

f.addChar('F3B',96,'`',333)

f.addChar('F3B',97,'a',500)

f.addChar('F3B',98,'b',556)

f.addChar('F3B',99,'c',444)

f.addChar('F3B',100,'d',556)

f.addChar('F3B',101,'e',444)

f.addChar('F3B',102,'f',333)

f.addChar('F3B',103,'g',500)

f.addChar('F3B',106,'j',333)

f.addChar('F3B',107,'k',556)

f.addChar('F3B',109,'m',833)

f.addChar('F3B',110,'n',556)

f.addChar('F3B',111,'o',500)

f.addChar('F3B',112,'p',556)

f.addChar('F3B',113,'q',556)

f.addChar('F3B',114,'r',444)

f.addChar('F3B',115,'s',389)

f.addChar('F3B',116,'t',333)

f.addChar('F3B',117,'u',556)

f.addChar('F3B',118,'v',500)

f.addChar('F3B',119,'w',722)

f.addChar('F3B',120,'x',500)

f.addChar('F3B',122,'z',444)

f.addChar('F3B',123,'{',394)

f.addChar('F3B',124,'|',220)

f.addChar('F3B',125,'}',394)

f.addChar('F3IB',32,' ',250)

f.addChar('F3IB',33,'!',389)

f.addChar('F3IB',34,'"',555)

f.addChar('F3IB',37,'%',833)

f.addChar('F3IB',38,'&',778)

f.addChar('F3IB',40,'(',333)

f.addChar('F3IB',41,')',333)

f.addChar('F3IB',42,'*',500)

f.addChar('F3IB',45,'-',333)

f.addChar('F3IB',46,'.',250)

f.addChar('F3IB',47,'/',278)

f.addChar('F3IB',49,'1',500)

f.addChar('F3IB',50,'2',500)

f.addChar('F3IB',51,'3',500)

f.addChar('F3IB',53,'5',500)

f.addChar('F3IB',54,'6',500)

f.addChar('F3IB',55,'7',500)

f.addChar('F3IB',57,'9',500)

f.addChar('F3IB',58,':',333)

f.addChar('F3IB',60,'<',570)

f.addChar('F3IB',61,'=',570)

f.addChar('F3IB',62,'>',570)

f.addChar('F3IB',63,'?',500)

f.addChar('F3IB',64,'@',832)

f.addChar('F3IB',65,'A',667)

f.addChar('F3IB',66,'B',667)

f.addChar('F3IB',67,'C',667)

f.addChar('F3IB',68,'D',722)

f.addChar('F3IB',69,'E',667)

f.addChar('F3IB',70,'F',667)

f.addChar('F3IB',71,'G',722)

f.addChar('F3IB',72,'H',778)

f.addChar('F3IB',73,'I',389)

f.addChar('F3IB',74,'J',500)

f.addChar('F3IB',75,'K',667)

f.addChar('F3IB',76,'L',611)

f.addChar('F3IB',77,'M',889)

f.addChar('F3IB',78,'N',722)

f.addChar('F3IB',80,'P',611)

f.addChar('F3IB',82,'R',667)

f.addChar('F3IB',83,'S',556)

f.addChar('F3IB',84,'T',611)

f.addChar('F3IB',85,'U',722)

f.addChar('F3IB',86,'V',667)

f.addChar('F3IB',87,'W',889)

f.addChar('F3IB',88,'X',667)

f.addChar('F3IB',90,'Z',611)

f.addChar('F3IB',91,'[',333)

f.addChar('F3IB',92,'\\',278)

f.addChar('F3IB',93,']',333)

f.addChar('F3IB',94,'^',570)

f.addChar('F3IB',95,'_',500)

f.addChar('F3IB',96,'`',333)

f.addChar('F3IB',97,'a',500)

f.addChar('F3IB',98,'b',500)

f.addChar('F3IB',99,'c',444)

f.addChar('F3IB',101,'e',444)

f.addChar('F3IB',102,'f',333)

f.addChar('F3IB',106,'j',278)

f.addChar('F3IB',107,'k',500)

f.addChar('F3IB',108,'l',278)

f.addChar('F3IB',110,'n',556)

f.addChar('F3IB',111,'o',500)

f.addChar('F3IB',112,'p',500)

f.addChar('F3IB',114,'r',389)

f.addChar('F3IB',116,'t',278)

f.addChar('F3IB',118,'v',444)

f.addChar('F3IB',119,'w',667)

f.addChar('F3IB',122,'z',389)

f.addChar('F3IB',123,'{',348)

f.addChar('F3IB',124,'|',220)

f.addChar('F3IB',126,'~',570)
f.addChar('F3I',32,' ',250)

f.addChar('F3I',33,'!',333)

f.addChar('F3I',34,'"',420)

f.addChar('F3I',35,'#',500)

f.addChar('F3I',36,'$',500)

f.addChar('F3I',38,'&',778)

f.addChar('F3I',39,'\'',333)

f.addChar('F3I',41,')',333)

f.addChar('F3I',42,'*',500)

f.addChar('F3I',43,'+',675)

f.addChar('F3I',44,',',250)

f.addChar('F3I',45,'-',333)

f.addChar('F3I',46,'.',250)

f.addChar('F3I',47,'/',278)

f.addChar('F3I',48,'0',500)

f.addChar('F3I',49,'1',500)

f.addChar('F3I',50,'2',500)

f.addChar('F3I',51,'3',500)

f.addChar('F3I',52,'4',500)

f.addChar('F3I',53,'5',500)

f.addChar('F3I',54,'6',500)

f.addChar('F3I',55,'7',500)

f.addChar('F3I',57,'9',500)

f.addChar('F3I',58,':',333)

f.addChar('F3I',59,';',333)

f.addChar('F3I',60,'<',675)

f.addChar('F3I',61,'=',675)

f.addChar('F3I',62,'>',675)

f.addChar('F3I',63,'?',500)

f.addChar('F3I',65,'A',611)

f.addChar('F3I',66,'B',611)

f.addChar('F3I',68,'D',722)

f.addChar('F3I',69,'E',611)

f.addChar('F3I',70,'F',611)

f.addChar('F3I',72,'H',722)

f.addChar('F3I',73,'I',333)

f.addChar('F3I',74,'J',444)

f.addChar('F3I',77,'M',833)

f.addChar('F3I',79,'O',722)

f.addChar('F3I',81,'Q',722)

f.addChar('F3I',82,'R',611)

f.addChar('F3I',83,'S',500)

f.addChar('F3I',84,'T',556)

f.addChar('F3I',86,'V',611)

f.addChar('F3I',87,'W',833)

f.addChar('F3I',88,'X',611)

f.addChar('F3I',90,'Z',556)

f.addChar('F3I',92,'\\',278)

f.addChar('F3I',93,']',389)

f.addChar('F3I',95,'_',500)

f.addChar('F3I',96,'`',333)

f.addChar('F3I',98,'b',500)

f.addChar('F3I',100,'d',500)

f.addChar('F3I',101,'e',444)

f.addChar('F3I',104,'h',500)

f.addChar('F3I',105,'i',278)

f.addChar('F3I',106,'j',278)

f.addChar('F3I',107,'k',444)

f.addChar('F3I',109,'m',722)

f.addChar('F3I',110,'n',500)

f.addChar('F3I',111,'o',500)

f.addChar('F3I',112,'p',500)

f.addChar('F3I',114,'r',389)

f.addChar('F3I',116,'t',278)

f.addChar('F3I',118,'v',444)

f.addChar('F3I',119,'w',667)

f.addChar('F3I',120,'x',444)

f.addChar('F3I',121,'y',444)

f.addChar('F3I',123,'{',400)

f.addChar('F3I',126,'~',541)



f.addChar('F2',38,'&',667)

f.addChar('F2',44,',',278)

f.addChar('F2',49,'1',556)

f.addChar('F2',55,'7',556)

f.addChar('F2',60,'<',584)

f.addChar('F2',66,'B',667)

f.addChar('F2',71,'G',778)

f.addChar('F2',76,'L',556)

f.addChar('F2',81,'Q',778)

f.addChar('F2',86,'V',667)

f.addChar('F2',92,'\\',278)


f.addChar('F2B',33,'!',333)

f.addChar('F2B',37,'%',889)

f.addChar('F2B',42,'*',389)

f.addChar('F2B',47,'/',278)

f.addChar('F2B',51,'3',556)

f.addChar('F2B',110,'n',611)

f.addChar('F2B',114,'r',389)

f.addChar('F2B',118,'v',556)

f.addChar('F2B',122,'z',500)

f.addChar('F2IB',57,'9',556)

f.addChar('F2IB',61,'=',584)

f.addChar('F2IB',65,'A',722)

f.addChar('F2IB',68,'D',722)

f.addChar('F2IB',75,'K',722)

f.addChar('F2IB',79,'O',778)

f.addChar('F2IB',82,'R',722)

f.addChar('F2IB',86,'V',667)

f.addChar('F2IB',89,'Y',667)

f.addChar('F2IB',93,']',333)

f.addChar('F2IB',97,'a',556)

f.addChar('F2IB',100,'d',611)

f.addChar('F2IB',104,'h',611)

f.addChar('F2IB',107,'k',556)

f.addChar('F2IB',111,'o',611)

f.addChar('F2IB',115,'s',556)


f.addChar('F2I',34,'"',355)

f.addChar('F2I',38,'&',667)

f.addChar('F2I',42,'*',389)

f.addChar('F2I',47,'/',278)

f.addChar('F2I',51,'3',556)

f.addChar('F2I',55,'7',556)

f.addChar('F2I',59,';',278)

f.addChar('F2I',63,'?',556)

f.addChar('F2I',109,'m',833)

f.addChar('F2I',113,'q',556)

f.addChar('F2I',117,'u',556)

f.addChar('F2I',121,'y',500)

f.addChar('F2I',125,'}',334)

f.addChar('F3',77,'M',889)

f.addChar('F3',81,'Q',722)

f.addChar('F3',86,'V',722)

f.addChar('F3',91,'[',333)

f.addChar('F3',97,'a',444)

f.addChar('F3',101,'e',444)

f.addChar('F3',106,'j',278)

f.addChar('F3',111,'o',500)

f.addChar('F3',116,'t',278)

f.addChar('F3',121,'y',500)

f.addChar('F3',126,'~',541)


f.addChar('F3B',50,'2',500)

f.addChar('F3B',55,'7',500)

f.addChar('F3B',60,'<',570)

f.addChar('F3B',65,'A',722)

f.addChar('F3B',70,'F',611)

f.addChar('F3B',75,'K',778)

f.addChar('F3B',80,'P',611)

f.addChar('F3B',84,'T',667)

f.addChar('F3B',89,'Y',722)

f.addChar('F3B',94,'^',581)

f.addChar('F3IB',35,'#',500)

f.addChar('F3IB',39,'\'',333)

f.addChar('F3IB',44,',',250)

f.addChar('F3IB',48,'0',500)

f.addChar('F3IB',52,'4',500)

f.addChar('F3IB',56,'8',500)

f.addChar('F3IB',105,'i',278)

f.addChar('F3IB',109,'m',778)

f.addChar('F3IB',113,'q',500)

f.addChar('F3IB',117,'u',556)

f.addChar('F3IB',121,'y',444)

f.addChar('F3IB',125,'}',348)

f.addChar('F3I',67,'C',667)

f.addChar('F3I',71,'G',722)

f.addChar('F3I',76,'L',556)

f.addChar('F3I',80,'P',611)

f.addChar('F3I',85,'U',722)

f.addChar('F3I',89,'Y',556)

f.addChar('F3I',94,'^',422)

f.addChar('F3I',99,'c',444)

f.addChar('F3I',103,'g',500)

f.addChar('F3I',108,'l',278)

f.addChar('F3I',113,'q',500)

f.addChar('F3I',117,'u',500)

f.addChar('F3I',122,'z',389)

f.addChar('F2',47,'/',278)

f.addChar('F2',67,'C',722)

f.addChar('F2',87,'W',944)

f.addChar('F2',94,'^',469)

f.addChar('F2',110,'n',556)

f.addChar('F2',122,'z',500)

f.addChar('F2B',54,'6',556)

f.addChar('F2B',60,'<',584)

f.addChar('F2B',79,'O',778)

f.addChar('F2B',97,'a',556)

f.addChar('F2B',113,'q',611)

f.addChar('F2IB',41,')',333)

f.addChar('F2IB',69,'E',667)

f.addChar('F2IB',98,'b',611)

f.addChar('F2I',52,'4',556)

f.addChar('F2I',68,'D',722)

f.addChar('F2I',87,'W',944)

f.addChar('F2I',105,'i',222)

f.addChar('F2I',126,'~',584)


f.addChar('F3',49,'1',500)

f.addChar('F3',66,'B',667)

f.addChar('F3',84,'T',611)

f.addChar('F3',103,'g',500)

f.addChar('F3',120,'x',500)

f.addChar('F3B',38,'&',833)

f.addChar('F3B',58,':',333)

f.addChar('F3B',79,'O',778)

f.addChar('F3B',108,'l',278)

f.addChar('F3B',121,'y',500)


f.addChar('F3IB',36,'$',500)

f.addChar('F3IB',59,';',333)

f.addChar('F3IB',81,'Q',722)

f.addChar('F3IB',100,'d',500)

f.addChar('F3IB',120,'x',500)


f.addChar('F3I',37,'%',833)

f.addChar('F3I',56,'8',500)

f.addChar('F3I',75,'K',667)

f.addChar('F3I',97,'a',500)

f.addChar('F3I',115,'s',389)

f.addChar('F2',53,'5',556)

f.addChar('F2B',80,'P',667)

f.addChar('F2B',121,'y',556)
f.addChar('F2IB',71,'G',778)


f.addChar('F2I',56,'8',556)

f.addChar('F2I',75,'K',667)

f.addChar('F2I',119,'w',722)

f.addChar('F3',74,'J',389)

f.addChar('F3',119,'w',722)

f.addChar('F3B',32,' ',250)

f.addChar('F3B',71,'G',778)

f.addChar('F3B',105,'i',278)
f.addChar('F3IB',103,'g',500)

f.addChar('F3I',78,'N',667)

f.addChar('F2',48,'0',556)

f.addChar('F2',73,'I',278)

f.addChar('F2',100,'d',556)

f.addChar('F2',119,'w',722)
f.addChar('F2B',35,'#',556)

f.addChar('F2B',59,';',333)

f.addChar('F2B',84,'T',611)

f.addChar('F2B',104,'h',611)


f.addChar('F2IB',47,'/',278)

f.addChar('F2IB',80,'P',667)

f.addChar('F2IB',113,'q',611)
f.addChar('F2I',61,'=',584)

f.addChar('F2I',67,'C',722)

f.addChar('F2I',92,'\\',278)

f.addChar('F2I',122,'z',500)

f.addChar('F3',34,'"',408)

f.addChar('F3',58,':',278)

f.addChar('F3',80,'P',556)

f.addChar('F3',105,'i',278)
f.addChar('F3B',39,'\'',333)

f.addChar('F3B',66,'B',667)

f.addChar('F3B',91,'[',333)

f.addChar('F3B',104,'h',556)

f.addChar('F3B',126,'~',520)

f.addChar('F3IB',79,'O',722)

f.addChar('F3IB',104,'h',556)
f.addChar('F3I',40,'(',333)

f.addChar('F3I',64,'@',920)

f.addChar('F3I',91,'[',389)

f.addChar('F3I',124,'|',275)

f.addChar('F3I',125,'}',400)
f.addChar('F2',68,'D',722)

f.addChar('F2B',120,'x',556)

f.addChar('F2B',52,'4',556)

f.addChar('F2I',116,'t',278)
f.addChar('F2IB',66,'B',722)

f.addChar('F2IB',105,'i',278)

f.addChar('F2IB',72,'H',722)
f.addChar('F3',65,'A',722)

f.addChar('F3',114,'r',333)

f.addChar('F3I',102,'f',278)
f.addChar('F3B',61,'=',570)
f.addChar('F3IB',89,'Y',611)

f.addChar('F3IB',115,'s',389)
f.addChar('F3IB',43,'+',570)

f.writeFontMetrics()