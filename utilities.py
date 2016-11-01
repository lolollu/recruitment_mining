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

def json_parse(file_name):
    """
    TODO: read the json file and return the parsed context
    """
    fr = open(file_name,'r+')
    city_level_json = json.loads(fr.read())
    fr.close()
    return city_level_json

def save_json(json_content,file_name):
    fw = open(file_name,'w+')
    fw.write(json.dumps(json_content,skipkeys = True, encoding = 'utf-8'))
    fw.close()


def lat_lng(address):
    """TODO: using baidu api to get the latitude and longitude number from verbal location
    :returns: a tuple of (lat,lng)

    """
    ak = r'yGm5sw8czxvx0e2idl1UbouoyD9bj0q3'
    api_url = r'http://api.map.baidu.com/geocoder/v2/?address={address}&output=json&ak={ak}&callback=showLocation'
    api_url = api_url.format(address = address, ak = ak)

    post_content = get_html_content(api_url)
    post_content = post_content.replace(r'showLocation&&showLocation(','')
    post_content = post_content[:-1]
    json_parse = json.loads(post_content)

    try:
        confidence = int(json_parse['result']['confidence'])
    except:
        confidence = 0

    if confidence >= 50:
        lng = json_parse['result']['location']['lng']
        lat = json_parse['result']['location']['lat']
    else:
        lng = None
        lat = None
    return (lat,lng)


if __name__ is "__main__":
    web_url = r'http://www.pythonscraping.com/pages/page1.html'
    html_text = get_html_content(web_url)
    if html_text is not None:
        # print html_text[:10]
        bs_obj = bs_parse(html_text)

        print bs_obj.html.h1.get_text()
