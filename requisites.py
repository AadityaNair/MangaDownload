import urllib2

try:
    from bs4 import BeautifulSoup
except ImportError:
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        print "Please Install BeautifulSoup4 and try again"
        exit(-1)
'''
if Data['proxy_url'] is not None:
    proxy=urllib2.ProxyHandler({ 'http':Data['proxy_url'] })
    opener=urllib2.build_opener(proxy)
    urllib2.install_opener(opener)	
'''# For Testing only
class WebResponse(object):
    def __init__(self,url):
        self.url=url
        self.page=''
        self.ErrorCode=0

        try:
            response=urllib2.urlopen(url,timeout=10)
        except urllib2.URLError:
            print "Network Unreachable.Check your internet connection and try again."
            print "If you access internet thru a proxy, supply it by a command line argument"
            exit(-1)
        except urllib2.socket.timeout:
            print 'Internet Connection too slow.Aborting page download.'
            self.ErrorCode=-1
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


def get_chapters( chapter_range ):
    chapter_list_location=get_list_location( Data['manga_name'] )
    response=WebResponse( chapter_list_location )
    
    soup=BeautifulSoup(response.page)
    l=soup.body.find_all('tr')
    return_list=[]
    
    begin=chapter=1
    end=len(l)
    if chapter_range.has_key('begin'):
        begin=chapter_range['begin']
    if chapter_range.has_key('end'):
        end=chapter_range['end']
        
    
    while chapter >= begin and chapter <= end:
        try:
            name= l[ 11+chapter ].a.string + l[ 11+chapter ].td.contents[4]
        except IndexError:
            break
        return_list.append(name)
        chapter=chapter+1
    return return_list

def get_list_location(manga_name):
    response=WebResponse("http://www.mangapanda.com/alphabetical")
    soup=BeautifulSoup(response.page)
    l=soup.find_all('div',class_='series_alpha')
    
    for target in l:
        if target.a.string==manga_name[0].upper():
            break
    for loc in target.find_all('li'):
        if loc.a.string.lower()==manga_name.lower():
            break
    print 'List Location Discovered.'
    return Data['site'] +loc.a['href']
