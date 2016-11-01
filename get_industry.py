#!/usr/bin/env python
# encoding: utf-8


import utilities
import json
import re

#test_url = r"http://www.zhaopin.com/"
f = r'temp'
fr = open(f,'r+')
web_context = fr.read()
fr.close()

#web_context = utilities.get_html_content(test_url)
if web_context is not None:
    web_parse = utilities.bs_parse(web_context)

#city_list = web_parse.find('div',"city_nav_details show_nav_city").find_all('a')
industries =  web_parse.find('table','chebox').find_all('tr',attrs={"class":re.compile(r"zebraCol\d")})

json_context = []
for industry in industries:
    title = unicode(industry.find('td', 'leftClass industryLCla').string)
    subs = industry.find_all('label','noselItem')
    sub_titles = []
    for sub in subs:
        sub_titles.append(unicode(sub.find('input')['iname']))
    print '`````````````'
    print title
    print '`````````````'
    for t in sub_titles:
        print t
    json_context.append({'industry':title,'fields':sub_titles})


json_file = r'industry_list.json'
fp = open(json_file,'w+')
fp.write(json.dumps(json_context,skipkeys = True, encoding = 'utf-8'))
fp.close()
