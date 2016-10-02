#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup
import urllib2
from urllib2 import HTTPError, URLError

import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_html_content(url):
    if url == '' or url == None:
        return None
    else:
        try:
            request = urllib2.Request(url)
            html_obj = urllib2.urlopen(request)
        except HtmlError as e:
            print "Cannont find the Html: %s" %url
            print e
            return None
        except UrlError as e:
            print "UrlError"
            print e
            return None
        finally:
            return html_obj.read()

def bs_parse(html_text):
    if html_text == '' or html_text == None:
        return None
    else:
        try:
            bs_obj = BeautifulSoup(html_text, 'html.parser')
        except:
            print 'The BeautifulSoup Parse encounter some problem!'
            return None
        return bs_obj

def city_url(city_key):
    """TODO: get the city url from city key, the key is from city_level.json
             if it is in city_cat_list.json
    :returns: the city url

    """
    f = r'city_cat_list.json'
    ft = open(f,'r+')
    city_cat_json_list = json.loads(ft.read())
    ft.close()
    for city in city_cat_json_list:
        #print city_key
        #print city['city']
        if unicode(city_key) ==  city['city']:
            return city['href']
    return None

def city_list():
    """
    TODO: get the city_list and level from city_level.json
    :returns: a list which contains city level and list of cities of this level.

    """
    f = r'city_level.json'
    fr = open(f,'r+')
    city_level_json = json.loads(fr.read())
    fr.close()
    return city_level_json

if __name__ is "__main__":
    web_url = r'http://www.pythonscraping.com/pages/page1.html'
    html_text = get_html_content(web_url)
    if html_text is not None:
        # print html_text[:10]
        bs_obj = bs_parse(html_text)

        print bs_obj.html.h1.get_text()
