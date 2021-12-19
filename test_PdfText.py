# test_PdfText.py

from PdfTextFont import TextFont
from PdfChapter import PdfChapter

from PdfParagraph import PdfParagraph, PdfFootnoteParagraph
from PdfString import PdfString

from PdfDoc import PdfDocument






def introduction( doc ):
	# nested functions
	
	def standardParagraph( chapter ):
		para = PdfParagraph(chapter, 'j')
		para.setIndent(36)
		para.setTail(5)
		para.setAlignment('j')
		return para

	def addpGraph( chapter, txt):
		para = standardParagraph( chapter)
		para.addString( mainFont, txt.replace(chr(10),''))
		chapter.addParagraph( para)
	
	def addpGraphStrs( chapter, strs):
		para = standardParagraph( chapter)
		for s in strs:
			para.addString( s.getFont(), s.string)
			# para.strings.append( s)
		chapter.addParagraph( para )	

	
	def addqGraph( chapter, txt):
		para = standardParagraph(chapter)
		para.setIndent(0)
		para.setMargins(24,24)
		para.addString(mainFont.asItalic(), txt)
		chapter.addParagraph( para )
	
	
	def addFn( chapter, txt):
		para = PdfFootnoteParagraph( chapter)
		para.addString( ftrFont, txt)
		chapter.addFootnote( para )
	
	def addFnStrs( chapter, strs):
		para = PdfFootnoteParagraph( chapter)
		for s in strs:
			para.strings.append(s)
		chapter.addFootnote( para )
	
	def addSubHead( chapter, txt):	
		para = PdfParagraph(chapter, 'l', 0)
		para.addString(subHdrFont,txt)
		para.setLead(9)
		para.setTail(10)
		chapter.addParagraph( para )
	
	def lineParagraph( chapter):
		para = PdfParagraph(chapter, 'l')
		para.setIndent(0)
		para.setTail(0)
		return para

	chapter = PdfChapter( doc )
	hdrFont = TextFont('F3B', 12)
	subHdrFont = TextFont('F3I',10)
	mainFont = TextFont('F3',9)
	ftrFont = TextFont('F3',8)

	chapter.setFooterStyle( 'RomanRight', ftrFont)

	# define header

	para = PdfParagraph(chapter, 'c',0, 3)
	para.addString(hdrFont,'Introduction')
	para.setTail(10)
	chapter.addHeader( para, False )


	# subheading

	addSubHead( chapter, 'Overview')

	p0 = """In 1940 Frank Gruber, a young writer living in New York, was trying to  
break into the book market. He had been writing for """
	p1 = """Black Mask"""
	p2 = """ and many other pulps, and turned to  westerns for his first attempt to sell to book publishers. 
A western, however, was only good for from $250 to $500 a title, so he decided to try his hand at writing mysteries. His 
first was quite successful."""
	strs = []
	strs.append(PdfString(mainFont, p0))
	strs.append(PdfString(mainFont.asItalic(), p1))
	strs.append(PdfString(mainFont, p2))
	addpGraphStrs(chapter, strs)


	p = """[though a friend] I met Walter J. Black, who had a book club for classics. It was called the classics club.  
I talked to him a number of times and he kept sounding me out about mysteries, but never revealed the reason. 
Suddenly he announced The Detective Book Club, a mail order operation. This has become, through the years, 
a very successful thing and a great many of my mysteries have been selections of the club. The first book of mine 
that Black took on was The Mighty Blockhead. At that time Black paid one thousand dollars flat royalties to the author, 
of which the original publisher, however, got half^.""".replace(chr(10),"")
	addqGraph(chapter, p)


	# fp = "Gruber, Frank. The Pulp Jungle.  Los Angeles: Sherbourne Press. [c.1967]. p.170"
	strs = []
	strs.append( PdfString( ftrFont, "Gruber, Frank. "))
	strs.append( PdfString( ftrFont.asItalic(),"The Pulp Jungle.  "))
	strs.append( PdfString( ftrFont,"Los Angeles: Sherbourne Press. [c.1967]. p.170" ))
	addFnStrs(chapter, strs)



	p = "Gruber goes on to write about the economics of writing mystery novels."
	addpGraph( chapter, p)


	p = """Things were adding up, though. Five hundred from the paperback companies, five hundred 
from the book club, seven or eight hundred from the original hardcover editions, a couple of hundred from 
the Grosset & Dunlap seventy-five-cent hardcover editions, one thousand to fifteen hundred dollars 
for first serial rights; a mystery novel was beginning to earn respectable money.""".replace(chr(10),'')
	addqGraph( chapter, p)


	p = """The book club did indeed become \"a very successful thing\". Over the course of almost 60 years 
it went on to reprint more than 2700 titles.  Its volumes provide a comprehensive selection of mainstream 
mystery-thriller-suspense titles published throughout the rest of the 20th century and the 
very beginning of the 21st century. They published Erle Stanley Gardner ( in 81 volumes), Hugh 
Pentecost (50 volumes); George Simenon (40 volumes); Agatha Christie (21 volumes). Frank Gruber (15 volumes); Robert Parker 
(7 volumes). And on and on, including  writers not quite mainstream, such as 
Friedrich Durrenmatt, Russell Greenan and Patricia Highsmith."""
	addpGraph( chapter, p )

	p = """The club began distribution in April of 1942.  Walter J. Black, Inc. had been selling books by 
mail order and department store since the 1920's, and was looking to branch out. Branch out they did: the book 
club survived into the 21st century, initially sending out one  volume a month containing three recent 
mysteries.  In the 1970\'s they added a supplemental distribution scheme, marketed as  The Inner Circle, 
which received initially one, and later two,  additional three-in-one volumes very other month,  
There was also a Reader\'s Service Plan available, where two regular monthly volumes 
were combined for shipment every other month  with a reduction in postage and handling 
charges. The frequency of distribution in the their last decade is uncertain, but there are 25 volumes 
that include books with a copyright date as late as 1999 and another 25 volumes containing at 
least one title with a 1998 copyright date. There are a couple of volumes where the latest copyright date 
is 2000; given those 53 volumes  that could not have been issued prior to 1998, it is very likely the club was active in 
2000, and may have continued beyond the year 2000."""
	addpGraph( chapter, p )


	strs = []
	p1 = """The club also produced numerous promotional volumes containing one or
two  mystery novels.  Single-volume reprints seem particular common in the 1950's. 
Double-volumes, often with reprints of Erle Stanley Gardner (and his most popular pseudonym, A. A. Fair) 
are also common.  This checklist lists only the 3-in-1 omnibus volumes, whether a regular distribution or a promotional volume.  
With at least one exception (Ross MacDonald's """
	p2 = "Lew Archer, Private Investigator"
	p3 = """ ) the promotional volumes 
are made up of novels already issued by the club. There is nothing in appearance to distinguish a promotional 
volume from a regular volume; promotional volume can be identified by containing novels that appear separately 
in multiple other volumes. There are around 25 promotional volumes in this listing, but because of their 
ad hoc nature there were probably many more."""
	strs.append( PdfString( mainFont, p1))
	strs.append( PdfString( mainFont.asItalic(), p2))
	strs.append( PdfString(mainFont,  p3))
	addpGraphStrs( chapter, strs)







	addSubHead( chapter, 'Dating')

	strs = []
	p1 = """The book club volumes contain no dating information other than the copyright dates for each of the novels being reprinted. 
The main source of specific dating information for volumes issued though October 1983 is Michael L. Cook's """.replace(chr(10),'')
	p2 = "Murder By Mail. Inside the Mystery Book Clubs.^"
	p3 = """ This book is now out of print. Cook had access 
to company records, and was able to identify the month of distribution for each regular issue, as well as distinguish between regular 
book club issues and volumes issued for the Inner Circle club.  Physically there is nothing  in the volumes to distinguish 
between the two sources.""".replace(chr(10),'')
	strs.append( PdfString( mainFont, p1))
	strs.append( PdfString( mainFont.asItalic(), p2))
	strs.append( PdfString(mainFont,  p3))

	addpGraphStrs( chapter, strs )
	addFn( chapter, "\"Revised and Updated Edition\"  Bowling Green University Popular Press, c.1983" )



	p = """There are a few gaps during the period covered by Cook's listing. No volumes are identified for April and May, 1946; 
February 1947; and May and June 1948. There are several pairs of months where two volumes were given:  August and 
September 1954; August and September 1955.  From January though April 1983 no volumes were issued at all due to their printer 
suddenly going out of business.""".replace(chr(10),'')
	addpGraph( chapter, p )

	p = """After October 1983 the dating of the volumes becomes an arbitrary assignment based on the copyright dates 
of the novels included in each omnibus.  This is only an approximation.  Volumes are assigned to years based on 
the copyright dates of the novels each volume contains; the most recent copyright date becomes the year assigned to a volume.  
It is very unlikely that this is correct for volumes issued in a January or a February of the years 
from 1984 though the end.  No volume has been found containing a mystery with a copyright date after 2000, so 
2000 is the final year used in this listing.""".replace(chr(10),'')
	addpGraph( chapter, p )

	p = """In 1990 the city of publication listed on the title pages was changed from Roslyn, NY to Port Washington, NY. """.replace(chr(10),'')
	addpGraph( chapter, p )

	p1 = """Beginning with the volumes we have assigned to 1993 the city of publication was moved again, 
to Woodbury, NY, and the imprint changed from \"Walter J. Black, Inc for the Detective Book Club\" to simply 
\"The Detective Book Club\".  It is very likely that the club had ceased operations in 1992 (there are 
just 4 volumes containing titles with copyright dates reaching 1992), and was restarted in 1994 or 1995. 
There is a brief mention in """.replace(chr(10),"")
	p2 = "Publisher's Weekly^"""
	p3 = """ of \"the Detective Book Club, recently resurrected by Platinum Press in Woodbury\" .""".replace(chr(10),'')
	strs = []
	strs.append( PdfString( mainFont, p1))
	strs.append( PdfString( mainFont.asItalic(), p2))
	strs.append( PdfString(mainFont,  p3))
	addpGraphStrs( chapter, strs )
	addFn( chapter,'October 20, 1997, Volume 244, Issue 43 p.49' )

	addSubHead( chapter, 'Book Club First Editions?')

	p = """The club reprinted recent mysteries.  In this volume's listings the publisher of the edition being 
reprinted, and its year of publication,  are listed after each title. Occasionally a book that was published 
two years previously will be included, and sometimes titles will be included when the original publisher 
is reissuing books in hardcover, but in general they did not mine the backlists.  Sometimes, however, they seemed 
to publish concurrently with the trade publisher; and in a few cases they published the first US edition of a title.""".replace(chr(10),'')
	addpGraph( chapter, p )


	p = """The main example of first American editions from the book club are the books by Roy Vickers.  
Someone in the selection committee of the Detective Book Club must have been a Vickers fan; of the 12 Vickers 
titles that appear from the DBC,  5 have their first appearance in the US via the book club.""".replace(chr(10),'')
	addpGraph( chapter, p )


	p1 = """Several titles were published only by the Detective Book Club, including """
	p2 = """The Famous McGarry Stories"""
	p3 = """ by Matt Taylor (1958), and """
	p4 = """Columbo and the Samurai Sword"""
	p5 = """ by Bill Magee and Craig Schenck (1980)."""
	strs = []
	strs.append( PdfString( mainFont, p1))
	strs.append( PdfString( mainFont.asItalic(), p2))
	strs.append( PdfString( mainFont, p3))
	strs.append( PdfString( mainFont.asItalic(), p4))
	strs.append( PdfString( mainFont, p5)) 
	addpGraphStrs( chapter, strs)




	p1 = """The Big Blackout"""
	p2 = """ by Don Tracy (1959) preceded a paperback original from Pocket Books, as did """
	p3 = """The Black Gold Murders """
	p4 = """ by John B. Ethan (1959). """
	p5 = """Murder On Trial"""
	p6 = """ by Michael Underwood was issued by the club in December 1957; its official US publication date was February 1958."""
	strs = []
	strs.append( PdfString( mainFont.asItalic(),p1))
	strs.append( PdfString( mainFont,p2))
	strs.append( PdfString( mainFont.asItalic(),p3))
	strs.append( PdfString( mainFont,p4))
	strs.append( PdfString( mainFont.asItalic(),p5))
	strs.append( PdfString( mainFont,p6))
	addpGraphStrs( chapter, strs)



	p1 = """A possibly more interesting (because more collectible) example is Agatha Christie's """
	p2 = """Blood Will Tell"""
	p3 = """, issued by the club in January 1952. The official Dodd, Mead publication date ( as """
	p4 = """Mrs. McGinty's Dead"""
	p5 = """ ) was February 1952^. The British publication date was March 1952 so a case could be made that 
	the Detective Book Club printing is its true first edition.""".replace(chr(10),'')
	strs = []
	strs.append( PdfString( mainFont, p1))
	strs.append( PdfString( mainFont.asItalic(), p2))
	strs.append( PdfString( mainFont, p3))
	strs.append( PdfString( mainFont.asItalic(), p4))
	strs.append( PdfString( mainFont, p5)) 

	addpGraphStrs( chapter, strs)


	strs = []
	strs.append( PdfString( ftrFont.asItalic(), "Publishers Weekly "))
	strs.append( PdfString( ftrFont," December 28, 1951. P.9.  "))
	addFnStrs(chapter, strs)


	addSubHead(chapter,'Citations')

	para = lineParagraph( chapter )
	para.addString( mainFont.asBold(), "1978.01  ")
	para.addString( mainFont.asBoldItalic(), "January ")
	para.addString( mainFont.asBold(),"                                                                                 4586710")
	chapter.addParagraph( para )

	para = lineParagraph( chapter )

	para.addString(mainFont.asBold(),"MacDonald, John D.  ")
	para.addString(mainFont.asBoldItalic(),"One Fearful Yellow Eye.  ") 
	para.addString(mainFont.asBold(), "1977 Lippincott")
	chapter.addParagraph( para )

	para = lineParagraph( chapter )
	para.addString(mainFont.asBold(),"Ferrars, E.X. ")
	para.addString(mainFont.asBoldItalic(),"The Pretty Pink Shroud.  ")
	para.addString(mainFont.asBold(),"1977 Doubleday.")
	chapter.addParagraph( para )

	para = lineParagraph( chapter )

	para.addString(mainFont.asBold(),"Wetering, Janwillem van de. ")
	para.addString(mainFont.asBoldItalic(),"The Japanese Corpse. ")
	para.addString(mainFont.asBold(),"1977 Houghton Mifflin.")
	para.setTail(36)
	chapter.addParagraph( para ) 


	p = """The citations are ordered by year, and by month when month is known. Promotional volumes appear 
at the end of the year to which they are assigned."""
	addpGraph(chapter, p)


	p = """The number at the beginning - 1978.01 above - is used to reference a specific volume in the indexes.  
These numbers are only useful within the context of this volume.  In the above example, \"1978\" identifies the 
year the volume is assigned to. "01" in this case corresponds to the month, but that will only occasionally be 
true; it breaks down completely when multiple volumes are issued in any month,  When no month is known 
then order within a year becomes arbitrary (other than for promotional volumes which are listed at the end 
of listings for the year they are assigned to). In a few cases a change in publisher or location or cover 
design allows a years volumes to be partially ordered. There are rare cases where a month of issue after 
1983 can be independently determined."""
	addpGraph(chapter,p)

	p = """The number at the right on the top line is the WorldCat id.  WorldCat (www.worldcat.org) is a 
consolidated database of library catalogs from around the world; A world cat id has been identified for 
nearly every citation in this listing, as part of the verification process. It can be used to retrieve a 
catalog entry for each of the volumes; often these have additional details, such as pagination."""
	addpGraph(chapter, p)


	p0 = """The remainder of the listing consists of the three titles included in the volume. Each line contains the author, 
the title, and then the year and publisher of the regular edition being reprinted by the club.  
Occasionally the title used by the club will differ from that of the original publisher.  Note also that date and 
publisher is not necessarily the first American edition of a title; sometimes the club would pick up re-issues. 
John D. MacDonald is a good example of that practice; some of his books were paperback originals."""
	p1 = """A Deadly Shade of Gold """
	p2 = "was published by Fawcett paperbacks in 1965; issued in hardcover by Lippincott in 1974 and by the Club in January of 1975."""
	strs = []
	strs.append( PdfString( mainFont, p0))
	strs.append( PdfString( mainFont.asItalic(), p1))
	strs.append( PdfString( mainFont, p2))
	addpGraphStrs( chapter, strs)




	p = """Publisher names change a good deal over time; occasionally they are given in somewhat 
abbreviated form, but where space allows the full name of the publisher has been preserved.  
Elizabeth Daly, in these listings, was published four times by Farrar & Rinehart. Farrar left 
(to form Farrar & Straus)  and Day's remaining  seven titles appeared from  Rinehart.  Rinehart eventually 
merged into Holt, Rinehart & Winston. All three forms of Rinehart appear many times in these listings.""".replace(chr(10),'')
	addpGraph( chapter, p)


	addSubHead(chapter, 'Book Design')

	p = """Volumes were originally published in a tan binding with dust jacket. The jackets used a three-panel design, 
one for each of the three novels present.  Author and title are listed, and a sketch presumed to represent something from the 
book.  The typography varies from standard to script-type fonts. Colors varied from month to month.""".replace(chr(10),'')
	addpGraph( chapter, p)

	p = """In 1952 the sketch was replaced with a picture of the original hardcover volume (occasionally 
imagined rather than an actual representation), at a bit of an angle so that part of the 
spine is visible and one gets a sense of the size of each book being included.""".replace(chr(10),'')
	addpGraph( chapter, p)

	p = """In 1959 the jacket were dropped, and the design from the jacket was used for pictorial paper-over-board covers."""
	addpGraph( chapter, p)

	strs = []
	p0 = """Around 1993 (see the section """
	p1 = """Dating"""
	p2 = """ above) the imprint was changed from  
\"Water J. Black for the Detective Book Club / Roslyn. NY\" to \"The Detective Book Club / Woodbury NY\".  
This probably corresponds to the club going defunct for some period of time, and then being resurrected by The Platinum Press of Woodbury.""".replace(chr(10),'')
	strs.append( PdfString( mainFont, p0))
	strs.append( PdfString( mainFont.asItalic(), p1))
	strs.append( PdfString( mainFont, p2))
	addpGraphStrs( chapter, strs)


	p = """In 1996 the jacket design was modified, dropping the representation of the original books, leaving just 
the author and title in each of the three panels.""".replace(chr(10),'')
	addpGraph( chapter, p)


	p = """The last few volumes assigned to 1999 or 2000 have a new cover design, no longer using a 
three panel design: there is a solid border around the front, with a top label 
"Detective Book Club Triple Mysteries", and the three reprints identified in a single panel in the middle.""".replace(chr(10),'')
	addpGraph( chapter, p)


	addSubHead( chapter, 'Numbers')

	p = """The original price of the volumes was $1.89 each, and that price was maintained for a surprisingly long time. 
By 1958 the price was only $2.29. By 1963 the price was $2.89. In 1968 the price was $3.39. 
In 1975 the price - after very considerable inflation - was just $3.89; in 1977 it was $4.39.""".replace(chr(10),'')
	addpGraph( chapter, p)


	p = """Some indication of the size of the club's membership can be given by the club's reported newspaper 
advertising budget: $406,579 in 1951, $263,248 in 1952^ (a year when newspaper ad spending was generally down).  
It would take more than 18,000 members buying all 12 volumes for a year to gross an amount of revenue equal to 
the 1951 newspaper ad expenditure; and of course there are production costs, reprint rights, 
other advertising costs, and general overhead to consider.  As a point of comparison, Random House, a large and 
commercially aggressive publisher,  spent $189,145.  Other book clubs did have larger expenditures, the largest 
being the Literary Guild: $767,268 in 1951, $525,614 in 1952: more or less twice that of the Detective Book Club.""".replace(chr(10),'')

	addpGraph( chapter, p)



	# [ref: Publishers Weekly Vol 164. July 18, 1953 p194]. 


	strs = []
	strs.append( PdfString( ftrFont.asItalic(), "Publishers Weekly "))
	strs.append( PdfString( ftrFont," Vol 164, July 18, 1953. p194."))
	addFnStrs(chapter, strs)







	p = """In an interview published in 1988^, total membership was described as a \"company secret\", but was more than 
50,000.  Walter Black ( A grandson of the founder ) said that they bought non-exclusive rights to books for from between $15,000 and $55,000. 
\"A book may get 5,000 to 6,000 copies sold in trade. If we buy the rights, we can get 10 times the volume in sales\".""".replace(chr(10),'')
	addpGraph( chapter, p)

	strs = []
	strs.append( PdfString( ftrFont.asItalic(), "Newsday "))
	strs.append( PdfString( ftrFont," Nassau and Suffolk Edition, Long Island. 26 Dec 1988. p.6." ))
	addFnStrs(chapter, strs)


	addSubHead( chapter, "A Final Word")

	p = """There is some uncertainty about the last years of the Detective Book Club. Because it was a book club 
it did not receive the kind of attention that regular trade publishers did and do. 
The phrase \"A selection of the Detective Book Club\" appears many times in the pages of Publishers Weekly , 
but the club otherwise received very little attention.  It was a major source of ad revenue for newspapers and periodicals; 
it pioneered various forms of direct advertising such as postcard inserts in paperbacks and
magazines, but in its final years it received very little notice.  """.replace(chr(10),'')
	addpGraph( chapter, p)

	p = """The identification of titles after 1983 is based on personal research, not on company records.  
In spite of the very large number of volumes identified through the end of the 1990's it is very likely that this listing is incomplete. """.replace(chr(10),'')
	addpGraph( chapter, p)


	chapter.printChapter()
	#
	# end if introduction()
	
	
#chapter.buildPages()
#for page in chapter.pages:
#	page.dumpPage()

doc = PdfDocument()

doc.beginDoc('test_PdfText.pdf')
doc.setPageSize( 8.5, 5.5, 'i')
doc.setLineHeightFactor(1.1)
doc.setLeftMargin(0.5,'i')
doc.setRightMargin(0.5,'i')
doc.setTopMargin(0.25,'i')
doc.setBottomMargin(0.5,'i')
		
doc.setDefaultUnit('p')

introduction( doc )

doc.endDoc()
print ('See test_PdfText.pdf')



