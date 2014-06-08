MangaDownload
=============

Python script to downoad manga from web.It works by scraping images off each manga page.It is useful for people like me who have a slow internet and prefer to read offline.

Dependencies
============

 * Python 2.7
 * BeautifulSoup (use `pip install BeautifulSoup` or `pip install BeautifulSoup4` to install)

Tested on Fedora 20. Should work on any Linux Distribition as long as dependencies are installed.

Features
========

The script offers many features notable a resume featue.
  * **Resume**: Automatically detects missing pages from every chapter and downloads it as long as the download location is same.
  * **Selective Download**: You can specify what range of chapters to download or download a specific chapter.
  * **Destination**: You can specify where to download the manga.

Usage
=====

The script works thru command-line options:

1. This will display all the help related to options available
    ```sh
    python manga.py --help
    ```
2. This will download the manga given by `manga_name` from beginning to end
    ```sh
    python manga.py [manga_name]
    ``` 
3. This will download the manga at location pointed by `TARGET`
    ```sh
    python manga.py [manga_name] --target TARGET
    ```
4. This will download the given manga from chapters `BEGIN` to `END`
    ```sh
    python manga.py [manga_name] -b [BEGIN] -e [END]
    ```
  ***Note that if `-b` is not specified, default is taken as the first chapter.***
  ***Similarly if `-e` is omitted, the program downloads till the last chapter.***

5. This will download only one chapter `CHAPTER`
    ```sh
    python manga.py [manga_name] -c [CHAPTER]
    ``` 
