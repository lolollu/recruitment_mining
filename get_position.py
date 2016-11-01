#!/usr/bin/env python
# encoding: utf-8

import utilities
import time
import random


def all_positions(url):
    web_context = utilities.get_html_content(url)
    bs_parse = utilities.bs_parse(web_context)
    position_list = bs_parse.find('div', id='search_dom1').find_all('a')
    print len(position_list)
    position_set_list = []
    for position in position_list:
        field = unicode(position.string).strip()
        url = position['href']
        position_set_list.append({'field':field, 'url':url})

    return position_set_list

def sub_positions(position_set):
    position = position_set['field']
    url = position_set['url']
    web_context = utilities.get_html_content(url)
    bs_parse = utilities.bs_parse(web_context)

    sub_positions = bs_parse.find('div','subposition').find('div','sublist').find_all('a')
    sub_position_set_list = []
    for sub_position in sub_positions:
        sub_title = unicode(sub_position.string).strip()
        sub_position_set_list.append(sub_title)
    return {'field':position, 'sub_position':sub_position_set_list}


if __name__ == "__main__":
    random_span = [i*0.1 for i in range(1,30)]
    url = r'http://jobs.zhaopin.com/all/'
    position_set_list = all_positions(url)
    positions_list = []
    for field in position_set_list:
        time.sleep(random.choice(random_span))
        print field['field']
        sub_position_set = sub_positions(field)
        positions_list.append(sub_position_set)

    utilities.save_json(positions_list, r'position_list')

