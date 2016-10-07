#!/usr/bin/env python
# encoding: utf-8

import utilities
import config
import re

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
        try:
            next_page_url = self.bs_parse.find('a',title='下一页')['href']
            self.next_page_url = root_url+next_page_url
        except:
            self.next_page_url = None

class Company_Info(Basic_Parse):
    def __init__(self,url):
        Basic_Parse.__init__(self,url)
        self.company_info = config.Company()
        self.job_list = self.get_job_list()

        self.get_information()

    def get_job_list(self):
        try:
            position_list_content = self.bs_parse.find('div', 'positionListContent').find_all('div', 'positionListContent1')
        except:
            position_list_content = None

        if position_list_content:
            position_list = []
            for position_content in position_list_content:
                position_name = unicode(position_content.find('span', 'jobName').a.string)
                position_url  = position_content.find('span', 'jobName').a['href']
                position_list.append({'job_name':position_name,'job_url':position_url})
        else:
            position_list = None

        return position_list


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
                table_set[unicode(table[i*2].string.replace('：','').strip())] =  unicode(table[i*2+1].string.strip())
            for key,content in table_set.items():
                print '{key} : {content}'.format(key=key,content=content)

            #convert table_set
            convert_set = {}
            try:
                #convert_set['company_type'] = table_set[u"公司性质"]
                company_type_set = config.Filter_Info().company_type_set
                company_type = table_set[u"公司性质"]
                company_type_code = "%02d"%company_type_set[company_type]
                convert_set['company_type'] = company_type_code
            except:
                convert_set['company_type'] = None

            try:
                #convert_set['company_size'] = table_set[u"公司规模"]
                company_size_set = config.Filter_Info().company_size_set
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
                        for j in range(len(fields)):
                            if company_industry == fields[j]:
                                industry_code = "%03d%03d"%(i,j)
                                print industry_code
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
        try:
            map_content = self.bs_parse.find('table', 'comTinyDes').find_all('td')[-1].button['onclick']
        except:
            map_content = None

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
            temp_content = ""
            intro = self.bs_parse.find('div', 'company-content').find_all(string = True)
            for i in intro:
                temp_content += i.strip().replace(' ','')
            merge_content = temp_content.split('。')
            if len(merge_content) >= 3:
                for i in range(3):
                    intro_content += merge_content[i]+"。"
                return intro_content
            else:
                return temp_content
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

        self.company_info.company_type = company_table['company_type']
        self.company_info.size = company_table['company_size']
        self.company_info.industry = company_table['company_industry']
        self.company_info.address = company_table['company_address']
        self.company_info.website = company_table['company_website']

        #get lat&lng
        self.company_info.latitude, self.company_info.logitude = self.get_latlng()

        #get company introduction
        self.company_info.info= self.get_intro()

