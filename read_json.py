#!bin/python3
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
        for entry in myfile:
            for k,v in entry.items():
                try:
                    vh = html2text.html2text(v)
                    print(f"{k} : {vh}")
                except Exception as e:
                    print (f"Exception : ",e)
                    print(f"{k} : {v}")
            print("-------next list elem--------")
    if dict == type(myfile):
        for k,v in myfile.items():
            print(f"{k} : {v}")
        print("------dict---------")

