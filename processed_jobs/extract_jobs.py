#!../bin/python3
import os
import json
import sys
import html
from html.parser import HTMLParser 
import html2text


help_str="""
How to use?
./read_json.py <path to json file>
"""

h=html.parser

json_file=sys.argv[1]
if not os.path.isfile(json_file):
    print (help_str)
    exit(1)


with open(json_file, "r") as file:
    myfile=json.load(file)
    if list == type(myfile):
        for job in myfile:
            if job:
                if job['match']:
                    print(f"Title : {job['title']} {job['llama']}")
                    print(f"Link : {job['applylink']}")

