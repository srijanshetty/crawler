# To get the HTML of the website
import urllib2
from BeautifulSoup import BeautifulSoup
import re
from urlparse import urljoin, urlparse
import sys,traceback
import os

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