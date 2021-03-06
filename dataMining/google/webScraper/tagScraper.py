'''
@author - Eric Kingori
@description  - this scraper is extract all text from most websites
@limitations - cannot extract from Document files such PDFs, word or powerpoints files
@output -  depending usage can either write scraped data to a file or return it as 
a variable to calling module 
'''

import sys
import urllib
import urllib2
import mechanize
from bs4 import BeautifulSoup

#global variables to allow use from other modules
remoteAccess = False
dataset=[]

#This Function sets up the browser 
def browser():
	br = mechanize.Browser();
	br.set_handle_robots(False)
	headers = [("user-agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1")]
	br.addheaders = headers
	return br


#This function sends the request and stores the info from the into an beautifulSoup object
def openLink(br,url):	
	try:	
		rawData =  br.open(url).read()
		soup = BeautifulSoup(rawData)
		return soup
	except urllib2.HTTPError, e:
		print "HTTP Error code: " + str(e.code)
		if (e.code == 404):
			print "Page not found"
		return False

#This function extracts data from an object and save it to the output file or to the list tobe returned
def extractText(soup, filename, write):
	tagList = ['li', 'strong', 'p', 'body', 'em', 'i', 'label', 'title', 'u' ]
	if(write):
		f = open(filename, 'w')
	for tag in tagList:	
		info =soup.findAll(tag)
		for paragraph in info:
			if (write):			
				f.write((paragraph.text).encode('utf-8'))
			else:
				dataset.append((paragraph.text).encode('utf-8'))
	print("Done")
	if(write):
		f.close()
	
	

def run():
	#calling the defined functions
	br = browser()
	filename = "../../output/scrapedData.txt"
	if (len(sys.argv)==1):
		print 'Usage: ' + sys.argv[0] +' [URL]'
		sys.exit(2)
	else:
		url = sys.argv[1]
		print url[-4:] 
		if (url[-4:] == ".pdf"):
			print 'Cannot extract text from pdfs'
			sys.exit(2)
	
	print url
	soup = openLink(br, url)
	if (soup != False):
		extractText(soup, filename)
#to run locallly for independent testing
#run()

#remote call from other Modules
def remote (url, filename, write):
	#calling the defined functions
	br = browser()
	print url
	#ignoring pdfs
	if ".pdf" in url:
			print 'Cannot extract text from pdfs'
			return
	soup = openLink(br, url)
	if (soup != False):
		extractText(soup, filename, write)
	if(write==False):
		read = '\n'.join(dataset)
		return read


