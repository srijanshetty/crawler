# To get the HTML of the website
import urllib2
from BeautifulSoup import BeautifulSoup
import re
from urlparse import urljoin,urlparse
import sys,traceback

# For searching google
from google import search

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

def getData(soup,link):
	"""Extracts deadline from a given soup element
		Arguments: soup object, link
	"""

	base_url=urlparse(link).netloc

	text = soup.findAll(text=True)
	flag=0
	flag_date=0
	for line in text:
		prev_line = line
		deadline=re.search(r'(.*[Ss]ubmission\s[Dd]eadline*.*)|(.*[Dd]eadline\s[Ss]ubmission*.*)|(.*[Dd]eadline)|(.*[Nn]otification of [Aa]cceptance)|(.*Important Dates.*)', str(line)) # Find all strings matching deadline
		date=re.search(r'(^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d)|(.*January\s*.*)|(.*February\s*.*)|(.*March\s*.*)|(.*April\s*.*)|(.*May\s*.*)|(.*June\s*.*)|(.*July\s*.*)|(.*August\s*.*)|(.*September\s*.*)|(.*October\s*.*)|(.*November\s*.*)|(.*December\s*.*)',str(line))
		if(flag_date):
			due_date=re.search(r'.*[Dd]ue.*',str(line))
			if(due_date):
				print due_date
			#	print prev_line.string
			flag_date=0
		if (deadline):
			# Now we get the base url from the link and add this entry into the database
			flag=1
			flag2=re.search(r'(^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d)|(.*January\s*.*)|(.*February\s*.*)|(.*March\s*.*)|(.*April.*)|(.*May\s*.*)|(.*June\s*.*)|(.*July\s*.*)|(.*August\s*.*)|(.*September\s*.*)|(.*October\s*.*)|(.*November\s*.*)|(.*December\s*.*)',str(deadline.group()))
			print deadline.group()
		if(date):
			flag_date=0
			if(flag):
				if(flag2):
					pass
				else:
					print date.group()
					flag_date=1
					if(flag>=1):
						flag=0
					else:	
						flag=flag+1

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
			print '\nProcessing URL:\t%s' %main_url
			level=main_url.count('/')
			if(level>(depth+1)):
				print "Exceeded Depth of Crawl"
				continue
			getData(soup,main_url)
		except urllib2.URLError:
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason
		  	return None
 
		# Processing the links
		links=soup('a')

		# Processing the tags obtained from the soup and converting them to urls
		for link in links:
			# Regex for the URL
			urls=re.search(r'href=["]([^"]*)["]','%s' %link)
			if(urls):
				url=urls.group(1)

				# Joining the URL
				temp_url=urljoin(main_url,url)
				temp_url_netloc=urlparse(temp_url).netloc

				# Restricting only to our site
				if(temp_url_netloc != main_url_netloc): 
					print 'Skipping URL:\t%s' %temp_url
				elif(temp_url_netloc in blacklist_urls):
					print 'Skipping URL:\t%s' %temp_url
				elif(temp_url not in processed_urls):
					level=temp_url.count('/')
					if(level>(depth+1)):
						print "Exceeded Depth of Crawl"
						break
					processed_urls.append(temp_url)
					print 'Adding URL:\t%s' %temp_url	
	
def frontier():
	""" Crawls the given seed URLS """
	
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
		
	# Performing a google search and looping through the results
	print "Initializing"
	print "Querying google for urls"
	try:
		google_search=search(search_query, stop=10)
		for url in google_search:
			if(urlparse(url).netloc in blacklist_urls):
				print "\nSkipping URL:\t%s" %url
			else:
				print "\nAdding URL:\t%s" %url
				processed_urls.append(url)
	except urllib2.HTTPError, e:
	    print 'The server couldn\'t fulfill the request.'
	    print 'Error code: ',e.code
	except urllib2.URLError, e:
		print 'We failed to reach a server.'
		print 'Reason: ',e.reason

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



