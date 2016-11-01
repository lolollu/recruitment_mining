#!/usr/bin/env python
# encoding: utf-8

import utilities
import config

class Basic_Parse():
    def __init__(self, url):
        self.url = url
        self.web_context = utilities.get_html_content(self.url)
        self.bs_parse = utilities.bs_parse(self.web_context)

class Company_List(Basic_Parse):
    def __init__(self,url):
        Basic_Parse.__init__(self,url)
        self.page_list = []
        self.next_page_url = ''

        self.get_list()
        self.get_next_url()

    def get_list(self):
        comp_list = self.bs_parse.find('div', 'result-jobs').find_all('div','fleft checkjobs width280')
        print len(comp_list)
        for company in comp_list:
            a = company.a
            company_name = unicode(a.string)
            company_href = a['href']
            #print company_name
            #print company_href
            #print '```````````'
            self.page_list.append((company_name,company_href))

    def get_next_url(self):
        root_url = r'http://company.zhaopin.com'
        next_page_url = self.bs_parse.find('a',title='下一页')['href']
        self.next_page_url = root_url+next_page_url
        #print self.next_page_url

class Company_Info(Basic_Parse):
    def __init__(self,url):
        Basic_Parse.__init__(self,url)
        self.company_info = config.Company()



if __name__=="__main__":
    companies_url= Company_List(r'http://company.zhaopin.com/changsha/')
    print companies_url.page_list
    print companies_url.next_page_url
