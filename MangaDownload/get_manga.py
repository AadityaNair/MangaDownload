"""
    Manga Downloader
    Author: Aaditya M Nair (Prometheus)	
    Created On : Sat 13 Dec 2014 17:14:07 IST

    Gets the best possible manga from the website
"""

from fuzzywuzzy import process

def get_name_list(site='mangapanda'):
    """
    Gets all the names of manga from the site.
    """
    global website_specific

    if site=='mangapanda':
        from website import mangapanda
        website_specific=mangapanda
    else:
        return []
    return website_specific.get_manga_list()

def ask_best_match(matches):
    """
    Asks the user for the best possible match.
    If `matches` contains only one element that element is returned.
    If it contains no elements, it exits with  status -2.
    """
    if( len( matches ) == 0 )
        print "No Manga matches the given name."
        exit(-2)

    if( len( matches ) == 1 )
        return matches[0]
# TODO Complete user input for multiple matches
    

def get_best_match_location(manga_name, choices):
    """
    Extracts the best possible matching manga.
    If it cannot find the exact match asks the user for the best matches.
    """
    
    matches=process.extractBests(manga_name, choices, limit=10, score_cutoff=100)
    if( len(matches) == 0 ):
        matches=process.extractBests(manga_name, choices, limit=10, score_cutoff=80)

    match=ask_best_match(matches)
    return website_specific.absoulute_location( match )
