# To get the HTML of the website
import urllib2
from BeautifulSoup import BeautifulSoup
import re
from urlparse import urljoin
import sys,traceback

processed_urls=[]

def getHTML(link):
	"""Extract HTML from a page and return HTML text"""

	# Request for the page and provide the site with our User-Agent
	request=urllib2.Request(link)
	request.add_header("User-Agent", "My Python Crawler")
	opener=urllib2.build_opener()
	response=opener.open(request)
	
	# Get the HTML from the page
	return response.read()

def getData(link):
	"""Function to get Data tuple through the page"""

	soup=BeautifulSoup(getHTML(link))
	tds=soup('td', {"class":"nameColumn"})
	for td in tds:
		title=td.find('span', {"class":"venueAlive venueKeywords"})
		location=td.nextSibling.find('span', {"class":"venueAlive"})
		deadline=td.nextSibling.nextSibling.find('span', {"class":"venueAlive"})
		start_date=td.nextSibling.nextSibling.nextSibling.find('span', {"class":"venueAlive"})
		if(title):
			print title.string,location.string,deadline.string,start_date.string

def crawl(main_link,depth):
	"""Extracts HTML from a URL, and gets the links from them"""

	# Do data processing over here
	if(re.findall(r'.*graphicView.*', '%s' %main_link)):
		getData(main_link[:len(main_link)-1]+"0")

	# Checking for depth
	if(depth==0):
		return

	# Create a soup
	soup=BeautifulSoup(getHTML(main_link))

	# Processing the links
	links=soup('a')
	
	# Processing the tags obtained from the soup and converting them to urls
	for link in links:
		urls=re.findall(r'href=["]([^"]*)["]','%s' %link)  # Regex for the URL 
		for url in urls:
			temp_url=urljoin(main_link,url)
			if(temp_url not in processed_urls): # Check if the URL is in processed list
				processed_urls.append(temp_url)
				print '\nCrawing URL: %s' %temp_url
				crawl(temp_url,depth-1) # Search for more links
	
def frontier():
	""" Loops through all the seed URLS"""
	
	# The seed urls
	seeds=["http://www.confsearch.org"]
	
	# Checking for depth argument
	try:
		depth=int(sys.argv[1])
	except IndexError:
		depth=1

	print '\nStarting the crawling'

	# Looping through the seeds
	for seed in seeds:
		print '\nSeed URL: %s' %seed
		crawl(seed,depth)

if __name__ == '__main__':
	try:
		frontier()
	except KeyboardInterrupt:
		sys.exit()
	except Exception, e:
		traceback.print_exc()



