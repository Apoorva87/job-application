from openai import OpenAI
import openai
import json
import os
import sys
import regex
import glob
from datetime import datetime
import html2text

client = OpenAI()

MODEL = "gpt-4-turbo"
"""
All Hail OpenAi!
visit : https://ollama.com

Download/Install for macOS
We will be using this for 'llama3' (8B param model)
First time the script runs it will download the model locally.

 stream = ollama.chat(
            model='llama3',
            messages=[
                {'role': 'user', 'content': f"What is the color of sky"}
                ],
            stream=True,
        )
        for chunk in stream:
          print(chunk['message']['content'], end='', flush=True)


"""

"""
How to use ollama_process_jobs.py?

"""

file_path='USAAScrapper_long_2024-05-03.json'

file_path=sys.argv[1]
if sys.argv[2]:
    resume_file='resume/yatin_resume.txt'
else:
    resume_file=sys.argv[2]


print (f"Reading jobs file : {sys.argv[1]}")
print (f"Reading resume    : {resume_file}")


m=regex.search("([\w]+)_long_([0-9\-]+).json", file_path)
if m:
    print (f"Jobs at   : {m.group(1)}")
    print (f"From date : {m.group(2)}")
else:
    print ("Your command should be : ./<>.py  <*_long_*.json> <resume> ")
    exit(1)

resume_text=open(resume_file, 'r').read()

jobs_at=m.group(1)
date=m.group(2)

jobs_applied_file=f"./processed_jobs/{jobs_at}_processed.json"
applied_dict=[dict()]
if os.path.isfile(jobs_applied_file):
    print (f"Reading {jobs_applied_file}")
    with open(jobs_applied_file, "r") as file:
        applied_dict=json.load(file)

lookup_dict=dict()
for j in applied_dict:
    if 'id' not in j.keys():
        continue
    try:
        jid=j['id']
        if jid not in lookup_dict.keys():
            lookup_dict[jid] = j
    except:
        continue


with open(file_path, "r") as file:
    jobs=json.load(file)
    for j in jobs:
        full_answer=''
        try:
            jid=j['id']
        except:
            continue
        
        #"Associate|Engineer|Specialist|Developer|Accountant|Representative|Underwriter|Processor"
        if 'engineer' in j['title'].lower() or\
            'specialist' in j['title'].lower() or\
            'developer' in j['title'].lower() or\
            'representative' in j['title'].lower() or\
            'underwriter' in j['title'].lower() or\
            'processor' in j['title'].lower():
            continue

        if jid in lookup_dict.keys():
            if lookup_dict[jid]['match']:
                print (f"Skipping --- {j['id']} -- {j['title']}")
                continue

        try:
            j['description'] = html2text.html2text(j['description'])
        except Exception as e:
            print("Cannot convert description in non html",e)

        print (f"\n\nJob title : {j['title']}")
        stream = client.chat.completions.create(
        #stream = ollama.chat(
        #   model='llama3',
            model=MODEL,
            messages=[
                {'role': 'system', 'content': f"Compare job description to resume and find if it is a good match and if I should apply to this job"},
                {'role': 'user', 'content': f"Here is my resume {resume_text}"},
                {'role': 'user', 'content': f"Here are the details for job {j}"},
                #{'role': 'user', 'content': f"Score if the above job description is a good fit for my resume based on my previous and current experience, my skills, my education and location. Provide 2 bullets of what would be good skills for the job that is not on my resume. At the end provide a one line match score out of 100 strictly in a format 'match_score_is <score>'"},
                {'role': 'user', 'content': f"Based on my previous and current experience, career trajectory, my skills, my education, my location and the requirements of the job provide a one line match score strictly in format 'match_score_is <score out of 100>'. If applicable, provide two most relevant skills that would be beneficial for the job but are missing from my resume"},
                ],
            #stream=True,
        )
        #for chunk in stream:
        #  #print(chunk)
        #  if type(chunk) is dict:
        #    full_answer+=chunk['message']['content']
        #    #print(chunk['message']['content'], end='', flush=True)
        #print (full_answer)
        #print("not full ans")
        print(json.dumps(json.loads(stream.model_dump_json()), indent=4))
        full_answer=json.loads(stream.model_dump_json())
        ans_text=full_answer['choices'][0]['message']['content']
        m = regex.search("match_score_is\s*([0-9]+)", ans_text)
        match = False
        if m:
            if int(m.group(1)) > 70:
                print("MATCHING JOB")
                match = True
        else:
            print("** Did not find match string")
        applied_dict.append({ "title" : f"{j['title']}",
                              'llama' : f"{ans_text}", 
                             "match" : match,
                             "applylink" : f"{j['applylink']}",
                             "id" : f"{j['id']}",
                             "applied" : False,
                             "posted" : f"{j['posted']}"})
        #input('proceed?')


print (f"Writing {jobs_applied_file}")
out_file = open(jobs_applied_file, "w")
json.dump(applied_dict, out_file, indent = 4)
out_file.close()

