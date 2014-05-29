"""
	Code to download manga
	
	Creator: Prometheus
	Created: 22 April, 2014

	Requires BeautifulSoup4
"""

__builtins__.site='http://www.mangapanda.com/'
__builtins__.manga_name='naruto'
__builtins__.target_location="/home/aaditya/" 

__builtins__.final_chapter=676
__builtins__.chapter_list_location='http://www.mangapanda.com/93/naruto.html'
__builtins__.proxy_url=''

import os,requisites

def main_function():
	if not os.path.exists(manga_name):
		os.mkdir(manga_name)
	os.chdir(manga_name)
	
	name_gen=requisites.get_chapters()
	
	for chapter in range( 1 , final_chapter ):
		chapter_name=name_gen.next()
		if os.path.exists( chapter_name ):
			continue
		else:
			os.mkdir( chapter_name )
		os.chdir( chapter_name )

		download_url= site + manga_name + '/' + str(chapter) + '/'
		obj=requisites.WebResponse(download_url)
		nop=get_number_of_pages(obj.page)

		for page in range(1,nop+1):
			url=download_url + str(page)
			
			obj=requisites.WebResponse(url)
			obj.save_image( str(page) )
			print "Chapter: %d\tPage: %d\tDownloaded." %(chapter,page)


		os.chdir('..')
	
	os.chdir('..')
	print "Whole manga Downloaded\n"



if __name__=='__main__':
	current_location=os.path.abspath( os.curdir )
	os.chdir( target_location )
	
	main_function()
	os.chdir( current_location )
