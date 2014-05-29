try:
	import urllib2, bs4
except ImportError:
	print "Please Install BeautifulSoup4 and try again"
	exit(-1)


proxy=urllib2.ProxyHandler({ 'http':proxy_url })
opener=urllib2.build_opener(proxy)
urllib2.install_opener(opener)	
	
class WebResponse(object):
	def __init__(self,url):
		self.url=url
		self.page=''

		try:
			response=urllib2.urlopen(url)
		except urllib2.HTTPError:
			print 'error'
		else:
			self.page=response.read()

	def get_image(self):
		"""
			Function to scrape image from URL and return response
		"""
		page=bs4.BeautifulSoup(self.page)
		url=page.body.img['src']
		return WebResponse(url)
	
	def save_image(self,name):
		"""
			Function to save image.
		"""
		image=self.get_image()
		new_name= str(name)+'.jpg'
		f=open(new_name,'wb')
		f.write(image.page)

def get_number_of_pages(response):
	soup=bs4.BeautifulSoup(response)
	
	l=soup.body.find(id='pageMenu').children
	page_count=len(list(l))/2
	return page_count 


def get_chapters():
	response=WebResponse( chapter_list_location )
	soup=bs4.BeautifulSoup(response.page)
	l=soup.body.find_all('tr')
	length=len(l)
	for i in range(length):
		try:
			name= l[12+i].a.string + l[12+i].td.contents[4]
		except IndexError:
		 	break
		yield name


