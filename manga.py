"""
    Code to download manga

    Creator: Aaditya M Nair ( a.k.a Prometheus ) 
    Created: 22 April, 2014

    Requires BeautifulSoup4
"""

__builtins__.Data={
        'site'            : 'http://www.mangapanda.com',
        'manga_name'      : None,
        'target_location' : '.',
        'chapter_range'   : {}
        }
import os, argparse 
import requisites

def main_function():
    if not os.path.exists( Data['manga_name'] ):
        os.mkdir( Data['manga_name'] )
    os.chdir( Data['manga_name'] )

    isNumeric=requisites.check_numeric_chapters()

    name_list=requisites.get_chapters( Data['chapter_range'], numeric=isNumeric )
    chapter=Data['chapter_range']['begin']
    
    for chapter_name in name_list:
        if not os.path.exists( str(chapter_name) ):
            os.mkdir( str(chapter_name) )
        os.chdir( str(chapter_name) )
        getPages=False
        page=1
        nop=-1

        download_url= Data['site'] + '/' + Data['manga_name'] + '/' + str(chapter) + '/'
        print str(chapter_name)

        while page <= nop or not getPages: 
            print '\tPage: %d' %(page), 
            
            if os.path.isfile( str( page ) + '.jpg' ):
                print "\t Already Downloaded."
                page=page+1
                continue

            url=download_url + str(page)
            obj=requisites.WebResponse(url)

            if not getPages and not obj.ErrorCode:
                nop=requisites.get_number_of_pages( obj.page )
                getPages=True
            obj.save_image( str(page) )
            if obj.isSaved:
                print "\t Downloaded."
            else:
                print "\t Unable to Downloaded."
            page=page+1

        chapter=chapter+1	
        os.chdir('..')

    os.chdir('..')
    print "Whole manga Downloaded"

def parse_arguments():
    parser=argparse.ArgumentParser()

    parser.add_argument('manga_name',
            type=str,
            help="Input the name of the manga."
            )
    parser.add_argument('-b','--begin',
            type=int,
            help='Input the starting chapter.Defaults to first chapter.'
            )
    parser.add_argument('-e','--end',
            type=int,
            help='Input the ending chapter.Defaults to the last possible chapter.'
            )
    parser.add_argument('-c','--chapter',
            type=int,
            help='Provide if you want to download only one chapter.'
            )
    parser.add_argument('-t','--target',
            type=str,
            help='The location where manga has to be downloaded.Defaults to the current directory.',
            default='.'
            )
    args=parser.parse_args()
    if args.chapter and (args.begin or args.end):
        print '--chapter cannot be specified with --begin/--end. \n'
        parser.parse_args('--help'.split())
    else:
        Data['manga_name']=args.manga_name
        Data['target_location']=args.target
        if args.chapter:
            Data['chapter_range']['begin']=Data['chapter_range']['end']=args.chapter
        else:
            Data['chapter_range']['begin']=args.begin
            Data['chapter_range']['end']=args.end



if __name__=='__main__':
    parse_arguments()

    current_location=os.path.abspath( os.curdir )
    os.chdir( os.path.abspath( Data['target_location'] ) )

    main_function()
    os.chdir( current_location )
