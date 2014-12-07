"""
    Manga Downloader
    Author: Aaditya M Nair (Prometheus)	
    Created On : Sun 07 Dec 2014 20:36:30 IST

    This file contains abstraction of a web page.
"""
import urllib2

class WebResponse(object):
    def __init__(self,url):
        self.url=url
        self.page=''
        self.ErrorCode=0

        try:
            headers = { 'User-Agent' : 'Mozilla/5.0' }
            req = urllib2.Request(url, None, headers)
            response=urllib2.urlopen(req,timeout=10)
        except urllib2.URLError:
            self.ErrorCode=2  # Network Unreachable
        except urllib2.socket.timeout:
            self.ErrorCode=1  # Connection too slow
        else:
            self.page=response.read()


