#!/usr/bin/env python
# encoding: utf-8

class Company(object):

    """Docstring for Company. """

    def __init__(self):
        self.company_name = ""
        self.company_url = ""
        self.company_type = ""
        self.size_min = 0
        self.size_max = 0
        self.industry = ""
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
        self.experience = ""
        self.location = ""
        self.occupation = ""
        self.education = ""
        self.title = ""
        self.duty = ""
        self.requirement = ""
