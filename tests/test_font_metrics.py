#! /usr/bin/python
# test_font_metrics.py


from PdfFontMetrics import PdfFontMetrics

f = PdfFontMetrics()
f.readFontMetrics()

s = 'Now is the time for all good men to come to the aid of their country'

print ('String: ' + s )
print('Character length is ' + str(len(s) ))

print('F1 length: ' + str( f.strLength('F1',s) ))

print('F2 length: ' + str( f.strLength('F2',s) ))

print('F3 length: ' + str( f.strLength('F3',s) ))


for c in s:
		print('Char ' + c + ' Font F2 Length ' + str( f.strLength('F2',c)))
		
		
		
	