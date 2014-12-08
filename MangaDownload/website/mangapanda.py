"""
    Manga Downloader
    Author: Aaditya M Nair (Prometheus)	
    Created On : Sun 07 Dec 2014 20:35:19 IST

    Website Parser Module for MangaPanda
"""
from webpage import WebResponse

try:
    from bs4 import BeautifulSoup
except ImportError:
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        print "Please Install BeautifulSoup4 and try again"
        exit(-1)


def get_manga_list():
    manga_list={}

    res=WebResponse("http://www.mangapanda.com/alphabetical")
    soup=BeautifulSoup(res.page)

    name_wise_list=soup.find_all('ul',class_='series_alpha')

    for ul in name_wise_list:
        item=ul.find_all("li")
        for li in item:
            manga_name,manga_loc = li.a.string, li.a['href']
            manga_list[manga_name]=manga_loc
    return manga_list

def get_chapter_count(chapter_list_location):
    soup = BeautifulSoup( WebResponse( chapter_list_location ).page )
    lis = soup.find_all('div', class_='chico_manga')
    count=len(lis)

    if count > 12:
        return count - 6
    else:
        return count/2
