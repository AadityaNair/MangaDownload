MangaDownload
=============

Python script to downoad manga from web.It works by scraping images off each manga page.It is useful for people like me who have a slow internet and prefer to read offline.

Dependencies
============

  Python 2.7
  BeautifulSoup (use pip install BeautifulSoup or pip install BeautifulSoup4 to install)

Tested on Fedora 20. Should work on any Linux Distribition as long as dependencies are installed.

Features
========

The script offers many features notable a resume featue.
  Resume: Automatically detects missing pages from every chapter and downloads it as long as the download location is same.
  Selective Download: You can specify what range of chapters to download or download a specific chapter.
  Destination: You can specify where to download the manga.

Usage
=====

The script works thru command-line options:
1. python manga.py --help 
   will display all the help related to options available
2. python manga.py [manga_name]
   will download the manga 'manga_name' from beginning to end
3. python manga.py [manga_name] --target TARGET
   will download the manga at the location pointed by TARGET
