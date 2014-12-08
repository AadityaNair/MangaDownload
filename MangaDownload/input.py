"""
    Manga Downloader
    Author: Aaditya M Nair (Prometheus)	
    Created On : Sun 07 Dec 2014 18:04:12 IST

    This file parses the user input for further processing
"""

import argparse
from . import globals

def create_parser():
    """
    Defines the command line arguments and parses arguments.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('manga_name',
            type = str,
            help = "Input the name of the manga."
            )
    parser.add_argument('-b','--begin',
            type = int,
            help = 'Input the starting chapter.Defaults to first chapter.'
            )
    parser.add_argument('-e','--end',
            type = int,
            help = 'Input the ending chapter.Defaults to the last possible chapter.'
            )
    parser.add_argument('-c','--chapter',
            type = int,
            help = 'Provide if you want to download only one chapter.'
            )
    parser.add_argument('-t','--target',
            type = str,
            help = 'The location where manga has to be downloaded.Defaults to the current directory.',
            default = '.'
            )
    parser.add_argument('-s','--site',
            type = str,
            help = 'The site through which the manga has to be downloaded. Defaults to MangaPanda.',
            default = 'mangapanda'
            )

    return parser
def parse_input():
    parser=create_parser()
    args=parser.parse_args()
    if args.chapter and (args.begin or args.end):
        print '--chapter cannot be specified with --begin/--end. \n'
        parser.parse_args('--help'.split())
    else:
# Make all inputs available globally
        globals.user_details['manga_name'] = args.manga_name
        globals.user_details['location'] = args.target
        if args.chapter:
            globals.user_details['begin'] = globals.user_details['end'] = args.chapter
        else:
# Both args.begin and args.end is None if not specified.
            globals.user_details['begin'] = args.begin
            globals.user_details['end'] = args.end

