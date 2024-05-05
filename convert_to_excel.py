#!bin/python3
import os
import json
import sys
import html
from html.parser import HTMLParser 
import html2text
import pandas as pd

help_str="""
How to use?
./convert_to_excel.py <path to json file>
"""

h=html.parser

json_file=sys.argv[1]
if not os.path.isfile(json_file):
    print (help_str)
    exit(1)

excel_filename=sys.argv[1][:-5]+'.xlsx'
if len(sys.argv) > 2:
    excel_filename=sys.argv[2]+'.xlsx'
    print (excel_filename)
    

with open(json_file, "r") as file:
    json_data=json.load(file)
    df = pd.DataFrame(json_data)

    # Save the DataFrame to an Excel file
    df.to_excel(excel_filename, index=False)

