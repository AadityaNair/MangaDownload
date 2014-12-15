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


def get_and_save_image(page, name):
    soup = BeautifulSoup(page)
    img_url = soup.body.img['src']

    image = WebResponse(img_url).page
    extn = img_url[img_url.rfind('.'):]
    image_name = name + str(extn)

    f = open(image_name, 'wb')
    f.write(image.page)
    f.close()


def MangaIterator(chapter_list_location, begin, end):
    """
    Returns an Iterator to each page in the chapter.
    """

    chapter_count = get_chapter_count(chapter_list_location)
    if begin is None:
        begin = 1
    if end is None:
        end = chapter_count
    assert begin <= chapter_count <= end

    import re
    # Assumed that the prefix for chapters is found on list location
    regex = '^http://www.mangapanda.com/\w*/(.*)\.html$'
    reg = re.compile(regex)
    match = reg.match(chapter_list_location)

    prefix = match.group(1)

    # url will be of the form http://www.mangapanda.com/prefix/chapter_no/page_no

    manga_base_url = "http://www.mangapanda.com/" + prefix + '/'
    chapter_no = begin

    while begin <= chapter_no <= end:
        chapter_base_url = manga_base_url + str(chapter_no) + '/'
        number_of_pages = get_page_count(chapter_base_url)

        assert number_of_pages is not None

        page=1
        while page <= number_of_pages:
            page_url = chapter_base_url + str(page)
            yield page_url
            page += 1
        chapter_no += 1