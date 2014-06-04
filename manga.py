"""
    Code to download manga

    Creator: Aaditya M Nair 
    Created: 22 April, 2014

    Requires BeautifulSoup4
"""

__builtins__.Data={
        'site'            : 'http://www.mangapanda.com/',
        'manga_name'      : 'Naruto',
        'target_location' : '/home/aaditya',
        'proxy_url'       : None
        }
__builtins__.chapter_list_location='http://www.mangapanda.com/93/naruto.html'

import os, sys
import requisites

def main_function():
    if not os.path.exists( Data['manga_name'] ):
        os.mkdir( Data['manga_name'] )
    os.chdir( Data['manga_name'] )

    name_list=requisites.get_chapters()
    chapter=0

    for chapter_name in name_list:
        chapter=chapter+1	
        if not os.path.exists( chapter_name ):
            os.mkdir( chapter_name )
        os.chdir( chapter_name )

        download_url= Data['site'] + manga_name + '/' + str(chapter) + '/'
        obj=requisites.WebResponse(download_url)
        nop=get_number_of_pages(obj.page)

        print chapter_name
        for page in range(1,nop+1):
            if os.path.isfile( str( page ) + '.jpg' ):
                continue

            url=download_url + str(page)
            obj=requisites.WebResponse(url)
            obj.save_image( str(page) )
            print "\tPage: %d\tDownloaded." %(chapter,page)


        os.chdir('..')

    os.chdir('..')
    print "Whole manga Downloaded"



if __name__=='__main__':
    if len(sys.argv)==2:
        proxy_url=sys.argv[1]

    current_location=os.path.abspath( os.curdir )
    os.chdir( target_location )

    main_function()
    os.chdir( current_location )
