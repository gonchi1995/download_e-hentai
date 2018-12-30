#!/usr/bin/python3
# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import urllib.request
import urllib.error
import argparse
import os

# List home page
def list_home_page(url: str) -> list:
    # Configure request
    useragent = "Mozilla/5.0"   # User agent
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", useragent)
        with urllib.request.urlopen(req) as page:
            content = page.read()
    except urllib.error.URLError as e:
        print(e)
        return None

    soup = BeautifulSoup(content, "html.parser")
    tdlist = soup.find('div', class_='gtb').findAll("td")

    ref = list()

    for i in tdlist:
        a = i.find("a")

        if a != None:
            ref.append(a.string)

    if "<" in ref:
        ref.remove("<")
    if ">" in ref:
        ref.remove(">")

    ref = list(map(int, ref))

    homelist = list()
    homelist.append(url)

    for i in range(1, max(ref)):
        homelist.append("{}?p={}".format(url, i))

    print("\n".join(homelist))
    return homelist
       
# List viewer page url
def list_viewpage_url(url: str) -> list:
    # Configure request
    useragent = "Mozilla/5.0"   # user agent
    try:
        req = urllib.request.Request(url)   # request
        req.add_header("User-Agent", useragent) # Add request header
        with urllib.request.urlopen(req) as page:  # open
            content = page.read()
    # URL error
    except urllib.error.URLError as e:
        print("URLError: {}".format(e))
        return None
    # HTTP error
    except urllib.error.HTTPError as e:
        print("HTTPError: {}".format(e.code))
        return None

    # Instance of BeautifulSoup
    soup = BeautifulSoup(content, "html.parser")

    # Get url
    gdtm = soup.findAll(class_="gdtm")  # Find gdtm class
    href = [i.find("a").get("href") for i in gdtm]  # Pull url

    print("\n".join(href))

    return href # Return url list
    
def download(url: str) -> bool:
    # Gallery directory
    gallery_dir = "galleries/"+ url.split("/")[-1].split("-")[-2]

    # Configure request
    useragent = "Mozilla/5.0" # user agent
    try:
        # Get view page
        req = urllib.request.Request(url)       # Request
        req.add_header("User-Agent", useragent) # Set user agent
        with urllib.request.urlopen(req) as page:
            content = page.read()   # View page content

        soup = BeautifulSoup(content, "html.parser")    # BeautifulSoup
    except urllib.error.URLError as e:  # URL error
        print(e)
        return False
    else:   # Success
        imgurl = soup.find('img', id="img").get('src')  # image url
        print(imgurl)   

        print("Downloading...{}".format(imgurl))

    try:
        # Get image data
        req2 = urllib.request.Request(imgurl)
        req2.add_header("User-Agent", useragent)
        with urllib.request.urlopen(req2) as img:
            img_content = img.read()

    except urllib.error.URLError as e:
        print(e)

    filename = imgurl.split("/")[-1]    # Image file name
    with open(gallery_dir+"/" +filename, "wb") as f:
        f.write(img_content)    # Write image

    return True # Download success

# Make directory
def makedir(url: str) -> None:
    gallery_dir = "galleries/"+url.split("/")[-3]

    # Make directory
    if os.path.isdir(gallery_dir) == False:
        os.makedirs(gallery_dir)

if __name__ == "__main__":
    # Argument parser
#    parser = argparser.ArgumentParser(description='Download image from e-hentai.org')
#
#    parser.add_argument('URL', help='Gallery Home URL') # URL
#
#    args = parser.parse_args()
#    
#    url = args.URL 

    #url = "https://e-hentai.org/g/1337256/eea0d94c8d/"
    #url = "https://e-hentai.org/g/1337390/150e69cdf4/"
    url = "https://e-hentai.org/g/1337447/601e8125b0/"

    homelist = list_home_page(url)    
    
    url_list = list()

    makedir(url)

    for i in homelist:
        url_list = list_viewpage_url(i)

        executor = ThreadPoolExecutor(max_workers=10)
        for url in url_list:
            executor.submit(download, url)

