"""
    Manga Downloader
    Author: Aaditya M Nair (Prometheus)	
    Created On : Sun 07 Dec 2014 18:04:12 IST

    This file parses the user input for further processing
"""

import argparse

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
args = parser.parse_args()
if args.chapter and (args.begin or args.end):
    print '--chapter cannot be specified with --begin/--end. \n'
    parser.parse_args('--help'.split())
else:
    global manga_name,target_location,chapter_name

    manga_name = args.manga_name
    target_location = args.target
    if args.chapter:
        chapter_range['begin'] = chapter_range['end'] = args.chapter
    else:
# Both args.begin and args.end is None if not specified.
        chapter_range['begin'] = args.begin
        chapter_range['end'] = args.end

