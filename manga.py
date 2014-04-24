"""
	Code to download manga
	
	Creator: Prometheus
	Created: 22 April, 2014

	Requires BeautifulSoup4
"""

import os
import urllib2
import bs4

manga_name='Naruto'
site='http://www.mangapanda.com/'

chapter=1
page=0

class WebResponse(object):
	def __init__(self,url):
		self.url=url

		response=urllib2.urlopen(url)
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
		page=self.get_image()
		new_name= str(name)+'.jpg'
		f=open(new_name,'wb')
		f.write(self.page)
		
	

def main_function():
	if not os.path.exists(manga_name):
		os.mkdir(manga_name)
	os.chdir(manga_name)
	end_flag=True


	for chapter in range(1,4):
		os.mkdir( str(chapter) )
		os.chdir( str(chapter) )

		while True:
			download_url=site + str(chapter) + '/' 
			if page != 0:
				download_url=download_url + str(page) + '/'

			response=WebResponse(url)
			
			print "For Chapter %d:\n" %(chapter)
			Download( response , page)
			page=page+1

		if end_flag:
			break
		os.chdir('..')
	
	os.chdir('..')
	print "Whole manga Downloaded\n"
