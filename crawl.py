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
	# try and except check for common HTML Errors
	try:
		request=urllib2.Request(link)
		request.add_header("User-Agent", "My Python Crawler")
		opener=urllib2.build_opener()
		response=opener.open(request)
	except urllib2.HTTPError, e:
	    print 'The server couldn\'t fulfill the request.'
	    print 'Error code: ',e.code
	    return None
	except urllib2.URLError, e:
		print 'We failed to reach a server.'
		print 'Reason: ',e.reason
		return None

	# Get the HTML from the page
	return response.read()

def getDeadline(soup):
	"""Extracts deadline from a given soup element"""
	
	text=soup.findAll(text=True)
	for line in text:
		deadline=re.findall(r'[Dd]eadline.*', str(line)) # Find all strings matching deadline
		if (deadline):
			print deadline
	
def crawl(main_link,depth):
	"""Extracts HTML from a URL, and gets the links from them"""

	# Create a soup and check for HTML Errors
	HTML=getHTML(main_link)
	if(HTML):
		soup=BeautifulSoup(HTML)
	else:
		return None # Nothing to do if we get a null from the URL

	# Do data processing over here
	try:
		getDeadline(soup) # Processing statement
	except urllib2.URLError:
		print 'We failed to reach a server.'
		print 'Reason: ', e.reason
	  	return None

	# Checking for depth
	if(depth==0):
		return

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
	seeds=["http://algo2013.inria.fr/esa-call.shtml"]
	
	# Checking whether the depth argument is passed in the call to the program or not
	try:
		depth=int(sys.argv[1])
	except IndexError:
		depth=1

	print '\nStarting the crawling'

	# Looping through the seeds in our seeds list
	for seed in seeds:
		if(seed not in processed_urls): # Check if the URL is in processed list or urls
			processed_urls.append(seed)
			print '\nSeed URL: %s' %seed
			crawl(seed,depth)

if __name__ == '__main__':
	try:
		frontier()
	except KeyboardInterrupt:
		sys.exit()
	except Exception, e:
		traceback.print_exc()



