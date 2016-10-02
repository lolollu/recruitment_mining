#!/usr/bin/env python
# encoding: utf-8

import utilities
import json

test_url = r"http://company.zhaopin.com"

web_context = utilities.get_html_content(test_url)
if web_context is not None:
    web_parse = utilities.bs_parse(web_context)

city_list = web_parse.find('div',"city_nav_details show_nav_city").find_all('a')
city_cat_list = []
for city in city_list:
    print 'city: %s'%city.string
    print 'link: %s'%city['href']
    city_cat_list.append({u'city':unicode(city.string),u'href':unicode(city['href'])})

f = 'city_cat_list.json'
fp = open(f,'w+')
fp.write(json.dumps(city_cat_list,skipkeys = True, encoding = 'utf-8'))
