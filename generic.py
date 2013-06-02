# To get the HTML of the website
import urllib2
from BeautifulSoup import BeautifulSoup
import re
from urlparse import urljoin,urlparse
import sys,traceback

processed_urls=[]
blacklist_urls=[]

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

def getData(soup):
	"""Extracts deadline from a given soup element
		Arguments: soup object, link
	"""

	text = soup.findAll('a')
	for line in text:
		if (line.string==u'Free'):
			print "Found"

def crawl(depth):
	"""Extracts HTML from a URL, and gets the links from them
	Arguments: link, depth_crawling
	"""

	for main_url in processed_urls:
		main_url_netloc=urlparse(main_url).netloc

		# Create a soup and check for HTML Errors
		HTML=getHTML(main_url)
		if(HTML):
			soup=BeautifulSoup(HTML)
		else:
			return None # Nothing to do if we get a null from the URL

		# Do data processing over here
		try:
			getData(soup)
		except urllib2.URLError:
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
		  	return None

		# Processing the links
		links=soup('a')
	
		# Processing the tags obtained from the soup and converting them to urls
		for link in links:
			urls=re.findall(r'href=["]([^"]*)["]','%s' %link)  # Regex for the URL 
			for url in urls:
				temp_url=urljoin(main_url,url)
				temp_url_netloc=urlparse(temp_url).netloc

				# Restricting only to our site
				if(temp_url_netloc != main_url_netloc): 
					print '\nSkipping URL:\t%s' %temp_url
					continue
				elif(temp_url_netloc in blacklist_urls):
					print '\nSkipping URL:\t%s' %temp_url
				elif(temp_url not in processed_urls):
					processed_urls.append(temp_url)
					print '\nAdding URL:\t%s' %temp_url
	
def frontier():
	""" Crawls the given seed URLS """
	
	# Checking for parameters
	try:
		processed_urls.append(sys.argv[1])
	except IndexError:
		print "You have not entered a seed.\nExiting Now"
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
		
	print '\n--------------Starting the crawl----------------'

	# Performing a google search and looping through the results
	crawl(depth)

	print '\n----------------End of crawl--------------------'

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



