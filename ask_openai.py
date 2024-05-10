#!bin/python3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
print(webdriver.__path__)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import html
import UserInfo as u



"""
In a seperate browser run this command. Note the port
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9224 --user-data-dir="chromeProfile"

Now before running the script. Open ChatGPT and login. Bring it to text screen and leave

"""

chromedriver_path='./chromedriver-mac-arm64/chromedriver'
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Runs Chrome in headless mode (without GUI)
#chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.debugger_address = "127.0.0.1:9224"

service = Service(chromedriver_path)
#chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9224");
#import pdb; pdb.set_trace()
#driver = webdriver.Chrome(service)
driver = webdriver.Chrome(service=service, options=chrome_options)
print (driver.title)

wait = WebDriverWait(driver, 120)  # Wait for up to 10 seconds


#####################
# Helper functions
#####################

def workday_save_and_next(wait, frm="prev", to="next"):
    print (f"Clicking save and next. Going from -> {frm} to {to}")
    next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id='bottom-navigation-next-button']")))
    time.sleep(2)
    if next_button:
        next_button.click()
    else:
        print ("Next button not present..")
        import pdb; pdb.set_trace()

def workday_wait_till_pageload(wait):
    time.sleep(5)
    try:
        next_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id='bottom-navigation-next-button']")))
    except:
        print ("This page is not getting loaded")
        import pdb; pdb.set_trace()


#############################################
# Helper functions - CSS elements fill types
##############################################
def css_dropdown_text_select(q_str, text=""):
    #import pdb; pdb.set_trace()
    try:
        search_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, f"{q_str}")))
    except:
        print (f"Cannot find this search box - {q_str}")
        import pdb; pdb.set_trace()
    search_box.send_keys(text)
    search_box.click()
    search_box.click()


def css_dropdown_select(q_str, response):
    #import pdb; pdb.set_trace()
    # (By.XPATH, "//*[contains(@aria-label, 'search')]"
    print (q_str)
    time.sleep(2)
    try:
        q = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"{q_str}")))
        q.click()
    except:
        print (f"Cannot find dropdown select - {q_str}")
        import pdb; pdb.set_trace()
    try:
        driver.execute_script("arguments[0].scrollIntoView(true);", q) 
        wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{response}']"))).click()
    except:
        print (f"Cannot select from dropdown list - {response}")
        import pdb; pdb.set_trace()


def css_add_text_info(field, key):
    key=key.replace("\r",' ')
    key=key.replace("\t",'  ')
    key = html.escape(key)
    for one in key.split("\n"):
        try:
            q = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"textarea[id='{field}']")))
        except:
            import pdb; pdb.set_trace()
        if q.text:
            print (f"******Already text - {q.text}")
            return
        q.send_keys(one)
        #ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
        #ActionChains(driver).key_down(Keys.ENTER).perform()
        time.sleep(1)
        print(one)

def css_click_radio_box(q_str):
    time.sleep(4)
    try:
        cb = driver.find_element(By.CSS_SELECTOR, f"{q_str}")
    except:
        print ("Cannot find clickable element for radio box")
        import pdb; pdb.set_trace()

    try:
        #cb.click()
        driver.execute_script("arguments[0].scrollIntoView(true);", cb)
        driver.execute_script("arguments[0].click();", cb)
    except Exception as e:
        print (f"Cannot click on {q_str} : {e}")
        # Retry the click with ActionChains to simulate complex interaction
        action = ActionChains(driver)
        action.move_to_element(cb).click().perform()  # Simulate precise clicking
        import pdb; pdb.set_trace()
        #driver.execute_script("arguments[0].click();", cb)



def css_click_button(q_str):
    time.sleep(4)
    #import pdb; pdb.set_trace()
    #en = Keys.ENTER
    try:
        cb = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"{q_str}")))
    except:
        print(f"Cannot find button {q_str}")
        import pdb; pdb.set_trace()

    try:
        #cb.click()
        driver.execute_script("arguments[0].scrollIntoView(true);", cb)
        driver.execute_script("arguments[0].click();", cb)
    except:
        print(f"Cannot press button {q_str}")
        action = ActionChains(driver)
        action.move_to_element(cb).click().perform()  # Simulate precise clicking
        import pdb; pdb.set_trace()

        #add_work = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Add Work Experience']")))



#####################################################
#          My information
#####################################################
#workday_wait_till_pageload(wait)

def ask_a_gpt(q_str):
    time.sleep(2)

    css_add_text_info("prompt-textarea", f"{q_str}")

    css_click_button(q_str="button[data-testid='send-button']")
    time.sleep(2)

    cb = driver.find_elements(By.CSS_SELECTOR, f"div[data-message-author-role='assistant']")
    time.sleep(20)
    if cb:
        print (cb[-1].text)
   

q_str="Tell me joke today?"
ask_a_gpt(q_str)


exit(0)

