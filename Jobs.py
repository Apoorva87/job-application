#!bin/python3
import requests
import json
import copy
import datetime as d
from bs4 import BeautifulSoup, Comment

class JobDetail(object):

    def __init__(self):
        self.job_detail = {}
        self.job_detail['title'] = ''
        self.job_detail['link'] = ''
        self.job_detail['applylink'] = ''
        self.job_detail['description'] = ''
        self.job_detail['id'] = ''
        self.job_detail['posted'] = ''
        self.job_detail['locations'] = ''
        self.job_detail['category'] = ''
        self.job_detail['applied'] = False
        self.job_detail['other'] = ''

    def __str__(self):
        return f"Title: {self.job_detail['title']}\
                Location: {self.job_detail['locations']}"

    def get_dict(self):
        return self.job_detail

    def add_detail(self, key, val):
        if key in self.job_detail.keys():
            self.job_detail[key] = val
        else:
            print(f"Looks like this /{key}/  is not standard job_detail")
            exit (1)

class Jobs(object):

    def __init__(self):
        self.job_list = []

    def get_job_list(self):
        return self.job_list

    def size(self):
        return len(self.job_list)

    def add_job(self, job : JobDetail):
        self.job_list.append(copy.copy(job))

    def add_job_list(self, job_list):
        for job in job_list:
            self.add_job(job)

    def save(self, name='default_joblist.json', exclude_list=[], do=False):
        if do:
            name = name[:-5] + '_'+str(d.date.today()) + '.json'
            filtered_data = [{k: v for k, v in job.get_dict().items() if k not in exclude_list} for job in self.job_list ]
            with open('scrapped_jobs/'+name, "w") as f: 
                #print (json.dumps(filtered_data, indent=2), file=f)
                json.dump(filtered_data, f, default=str, indent=2)
                #json.dumps(filtered_data, f, indent=2, default=str)



class WebPageParser(object):
    def __init__(self, name='default', link=None, timeout=60, debug=False, job_list=None):
        self.link = link
        self.timeout = timeout
        self.response = None
        self.soup = None
        self.good_resp = False
        if 'default' in name:
            self.name = self.__class__.__name__
        else:    
            self.name = name
        self.debug = debug
        self.jobs_list = Jobs()
        if job_list:
            self.jobs_list.add_job_list(job_list)

    def get_page(self):
        resp = requests.get(self.link, timeout=self.timeout)
        if self.debug:
            f = open(f"{self.name}_resp.txt",'+w')
            print (resp.text, file=f)
            f.close()
        if resp.status_code != 200:
            print ("Could not fetch page:")
            print (f"{self.link}")
            print (f"Error code {resp.status_code}")
        else:
            self.response = resp
            self.good_resp = True

    def parse_page(self):
        if self.good_resp:
            self.soup = BeautifulSoup(self.response.text, 'html.parser')
            if self.debug:
                f = open(f"{self.name}_soup.txt",'+w')
                print (self.soup, file=f)
                f.close()
       
    def get_jobs(self) -> Jobs:
        raise NotImplementedError()

    def process(self, save=False):
        print (f"DEBUG - Getting page..{self.name}\n{self.link}")
        self.get_page()
        print (f"DEBUG - Parsing page...")
        self.parse_page()
        print (f"DEBUG - Parsing page...")
        #import pdb; pdb.set_trace()
        if self.good_resp:
            jobs_list = self.get_jobs()
            self.jobs_list.add_job_list(jobs_list.get_job_list())
            num_jobs = self.jobs_list.size()
            print (f"DEBUG - Found {num_jobs} at this site")
        print (f"DEBUG - Saving saved jobs from {self.name}")
        if self.good_resp:
            self.save(save=save)

    def save(self, save=False):
        self.jobs_list.save(name=self.name+'_short.json', exclude_list=['description','category','other'], do=save)
        self.jobs_list.save(name=self.name+'_long.json', do=save)

