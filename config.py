#!/usr/bin/env python
# encoding: utf-8

class Filter_Info(object):
    def __init__(self):
        self.education_set = {u"不限":0,
                              u"高中/中专/中技":1,
                              u"大专":2,
                              u"本科/学士":3,
                              u"硕士/研究生":4,
                              u"博士":5,
                              u"其他":6,}

        self.experience_set = {u"不限":0,
                               u"无经验":1,
                               u"1年以下":2,
                               u"1-3年":3,
                               u"3-5年":4,
                               u"5-10年":5,
                               u"10年以上":6,}

        self.company_size_set = {u"20人以下":0,
                                 u"20-99人":1,
                                 u"100-499人":2,
                                 u"500-999人":3,
                                 u"1000-9999人":4,
                                 u"10000人以上":5,
                                 u"不限":6,}

        self.company_type_set = {u"不限":0,
                                 u"国企":1,
                                 u"外商独资":2,
                                 u"代表处":3,
                                 u"合资":4,
                                 u"民营":5,
                                 u"股份制企业":6,
                                 u"上市公司":7,
                                 u"国家机关":8,
                                 u"事业单位":9,
                                 u"其它":10,}

        self.occupation_set = {u"不限":0,
                               u"全职":1,
                               u"实习":2,
                               u"兼职":3,
                               u"其他":4,}

class Company(object):

    """Docstring for Company. """

    def __init__(self):
        self.company_name = ""
        self.company_url = ""
        self.company_type = None
        self.size = None
        self.industry = None
        self.address = ""
        self.logitude = 0.0
        self.latitude = 0.0
        self.website = ""
        self.info  = ""

class Job(object):
    def __init__(self):
        self.position = ""
        self.company_name = ""
        self.salary_min = 0
        self.salary_max = 0
        self.need_number = 0
        self.experience = ""
        self.location = ""
        self.occupation = ""
        self.education = ""
        self.title = ""
        #self.duty = ""
        #self.requirement = ""
        self.description = ""

