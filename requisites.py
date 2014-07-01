import urllib2
from os import walk as os 
import csv
try:
    from bs4 import BeautifulSoup
except ImportError:
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        print "Please Install BeautifulSoup4 and try again"
        exit(-1)

class WebResponse(object):
    def __init__(self,url):
        self.url=url
        self.page=''
        self.ErrorCode=0
        self.isSaved=False

        try:
            response=urllib2.urlopen(url,timeout=10)
        except urllib2.URLError:
            #Network Unreachable.
            self.ErrorCode=2
        except urllib2.socket.timeout:
            #Internet Connection too slow
            self.ErrorCode=1
        else:
            self.page=response.read()

    def get_image(self):
        """
            Function to scrape image from URL and return response
        """
        if not self.ErrorCode:
            page=BeautifulSoup(self.page)
            url=page.body.img['src']
            return WebResponse(url)

    def save_image(self,name):
        """
            Function to save image.
        """
        image=self.get_image()

        if not image and not image.ErrorCode:
            new_name= str(name)+'.jpg'
            f=open(new_name,'wb')
            f.write(image.page)
            f.close()
            self.isSaved=True

def get_number_of_pages(response):
    soup=BeautifulSoup(response)

    l=soup.body.find(id='pageMenu').children
    page_count=len(list(l))/2
    return page_count 

def InfiniteSequence(begin):
    while True:
        yield begin
        begin+=1

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
    if url:
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
        cache_url(data=url,get=False)
        return url
    else:
        print 'Manga Name does not exist.Check spelling and try again.'
        exit(-3)

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
        return f.read()
    else:
        print >> f, URL
        return True
