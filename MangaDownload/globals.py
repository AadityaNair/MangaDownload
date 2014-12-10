"""
    Manga Downloader
    Author: Aaditya M Nair (Prometheus)	
    Created On : Sun 07 Dec 2014 18:21:10 IST

    This file contains all the globally accessible variables for the program.
"""

def init():
    global manga, user_details
    user_details={}

    manga = None  # Supposed to hold the Manga Object.
    user_details['manga_name']= None
    user_details['location']= None
    user_details['begin']= 0
    user_details['end']= 0
