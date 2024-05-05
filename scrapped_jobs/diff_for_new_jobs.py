#!../bin/python3
import os
import json
import sys
import html
from html.parser import HTMLParser 
import html2text


help_str="""
How to use?
./diff_for_new_jobs.py <old jobs json> <new jobs json>
"""

h=html.parser

json_file=sys.argv[1]
if not os.path.isfile(json_file):
    print (help_str)
    exit(1)

old_myfile=None
old_dict=dict()
with open(json_file, "r") as file:
    old_myfile=json.load(file)
    for j in old_myfile:
        old_dict[j['id']] = j

new_json_file=sys.argv[2]
if not os.path.isfile(new_json_file):
    print (help_str)
    exit(1)

new_myfile=None
new_dict=dict()
with open(new_json_file, "r") as file:
    new_myfile=json.load(file)
    for j in new_myfile:
        new_dict['id'] = j['id']
        if j['id'] not in old_dict.keys():
            print ("\n\n ** New Job found **")
            #print(f"{old_dict.keys()}")
            print (j)

