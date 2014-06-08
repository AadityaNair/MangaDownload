import urllib2
from os import walk

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
        page=BeautifulSoup(self.page)
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
        f.close()

def get_number_of_pages(response):
    soup=BeautifulSoup(response)

    l=soup.body.find(id='pageMenu').children
    page_count=len(list(l))/2
    return page_count 

def get_chapters( chapter_range, numeric): 
    begin=1
    end=len(l)
    if chapter_range.has_key('begin'):
        begin=chapter_range['begin']
    if chapter_range.has_key('end'):
        end=chapter_range['end']
    chapter=begin

    if numeric:
        return range(begin,end+1)

    
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
        return Data['site'] +loc.a['href']
    else:
        print 'Manga Name does not exist.Check spelling and try again.'
        exit(-3)

def check_numeric_chapters():
    a=walk('.')
    b=a.next()
    chapter_list=b[1]

    for chapter in chapter_list:
        try:
            int(chapter)
        except ValueError:
            return False
    return True
