# To get the HTML of the website
import urllib2
from BeautifulSoup import BeautifulSoup
import re
from urlparse import urljoin, urlparse
import sys,traceback
import os

# For searching google
from google import search						

# Global variables
processed_urls=[]
blacklist_urls=[]
deadline_urls=[]

# File to store the urls
processed_urls_file=open('processed_urls','w')

def getHTML(link):
	"""Extract HTML from a page and return HTML text
		Arguments: link
	"""

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
	
def getDeadline(soup,link):
	"""Extracts deadline from a given soup element
		Arguments: soup object, link
	"""
	
	text=soup.findAll(text=True) # Extract text from the soup object
	for line in text:
		deadline=re.findall(r'[Dd]eadline.*\d.*', str(line)) # Find all strings matching deadline
		if (deadline):
			# Now we get the base url from the link and add this entry into the database
			base_url=urlparse(link).netloc
			print base_url, deadline

def crawl(main_link,depth):
	"""Extracts HTML from a URL, and gets the links from them
	Arguments: link, depth_crawling
	"""

	# Create a soup and check for HTML Errors
	HTML=getHTML(main_link)
	if(HTML):
		soup=BeautifulSoup(HTML)
	else:
		return None # Nothing to do if we get a null from the URL

	# Do data processing over here

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
			if(temp_url not in processed_urls and temp_url not in blacklist_urls): # Check if the URL is in processed list
				processed_urls.append(temp_url)
				processed_urls_file.write("%s\n" %temp_url)
				print '\nCrawling URL: %s' %temp_url
				crawl(temp_url,depth-1) # Search for more links
	
def frontier():
	""" Does a google search and then crawls"""
	
	# Checking for parameters
	try:
		search_query=str(sys.argv[1])
	except IndexError:
		print "You have not enter a search string.\nExiting Now"
		sys.exit()
	
	try:
		depth=int(sys.argv[2])
	except IndexError:
		print "You have not entered the depth of crawl, using 1 as the depth"
		depth=1

	# Loading the list of blacklist_urls
	try:
		blacklist_file=open('blacklist.txt','r')
	except IOError:
		pass
	else:
		for item in blacklist_file.read().split('\n'):
			blacklist_urls.append(item)
		
	print '\n############Starting the crawl##############'

	# Performing a google search and looping through the results
	try:
		google_search=search(search_query, stop=20)
	except urllib2.HTTPError, e:
	    print 'The server couldn\'t fulfill the request.'
	    print 'Error code: ',e.code
	    return None
	except urllib2.URLError, e:
		print 'We failed to reach a server.'
		print 'Reason: ',e.reason
		return None

	for url in google_search:
		if(urlparse(url).netloc in blacklist_urls):
			print "\nSkipping URL: %s" %url
			processed_urls.append(url)
		else:
			print "\nCrawling URL: %s" %url
			crawl(url,depth)		

if __name__ == '__main__':
	
	# Changing the encoding of the file
	reload(sys)
	sys.setdefaultencoding("utf-8")
	
	# Executing the code
	try:
		frontier()
	except KeyboardInterrupt:
		sys.exit()
	except Exception, e:
		traceback.print_exc()