"""
    Code to download manga

    Creator: Aaditya M Nair ( a.k.a Prometheus ) 
    Created: 22 April, 2014

    Requires BeautifulSoup4
"""
#------------------Data Constants--------------------#
site            = 'http://www.mangapanda.com'
manga_name      = None
target_location = '.'
chapter_range   = {}


#--------------------Imports------------------------#
import os, argparse,urllib2
try:
    from bs4 import BeautifulSoup
except ImportError:
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        print "Please Install BeautifulSoup4 and try again"
        exit(-1)

#------------------------Main Integrator Function--------------------------#

def main_function():
    if not os.path.exists( manga_name ):
        os.mkdir( manga_name )
    os.chdir( manga_name )

    isNumeric=check_numeric_chapters()

    name_list=get_chapters( chapter_range, numeric=isNumeric )
    chapter=chapter_range['begin']
    
    for chapter_name in name_list:
        if not os.path.exists( str(chapter_name) ):
            os.mkdir( str(chapter_name) )
        os.chdir( str(chapter_name) )
        getPages=False
        page=1
        nop=-1

        download_url= site + '/' + manga_name + '/' + str(chapter) + '/'
        print str(chapter_name)

        while page <= nop or not getPages: 
            print '\tPage: %d' %(page), 
            
            if os.path.isfile( str( page ) + '.jpg' ):
                print "\t Already Downloaded."
                page=page+1
                continue

            url=download_url + str(page)
            obj=WebResponse(url)

            if not getPages and not obj.ErrorCode:
                nop=get_number_of_pages( obj.page )
                getPages=True
            if not obj.ErrorCode:
                obj.save_image( str(page) )
            else:
                print "Problem"
                
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
        manga_name=args.manga_name
        target_location=args.target
        if args.chapter:
            chapter_range['begin']=chapter_range['end']=args.chapter
        else:
            chapter_range['begin']=args.begin
            chapter_range['end']=args.end



if __name__=='__main__':
    parse_arguments()

    current_location=os.path.abspath( os.curdir )
    os.chdir( os.path.abspath( target_location ) )

    main_function()
    os.chdir( current_location )

class WebResponse(object):
    def __init__(self,url):
        self.url=url
        self.page=''
        self.ErrorCode=0

        try:
            headers = { 'User-Agent' : 'Mozilla/5.0' }
            req = urllib2.Request(url, None, headers)
            response=urllib2.urlopen(req,timeout=10)
        except urllib2.URLError:
            self.ErrorCode=2  # Network Unreachable
        except urllib2.socket.timeout:
            self.ErrorCode=1  # Connection too slow
        else:
            self.page=response.read()

def save_image(web_page,name):
    if not web_page.ErrorCode:
        page=BeautifulSoup(web_page.page)
        url=page.body.img['src']
    
        image=WebResponse(url)
        if not image.ErrorCode:
            extn=url[url.rfind('.')+1:]
            new_name= str(name)+extn
            
            f=open(new_name,'wb')
            f.write(image.page)
            f.close()

#--------------------------------Functions to generate Metadata-------------------------------#

def get_number_of_pages(response):
    soup=BeautifulSoup(response)

    l=soup.body.find(id='pageMenu').children
    page_count=len(list(l))/2
    return page_count 

def get_chapters( chapter_range, numeric): 
    begin=1
    if chapter_range.has_key('begin'):
        begin=chapter_range['begin']
    if chapter_range.has_key('end'):
        end=chapter_range['end']
    chapter=begin

    if numeric:
        if chapter_range.has_key('end'):
            return range(begin,end+1)
        else:
            return InfiniteSequence(begin)
    
    chapter_list_location=get_list_location( Data['manga_name'] )
    isError=False
    try:
        response=WebResponse( chapter_list_location )
    except ValueError:
        isError=True
    else: 
        if response.ErrorCode:
            isError=True
        else:
            soup=BeautifulSoup(response.page)
            l=soup.body.find_all('tr')
            if not chapter_range.has_key('end'):
                end=len(l)

            return_list=[]
    if isError:
        print 'Unable to download chapter names.Going with numbers'
        return range(begin,end+1)
    
    while chapter >= begin and chapter <= end:
        try:
            name= l[ 11+chapter ].a.string + l[ 11+chapter ].td.contents[4]
        except IndexError:
            break
        return_list.append(name)
        chapter=chapter+1
    return return_list

def get_list_location(manga_name):
    url=cache_url(get=True)
    if url is not False:
        print "Used cached url."
        return url
    
    for i in range(5):
        response=WebResponse("http://www.mangapanda.com/alphabetical")
        if not response.ErrorCode:
            break
        else:
            if response.ErrorCode==2:
                print 'Network Unreachable.Trying again...'
            else:
                print 'Connection too slow.Retrying...'

    if response.ErrorCode==2:
        print 'Network Unreachable.Check your internet or proxy settings and try again.'
        exit(-2)
    if response.ErrorCode==1:
        return 1

    soup=BeautifulSoup(response.page)
    l=soup.find_all('div',class_='series_alpha')
    isExist=False

    for target in l:
        if target.a.string==manga_name[0].upper():
            break
    for loc in target.find_all('li'):
        if loc.a.string.lower()==manga_name.lower():
            isExist=True
            break
    if isExist:    
        print 'List Location Discovered.'
        url=Data['site'] + loc.a['href']
        cache_url(URL=url,get=False)
        return url
    else:
        print 'Manga Name does not exist.Check spelling and try again.'
        exit(-3)

#-----------------------Other Minor Funtions-----------------------#

def check_numeric_chapters():
    a=os.walk('.')
    b=a.next()
    chapter_list=b[1]

    for chapter in chapter_list:
        try:
            int(chapter)
        except ValueError:
            return False
    return True and len(chapter_list)

def cache_url(get,URL=None):
    if not os.path.exists('list_location') and get:
        return False
    f=open('list_location','w+')
    if get:
        text=f.read()
        print text
        return text
    else:
        print >> f, URL
        return True

def InfiniteSequence(begin):
    while True:
        yield begin
        begin+=1

