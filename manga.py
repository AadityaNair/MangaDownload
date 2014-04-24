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

			try:
				web_page=urllib2.urlopen(download_url)
			except urllib2.HTTPError:
				if flag is 0:
					end_flag=True
				break

			print "For Chapter %d:\n" %(chapter)
			Download( web_page.read() , page)
			page=page+1

		if end_flag:
			break
		os.chdir('..')
	
	os.chdir('..')
	print "Whole manga Downloaded\n"




def extractURL(text):
	"""
		Function to scrape the image url from the web page
	"""
	page=bs4.BeautifulSoup(text)
	img_url=page.body.img['src']
	return img_url


def Download(text,page):
	"""
		Function to Download the image and save it in the form of page.jpg
		To Be Added: Detect the format of image.
	"""
	
	img_url=extractURL(text)
	response=urllib2.urlopen(img_url)

	new_name=str(page)+'.jpg'
	f=open(new_name,'wb')
	f.write( response.read() )
	print "\t Page %d downloaded...\n" %(page)

