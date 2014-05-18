"""
	Code to download manga
	
	Creator: Prometheus
	Created: 22 April, 2014

	Requires BeautifulSoup4
"""

import os
import urllib2
import bs4

'''# ------ Code to Handle Proxy:

#proxy_url='proxy.iiit.ac.in:8080'
proxy_url=''
proxy=urllib2.ProxyHandler({ 'http':proxy_url })
opener=urllib2.build_opener(proxy)
urllib2.install_opener(opener)	
'''

site='http://www.mangapanda.com/'
manga_name='naruto'

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


	for chapter in range(1,4):
		if os.path.exists( str(chapter) ):
			continue
		else:
			os.mkdir( str(chapter) )
		os.chdir( str(chapter) )

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


def get_number_of_chapters(response):
	soup=bs4.BeautifulSoup(response.page)
	
	l=soup.body.find(id='chapterMenu').children
	chapter_count=len(list(l))
	return chapter_count

if __name__=='__main__':
	main_function()
