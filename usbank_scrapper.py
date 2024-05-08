#!bin/python3
import requests
import json
import datetime as d
from bs4 import BeautifulSoup
import html2text

from Jobs import *


class USBankScrapper(WebPageParser):
    def __init__(self, name='', link=None, job_list=None):
        super().__init__(name=self.__class__.__name__+name, link=link, job_list=job_list, debug=True)

    #Process pages which only specify 1 jobs details
    def process_single_job(self, link=None) -> JobDetail:
        myclass_name=self.__class__.__name__

        class MySingleJob(WebPageParser):
            def __init__(self, link=None):
                super().__init__(name=self.__class__.__name__ + myclass_name, link=link)

            def get_jobs(self) -> Jobs:
                jobs_list = Jobs()
                
                data = [json.loads(x.string) for x in self.soup.find_all("script", type="application/ld+json")]
                apply_link = self.soup.find("a", {"id":'js-apply-external'}, href=True)['href']
                jd = JobDetail()
                try:
                    vh = html2text.html2text(data[0]['description'])
                    jd.add_detail('description', vh) #needed
                except Exception as e:
                    jd.add_detail('description', data[0]['description']) #needed
                jd.add_detail('id', data[0]['identifier']) #needed
                jd.add_detail('posted', d.date.fromisoformat(data[0]['datePosted'][0:10])) #needed
                jd.add_detail('applylink', apply_link)

                jobs_list.add_job(jd)
                return jobs_list

        jc = MySingleJob(link=link)
        jc.process(save=False)
        return jc.jobs_list.get_job_list()[0] if len(jc.jobs_list.get_job_list()) > 0 else JobDetail()
                

    #Process top level pages that specify job_lists
    def get_jobs(self):
        comment = self.soup.findAll('script')[0]
        import re
        import json
        m=re.search("phApp.ddo\s*=\s*(?P<mydict>.*);\s*phApp.experimentData", comment.text)
        mj=json.loads(m.group('mydict'))
        jobs_container = mj['eagerLoadRefineSearch']['data']['jobs']

        jobs_list = Jobs()
        num_jobs = len(jobs_container)
        #print (f"DEBUG - Top level get_jobs {num_jobs} at this site")
        for job in jobs_container:
            job_title = job['title']
            full_link = job['applyUrl']
            job_location    =  job['location']
            job_category =  job['multi_category']
            job_id = job['reqId']
            job_post = job['postedDate']
            job_desc = job['descriptionTeaser']

            if 'teller' in job_title.lower() or \
            'assistant' in job_title.lower() or \
            'legal' in job_title.lower() or \
            'banker' in job_title.lower() or \
            'spanish' in job_title.lower() or \
            'branch' in job_title.lower(): #skip all teller jobs
                continue

            jd = JobDetail()
            jd.add_detail('title', job_title)
            jd.add_detail('applylink', full_link)
            jd.add_detail('description', job_desc) #needed
            jd.add_detail('id', job_id) #needed
            jd.add_detail('posted', job_post) #needed
            jd.add_detail('locations', job_location)
            jd.add_detail('category', job_category)
            jd.add_detail('other', f"'externalApply':{job['externalApply']}")

            #one_jd = self.process_single_job(link=full_link)
            #import pdb; pdb.set_trace()
            #for k,v in one_jd.get_dict().items():
            #    if v != '':
            #        jd.add_detail(k, v)
            print(jd)

            jobs_list.add_job(jd)
        return jobs_list

j_list=None
for n in ['https://careers.usbank.com/global/en/c/banking-operations-jobs',
         'https://careers.usbank.com/global/en/c/corporate-functions-risk-jobs',
          'https://careers.usbank.com/global/en/c/credit-underwriting-lending-jobs',
          'https://careers.usbank.com/global/en/c/executive-jobs']:
    job_url=f"{n}"
    scp = USBankScrapper(link=job_url, job_list=j_list)
    scp.process(save=True)
    j_list = scp.jobs_list.get_job_list()
