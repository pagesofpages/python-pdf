# test.py

from PdfText import PdfString


p1 = PdfString('F3',10,'this is a long long long string of no partiular interest, other than bad spelling')
print( 'p1 length is ' + str(p1.length))
print('p1 initial string is: ' + p1.string)
p2 = p1.split2( 600  )

print( 'p1 is: >'+p1.string+'<')
print( 'p2 is: >'+p2.string+'<')
print('p2 length is ' + str(p2.length))

