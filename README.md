Job Application

- Scrapper for job portals
- Simple form filling template for some websites


How to work here:
1. Make sure you have python virtualenv installed
pip install virtualenv

2. [skip] python3 -m venv <name of virtual env>

3. Activate python virtual env
source bin/activate

4. Install dependent libraries 
pip install -r requirements.txt
pip install --upgrade selenium
pip install --upgrade chromedriver
unzip chromedriver-mac-arm64.zip

5. [skip for now] Deactivate venv
deactivate

6. Download Ollama for running LLM 


Git Shenanigans:
- Have github.com (free) account
- Create PAT from git -> settings -> Developer settings (make sure you give full repo access)
- username : apoorva87
- Password : use PAT
This is needed for push

File Permissions:
chmod +x+u chrome_driver_test.py 

BUGS in Selenium 4.1.0
1. file upload command wrong
Locate this file on your mac - 
/Users/qatester/Library/Python/3.9/lib/python/site-packages/selenium/webdriver/remote/remote_connection.py
(USE - python3 -c  "from selenium import webdriver; print (webdriver.__path__)")
(then use - /Users/qatester/yatin_career/job-application/lib/python3.9/site-packages/selenium/webdriver/remote/remote_connection.py)

make the change as:
  Command.UPLOAD_FILE: ("POST", "/session/$sessionId/se/file"),
to:
  Command.UPLOAD_FILE: ("POST", "/session/$sessionId/file"),

