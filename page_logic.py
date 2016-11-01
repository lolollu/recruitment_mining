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
        self.get_information()

    def analyse_table(self,table):
        table_set = {}
        print len(table)
        if len(table)%2:
            print 'The comapny table is invaliable.'
            return None
        else:
            #init table set
            table_set = {}
            for i in range(len(table)/2):
                table_set[unicode(table[i*2].string.replace('：','').strip())] = unicode(table[i*2+1].string.strip())

            #convert table_set
            convert_set = {}
            try:
                #convert_set['company_type'] = table_set[u"公司性质"]
                company_type_set = config.Filter_Info.comapny_type_set
                company_type = table_set[u"公司性质"]
                company_type_code = "%02d"%company_type_set[company_type]
                convert_set['company_type'] = company_type_code
            except:
                convert_set['company_type'] = None

            try:
                #convert_set['company_size'] = table_set[u"公司规模"]
                company_size_set = config.Filter_Info.company_size_set
                company_size = table_set[u"公司规模"]
                company_size_code = "%02d"%company_size_set[company_size]
                convert_set['company_size'] = company_size_code
            except:
                convert_set['company_size'] = None

            try:
                convert_set['company_website'] = table_set[u"公司网站"]
                if convert_set['company_website'] == '':
                    convert_set['company_website'] = None
            except:
                convert_set['company_website'] = None

            try:
                convert_set['company_industry'] = []
                company_industry_list = table_set[u"公司行业"].split(",")
                industry_field_set = utilities.json_parse(r'industry_list.json')
                for company_industry in company_industry_list:
                    for i in range(len(industry_field_set)):
                        fields = industry_field_set[i]["fields"]
                        for j in range(len('fields')):
                            if unicode(company_industry) == fields[j]:
                                industry_code = "%03d%03d"%(i,j)
                                convert_set['company_industry'].append(industry_code)
                if convert_set['company_industry'] == []:
                    convert_set['company_industry']= None
            except:
                convert_set['company_industry'] = None

            try:
                convert_set['company_address'] = table_set[u"公司地址"]
                if convert_set['company_address'] == '':
                    convert_set['company_address'] = None
            except:
                convert_set['company_address'] = None

            return convert_set

    def get_latlng(self):
        map_content = self.bs_parse.find('table', 'comtinyDes').find_all('td')[-1].button['onclick']
        if map_content:
            map_content = map_content.replace('fnOpenMiniMap(','').replace(');','')
            print map_content
            info_list = map_content.split(', ')
            lat = info_list[-2].replace('\'','')
            lng = info_list[-1].replace('\'','')
            return (lat,lng)
        else:
            return utilities.lat_lng(self.company_info.address)

    def get_intro(self):
        intro_content = ""
        try:
            intro = self.bs_parse.find('div', 'comapny-content').find_all(string = True)
            for i in intro:
                intro_content += i
            if len(intro_content) >= 300:
                return unicode(intro_content[:300])
            else:
                return unicode(intro_content)
        except:
            return None


    def show_info(self):
        print 'name: {}'.format(self.company_info.company_name)
        print 'url: {}'.format(self.company_info.company_url)
        print 'type: {}'.format(self.company_info.company_type)
        print 'size: {}'.format(self.company_info.size)
        print 'industry&field: {}'.format(self.company_info.industry)
        print 'address: {}'.format(self.company_info.address)
        print 'lat&lng: {lat},{lng}'.format(lat = self.company_info.latitude, lng = self.company_info.logitude)
        print 'website: {}'.format(self.company_info.website)
        print 'info: '
        print self.company_info.info



    def get_information(self):
        main_content = self.bs_parse.find('div', 'mainLeft')
        self.company_info.company_name = unicode(main_content.find('h1').string).strip()

        print 'process %s company.'%self.company_info.company_name
        self.company_info.company_url = self.url

        company_table = main_content.find('table', 'comTinyDes').find_all('span')
        company_table = self.analyse_table(company_table)
        print company_table

        self.company_info.company_type = company_table['company_type']
        self.company_info.size = company_table['company_size']
        self.company_info.industry = company_table['company_industry']
        self.company_info.address = company_table['company_address']
        self.company_info.website = company_table['company_website']

        #get lat&lng
        self.company_info.latitude, self.company_info.logitude = self.get_latlng()

        #get company introduction
        self.company_info.info= self.get_intro()



if __name__=="__main__":
#    companies_url= Company_List(r'http://company.zhaopin.com/changsha/')
#    print companies_url.page_list
#    print companies_url.next_page_url
    company_info = Company_Info(r'http://company.zhaopin.com/CC466748528.htm')
    company_info.show_info()






