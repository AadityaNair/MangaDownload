"""
    Manga Downloader
    Author: Aaditya M Nair (Prometheus)
    Created On : Sun 07 Dec 2014 20:35:19 IST

    Website Parser Module for MangaPanda
"""
from webpage import WebResponse

manga_list = {}

try:
    from bs4 import BeautifulSoup
except ImportError:
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        print "Please Install BeautifulSoup4 and try again"
        exit(-1)


def get_manga_list():
    """
    Gets the name of all manga by parsing the listing of all mangas.
    """
    res = WebResponse("http://www.mangapanda.com/alphabetical")
    soup = BeautifulSoup(res.page)

    name_wise_list = soup.find_all('ul', class_='series_alpha')

    for ul in name_wise_list:
        item = ul.find_all("li")
        for li in item:
            manga_name, manga_loc = li.a.string, li.a['href']
            manga_list[manga_name] = manga_loc
    return manga_list


def get_chapter_count(chapter_list_location):
    """
    Counts the number of chapters by counting the number of icons(chico_manga)
    beside the ChapterName. Since six chapters are repeated in the recents list,
    the count is reduced by six
    """
    soup = BeautifulSoup(WebResponse(chapter_list_location).page)
    lis = soup.find_all('div', class_='chico_manga')
    count = len(lis)

    if count > 12:
        return count - 6
    else:
        return count / 2


def absoulute_location(manga_name):
    """
    Returns the absolute list location for the manga.
    Assumes that the manga name is in the `manga_list`.
    """
    assert manga_name in manga_list.keys()
    return "http://www.mangapanda.com" + manga_list[manga_name]


def get_page_count(page_in_chapter):
    """
    Returns the number of pages in a chapter.
    `page_in_chapter` is any page of the chapter
    """

    response = WebResponse(page_in_chapter).page

    soup = BeautifulSoup(response)
    partial_list = soup.body.find(id='pageMenu').children
    page_count = len(list(partial_list)) / 2
    return page_count