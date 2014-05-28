"""
	Code to download manga
	
	Creator: Prometheus
	Created: 22 April, 2014

	Requires BeautifulSoup4
"""

site='http://www.mangapanda.com/'
manga_name='naruto'
target_location="/home/aaditya/" 

final_chapter=676
chapter_list_location='http://www.mangapanda.com/93/naruto.html'
proxy_url=''

import os, urllib2

try:
	import bs4
except ImportError:
	print "Please Install BeautifulSoup4 and try again"
	exit(-1)


# ------ Code to Handle Proxy:

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
	

def main_function():
	if not os.path.exists(manga_name):
		os.mkdir(manga_name)
	os.chdir(manga_name)
	
	name_gen=get_chapters()
	
	for chapter in range( 1 , final_chapter ):
		chapter_name=name_gen.next()
		if os.path.exists( chapter_name ):
			continue
		else:
			os.mkdir( chapter_name )
		os.chdir( chapter_name )

		download_url= site + manga_name + '/' + str(chapter) + '/'
		obj=WebResponse(download_url)
		nop=get_number_of_pages(obj.page)

		for page in range(1,nop+1):
			url=download_url + str(page)
			
			obj=WebResponse(url)
			obj.save_image( str(page) )
			print "Chapter: %d\tPage: %d\tDownloaded." %(chapter,page)


		os.chdir('..')
	
	os.chdir('..')
	print "Whole manga Downloaded\n"



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


if __name__=='__main__':
	current_location=os.path.abspath( os.curdir )
	os.chdir( target_location )
	
	main_function()
	os.chdir( current_location )
