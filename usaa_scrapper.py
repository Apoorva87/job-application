#!bin/python3
import requests
import json
import datetime as d
from bs4 import BeautifulSoup
import html2text
import re

from Jobs import *


class USAAScrapper(WebPageParser):
    def __init__(self, name='', link=None, job_list=None, debug=False):
        super().__init__(name=self.__class__.__name__+name, link=link, job_list=job_list, debug=debug)

    #Process pages which only specify 1 jobs details
    def process_single_job(self, link=None) -> JobDetail:
        myclass_name=self.__class__.__name__

        class MySingleJob(WebPageParser):
            def __init__(self, link=None, debug=False):
                super().__init__(name=self.__class__.__name__ + myclass_name, link=link, debug=debug)

            def get_jobs(self) -> Jobs:
                jobs_list = Jobs()
                try:
                    data = json.loads(self.soup.find_all("script", type="application/ld+json")[0].text)
                except Exception as e:
                    #print(self.soup)
                    print(f"{e}")
                    try:
                        json_string = self.soup.find_all("script", type="application/ld+json")[0].text
                        cleaned_json_string = re.sub(r'[\x00-\x1F\x7F]', '', json_string)
                        cleaned_json_string = json_string.replace('\n', '\\n').replace('\t', '\\t')
                        data = json.loads(cleaned_json_string)
                    except Exception as e:
                        #print(self.soup)
                        print(f"{e}")
                        import pdb; pdb.set_trace()
                        exit (0)

                job_id = self.soup.find("div", class_="job-id job-info").dd.text
                try:
                    #apply_link = self.soup.find('a', class_='button job-apply btn-green top')['data-apply-url']
                    apply_link = self.soup.find('a', attrs={'data-apply-url': True})['data-apply-url']
                except:
                    apply_link=''
                    import pdb; pdb.set_trace()

                jd = JobDetail()
                jd.add_detail('posted', d.datetime.strptime(data['datePosted'],'%Y-%m-%d')) #needed
                #jd.add_detail('description', data['description'])
                try:
                    vh = html2text.html2text(data['description'])
                    jd.add_detail('description', vh) #needed
                except Exception as e:
                    jd.add_detail('description', data['description']) #needed
                jd.add_detail('id', job_id)
                jd.add_detail('applylink', apply_link)
                jd.add_detail('other', {'directApply':data['directApply']})

                jobs_list.add_job(jd)
                return jobs_list

        jc = MySingleJob(link=link, debug=self.debug)
        jc.process(save=False)
        return jc.jobs_list.get_job_list()[0] if len(jc.jobs_list.get_job_list()) > 0 else JobDetail()
                

    #Process top level pages that specify job_lists
    def get_jobs(self):
        jobs_container = self.soup.find('section',id="search-results-list").find_all('a')

        jobs_list = Jobs()
        num_jobs = len(jobs_container)
        #print (f"DEBUG - Top level get_jobs {num_jobs} at this site")
        for job in jobs_container:
            try:
                job_title       = job.h2.text
            except:
                job_title = ''
                full_link       = f"https://www.usaajobs.com/"+job['href']
                continue
                # </a>, <a aria-hidden="true" class="prev disabled" href="/search-jobs&amp;p=1" rel="nofollow">Prev</a>, <a class="next" href="/search-jobs&amp;p=2" rel="nofollow">Next</a>]
                import pdb; pdb.set_trace()
            full_link       = f"https://www.usaajobs.com/"+job['href']
            job_location    =  job.span.text.replace('|','').split('\xa0')
            job_id          = job['data-job-id']

            if 'teller' in job_title.lower() or \
            'assistant' in job_title.lower() or \
            'legal' in job_title.lower() or \
            'banker' in job_title.lower() or \
            'appraiser' in job_title.lower() or \
            'attorney' in job_title.lower() or \
            'spanish' in job_title.lower() or \
            'specialist' in job_title.lower() or \
            'consultant' in job_title.lower() or \
            'branch' in job_title.lower(): #skip all teller jobs
                continue

            jd = JobDetail()
            jd.add_detail('title', job_title)
            jd.add_detail('link', full_link)
            jd.add_detail('id', job_id) #needed
            jd.add_detail('locations', job_location)

            #jd.add_detail('description', job_desc) #needed
            #jd.add_detail('posted', job_post) #needed
            #jd.add_detail('category', job_category)
            #jd.add_detail('other', f"'externalApply':{job['externalApply']}")

            one_jd = self.process_single_job(link=full_link)
            #import pdb; pdb.set_trace()
            for k,v in one_jd.get_dict().items():
                if v != '':
                    jd.add_detail(k, v)
            #print(jd)

            jobs_list.add_job(jd)
        return jobs_list

j_list=None
#https://www.usaajobs.com/search-jobs?results&p=10
total_jobs = 0
for n in range(0,30):
    job_url=f'https://www.usaajobs.com/search-jobs?results&p={n}'
    #print(job_url)
    scp = USAAScrapper(link=job_url, job_list=j_list)
    scp.process(save=True)
    j_list = scp.jobs_list.get_job_list()
    if len(j_list) == total_jobs:
        print(f"Breaking at...{n}")
        break
    else:
        total_jobs = len(j_list)

