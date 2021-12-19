from PdfChapter import TextFont
from PdfString import PdfString
from PdfChapter import TextFont
s = []
s.append("This is a test of the emergency broadcasting system.  ")
s.append("  123 45 67.  89abcer fg.    ")
for s1 in s:
	print( str( s1.split(' ')))
	ps = PdfString( TextFont('F3',9),s1)
	print( '-- Original      --'  )
	print ( str(ps ))
	print( '--               --'  )
	pslist = ps.splitIntoWords()
	psnew = ''
	for s2 in pslist:
		print ( str( s2))
		psnew = psnew +s2.string
	print( '-- reconstructed --' )
	p = PdfString(TextFont('F3',9), psnew)
	print( str( p ))
	print( '--               --'  )

