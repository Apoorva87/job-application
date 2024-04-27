#!bin/python3
import requests
import json
import datetime as d
from bs4 import BeautifulSoup

from Jobs import *


class WFScrapper(WebPageParser):
    def __init__(self, name='', link=None, job_list=None):
        super().__init__(name=self.__class__.__name__+name, link=link, job_list=job_list)

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
        jobs_container = self.soup.find_all('div', class_='card card-job')
        jobs_list = Jobs()
        num_jobs = len(jobs_container)
        print (f"DEBUG - Top level get_jobs {num_jobs} at this site")
        for job in jobs_container:
            job_title = job.find('h2', class_="card-title").find_all('a',class_='stretched-link',href=True)[0].text
            href_title = job.find('h2', class_="card-title").find_all('a',class_='stretched-link',href=True)[0]['href']
            full_link = "https://www.wellsfargojobs.com/"+str(href_title)
            job_location    =  job.findAll('li', class_="list-inline-item")[0].text.replace('\n',' - ')
            job_category =  job.findAll('li', class_="list-inline-item")[1].text.replace('\n',' - ')

            jd = JobDetail()
            jd.add_detail('title', job_title)
            jd.add_detail('link', full_link)
            jd.add_detail('description', '') #needed
            jd.add_detail('id', '') #needed
            jd.add_detail('posted', '') #needed
            jd.add_detail('locations', job_location)
            jd.add_detail('category', job_category)

            one_jd = self.process_single_job(link=full_link)
            #import pdb; pdb.set_trace()
            for k,v in one_jd.get_dict().items():
                if v != '':
                    jd.add_detail(k, v)

            jobs_list.add_job(jd)
        return jobs_list

j_list=None
for n in range(1,4):
    jobs_url = f"https://www.wellsfargojobs.com/en/jobs/?page={n}&country=United+States+of+America&region=Texas&team=Administrative+%26+Corporate+Services&team=Governance+%26+Controls&team=Operations&team=Product+Management&team=Research&team=Strategy+%26+Execution&team=Technology+%26+Data&type=Full+time&wtype=Regular&pagesize=50#results"  # Example, may not be correct
    scp = WFScrapper(link=jobs_url, job_list=j_list)
    scp.process(save=True)
    j_list = scp.jobs_list.get_job_list()
