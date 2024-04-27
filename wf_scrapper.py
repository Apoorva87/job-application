#!/opt/anaconda3/bin/python3
import requests
from bs4 import BeautifulSoup

# URL of the Wells Fargo careers page (replace with the correct URL)

# Send a request to the page

for n in range(1,4):
    jobs_url = f"https://www.wellsfargojobs.com/en/jobs/?page={n}&country=United+States+of+America&region=Texas&team=Administrative+%26+Corporate+Services&team=Governance+%26+Controls&team=Operations&team=Product+Management&team=Research&team=Strategy+%26+Execution&team=Technology+%26+Data&type=Full+time&wtype=Regular&pagesize=50#results"  # Example, may not be correct
    response = requests.get(jobs_url, timeout=40)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the container or class that holds job listings
        #import pdb; pdb.set_trace()
        job_container = soup.find_all('div', class_='card card-job')  # Example class name
        #f = open('all_page.txt','+w')
        #f2 = open('all_resp_page.txt','+w')
        #print (soup, file=f)
        #print (response, file=f2)
        #f.close()
        #f2.close()

        # Create a list to store job details
        jobs = []

        # Loop through each job listing and extract information
        print ("FOund ", len(job_container))
        for job in job_container:
            job_title = job.find('h2', class_="card-title").find_all('a',class_='stretched-link',href=True)[0].text
            href_title = job.find('h2', class_="card-title").find_all('a',class_='stretched-link',href=True)[0]['href']
            full_link = "https://www.wellsfargojobs.com/"+str(href_title)
            #import pdb; pdb.set_trace()
            job_location    =  job.findAll('li', class_="list-inline-item")[0].text.replace('\n',' - ')
            job_description =  job.findAll('li', class_="list-inline-item")[1].text.replace('\n',' - ')

            # Add the job details to the list
            jobs.append({
                'title': job_title,
                'location': job_location.replace('\r',' - '),
                'link' : full_link,
                'description': job_description.replace('\r',' - ')
            })
            ##print (job_title)
        

        # Display the extracted job listings
        for job in jobs:
            print(f"Title: {job['title']}")
            print(f"Link: {job['link']}")
            print(f"Location: {job['location']}")
            print(f"Domain: {job['description']}")
            print ("--------------------------------")

        print ("Found ",len(jobs),f" jobs at WF in selected domains on page {n}. Good luck.")
    else:
        print("Failed to fetch the jobs page.")

