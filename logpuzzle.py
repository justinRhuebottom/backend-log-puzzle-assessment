#!/usr/bin/env python2
"""
Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

import os
import re
import sys
import urllib.request
import argparse


def read_urls(filename):
    """Returns a list of the puzzle URLs from the given log file,
    extracting the hostname from the filename itself, sorting
    alphabetically in increasing order, and screening out duplicates.
    """
    with open(filename) as f:
        text = f.read()

    # Find Puzzle URLs and sort them
    if filename == "animal_code.google.com":
        pattern = (r"/\w+/\w+/\w+-\w+-\w+/\w+/\w+/\w+-\w+\b.jpg")
        duplicates = re.findall(pattern, text)
        duplicates.sort()
    if filename == "place_code.google.com":
        pattern = (r"/\w+/\w+/\w+-\w+-\w+/\w+/\w+/\w+-\w+-\w+\b.jpg")
        duplicates = re.findall(pattern, text)
        duplicates.sort(key=lambda x: x[-8:-4])

    # Remove duplicate URLs and give them correct formatting
    short_urls = []
    [short_urls.append(x) for x in duplicates if x not in short_urls]
    urls = []
    for index, item in enumerate(short_urls):
        urls.insert(index, "http://" + filename.split("_", 1)[1] + item)
    return urls


def download_images(img_urls, dest_dir):
    """Given the URLs already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory with an <img> tag
    to show each local image file.
    Creates the directory if necessary.
    """
    dest_dir = dest_dir.split(" ")[0]
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    img_tags = []

    absolute_path = os.path.abspath(dest_dir)
    # Download each file and write its img tag
    for i, url in enumerate(img_urls):
        print("Retrieving... " + url)
        urllib.request.urlretrieve(url, dest_dir + f"/img{i}.jpg")
        img_tags.append(f"<img src={absolute_path}/img{i}.jpg>")
    img_tags = "".join(img_tags)
    html_string = f"""
    <html>
    <body>
    {img_tags}
    </body>
    </html>
    """
    with open(f"{dest_dir}/index.html", "w") as f:
        f.write(html_string)


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument(
        'logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
