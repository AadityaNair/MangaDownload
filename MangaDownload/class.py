"""
Manga Downloader Classes
Author: Aaditya M Nair (Prometheus)	
Created On : Sun 07 Dec 2014 17:34:00 IST

This module contains the class definitions for manga and chapters.
"""

class Manga(object):
    """
    Defines the Manga Properties
    Gets Manga Name from User, Calculates all other properties itself.
    """
    def __init__(self, name):
        self.manga_name = name
        self.chapters = 0
        self.list_location = None  # Location of All details of the Manga
        self.description = None    # Description of Manga

class Chapters(object):
    """
    Abstraction for a chapter.
    """
    def __init__(self):
        self.chapter_name = None
        self.page_count = 0