class Job_Info(Basic_Parse):
    def __init__(self,url):
        Basic_Parse.__init__(self, url)
        self.job_info = config.Job()

        self.get_information()

    def analyse_table(self,table_content):
        item_set = {}
        for item in table_content:
            key = unicode(item.find('span').string).strip("：")
            value = u""
            for i in item.find('strong').find_all(string = True):
                value += unicode(i.string).strip()
            item_set[key] = value

        #for key,value in item_set.items():
        #    print '{} : {}'.format(key, value)

        #parse items
        job_table = {}
        fielter_info = config.Filter_Info()
        try:
            salary = item_set[u"职位月薪"]
            salary = re.findall(r'\d+',salary)
            if len(salary) == 2:
                job_table['salary_min'] = int(salary[0])
                job_table['salary_max'] = int(salary[1])
            elif len(salary) == 1:
                job_table['salary_min'] = 0
                job_table['salary_max'] = int(salary[0])
            else:
                job_table['salary_min']=job_table['salary_max'] = None
        except:
            job_table['salary_min']=job_table['salary_max'] = None

        try:
            experience_set = fielter_info.experience_set
            experience = item_set[u"工作经验"]
            job_table['experience'] = experience_set[experience]
        except:
            job_table['experience'] = None

        try:
            need_number = item_set[u"招聘人数"]
            need_number = re.findall(r'\d+', need_number)
            if len(need_number) <= 2:
                job_table['need_number'] = int(need_number[-1])
            else:
                job_table['need_number'] = None
        except:
            job_table['need_number'] = None

        try:
            job_table['location'] = item_set[u"工作地点"]
        except:
            job_table['location'] = None

        try:
            occupation_set = fielter_info.occupation_set
            occupation = item_set[u"工作性质"]
            occupation_code = occupation_set[occupation]
            job_table['occupation'] = occupation_code
        except:
            job_table['occupation'] = None

        try:
            education_set = fielter_info.education_set
            education = item_set[u"最低学历"]
            for key, value in education_set.items():
                if education in key or education == key:
                    job_table['education'] = value
                    break
        except:
            job_table['education'] = None

        try:
            title_list = utilities.json_parse(r'position_list.json')
            temp_title = item_set[u"职位类别"].split("/")
            title = ""
            if len(temp_title) == 1:
                title = unicode(temp_title[0])
            else:
                for i in temp_title:
                    if len(title)< len(i):
                        title = unicode(i)

            print "*%s*"%title

            for i in range(len(title_list)):
                titles = title_list[i]['sub_position']
                job_table['title'] = None
                for j in range(len(titles)):
                    if len(temp_title) == 1:
                        if title == titles[j]:
                            title_code = "%03d%03d"%(i,j)
                            #print title_code
                            job_table['title'] = str(title_code)
                            i = -1
                            break

                    else:
                        if title in titles[j]:
                            title_code = "%03d%03d"%(i,j)
                            #print title_code
                            job_table['title'] = str(title_code)
                            i = -1
                            break
                if i <  0:
                    break
        except:
            job_table['title'] = None

        return job_table

    def parse_description(self, description_content):
        content = ''
        for line in description_content:
            content += unicode(line.string).strip()
        re_pattern = re.compile(r'SWSStringCutStart(.+?)SWSStringCutEnd')
        content = re.findall(re_pattern, content)
        if content is not []:
            content = content[0]
            if len(content) == 0 :
                return None
            elif len(content) > 500:
                return content[:500]
            else:
                return content
        else:
            return None


    def show_info(self):
        print 'position : {}'.format(self.job_info.position)
        print 'company_name : {}'.format(self.job_info.company_name)
        print 'min salary : {}'.format(self.job_info.salary_min)
        print 'max salary : {}'.format(self.job_info.salary_max)
        print 'experience : {}'.format(self.job_info.experience)
        print 'need_number : {}'.format(self.job_info.need_number)
        print 'location : {}'.format(self.job_info.location)
        print 'occupation : {}'.format(self.job_info.occupation)
        print 'education : {}'.format(self.job_info.education)
        print 'title : {}'.format(self.job_info.title)
        #print 'duty : {}'.format(self.job_info.duty)
        #print 'requirement : {}'.format(self.job_info.requirement)
        print 'description : {}'.format(self.job_info.description)


    def get_information(self):
        try:
            head = self.bs_parse.find('div', 'inner-left fl')
            try:
                h1 = head.h1.string
            except:
                h1 = None
            if h1:
                self.job_info.position = unicode(h1).strip()
            else:
                self.job_info = None
            try:
                h2 = head.h2.a.string
            except:
                h2 = None
            if h2:
                self.job_info.company_name = unicode(h2).strip()
            else:
                self.job_info.company_name = None
        except:
            self.job_info.position = self.job_info.company_name = None


        #get information details from table
        try:
            table_content = self.bs_parse.find('ul','terminal-ul clearfix').find_all('li')
            #print "table_content: %d"%len(table_content)
        except:
            print "Cannot find the job table."
            table_content = None
        if table_content:
            job_table = self.analyse_table(table_content)
        else:
            job_table = None

        if job_table:
            self.job_info.salary_min = job_table['salary_min']
            self.job_info.salary_max = job_table['salary_max']
            self.job_info.need_number = job_table['need_number']
            self.job_info.experience = job_table['experience']
            self.job_info.location = job_table['location']
            self.job_info.occupation = job_table['occupation']
            self.job_info.education = job_table['education']
            self.job_info.title = job_table['title']

        #get job description
        try:
            description_content = self.bs_parse.find('div', 'tab-inner-cont').find_all(string = True)
        except:
            description_content = None

        if description_content:
            job_description = self.parse_description(description_content)
        else:
            job_description = None

        if job_description:
            self.job_info.description = job_description



if __name__=="__main__":
    #    companies_url= Company_List(r'http://company.zhaopin.com/changsha/')
    #    print companies_url.page_list
    #    print companies_url.next_page_url
    #    company_info = Company_Info(r'http://company.zhaopin.com/CC430331122.htm')
    #    company_info.show_info()

    job_url = r'http://jobs.zhaopin.com/120019970287649.htm'
    job_info = Job_Info(job_url)
    job_info.show_info()
