"""
    MangaDownloader (Tests)
    Author: Aaditya M Nair (Prometheus)	
    Created On : Wed 10 Dec 2014 22:05:16 IST

    Tests for the globals.py file.
    Requires nosetests.
"""

import os, sys
sys.path.append( os.path.abspath( '../MangaDownload/' ) )

from nose.tools import *
import globals

def test_non_creation():
    """
    Assert that variables are not created before init()
    """
    try:
        globals.manga
        globals.user_details
    except AttributeError:
        pass
    else:
        raise AttributeError

def test_creation():
    """
    Test whether variables are created after init()
    """
    
    globals.init()
    try:
        globals.manga
        globals.user_details
    except AttributeError:
        raise AttributeError
    else:
        pass
    assert_equals(isinstance(globals.user_details, dict), True)

def test_default_values():
    """
    Check for default values
    """
    
    globals.init()

    assert_equals(globals.manga, None)
    assert_equals(globals.user_details['manga_name'], None)
    assert_equals(globals.user_details['location'], None)
    assert_equals(globals.user_details['begin'], 0)
    assert_equals(globals.user_details['end'], 0)

def test_value_assignment():
    """
    Check if values can be assigned
    """
    test_default_values()
    #manga = ''  # Supposed to hold the Manga Object.
    globals.user_details['manga_name']= 'Naruto'
    globals.user_details['location']= '/home'
    globals.user_details['begin']= 5
    globals.user_details['end']= 10

    assert_equals(globals.user_details['manga_name'], 'Naruto')
    assert_equals(globals.user_details['location'], '/home')
    assert_equals(globals.user_details['begin'], 5)
    assert_equals(globals.user_details['end'], 10)
# Check for Manga Object

def test_value_flush():
    """
    Check if init also flushes values
    """
    test_value_assignment()
    globals.init()
    test_default_values()
    
    
