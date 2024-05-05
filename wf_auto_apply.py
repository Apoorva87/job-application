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

##driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
#driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
#driver.get('http://www.google.com/');
#time.sleep(5) # Let the user actually see something!
#search_box = driver.find_element_by_name('q')
#search_box.send_keys('ChromeDriver')
#search_box.submit()
#time.sleep(5) # Let the user actually see something!
#driver.quit()

chromedriver_path='./chromedriver-mac-arm64/chromedriver'
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Runs Chrome in headless mode (without GUI)
chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--disable-dev-shm-usage")


service = Service(chromedriver_path)
service.start()
driver = webdriver.Remote(service.service_url, options=chrome_options)

#driver.get('http://www.google.com/');
# https://wd1.myworkdaysite.com/en-US/recruiting/wf/WellsFargoJobs/job/BEE-CAVE%2C-TX/Senior-Premier-Banker---BEE-CAVE---GALLERIA---Bee-Cave--TX_R-364228/apply/useMyLastApplication
#url='https://wd1.myworkdaysite.com/recruiting/wf/WellsFargoJobs/job/BEE-CAVE-TX/Senior-Premier-Banker---BEE-CAVE---GALLERIA---Bee-Cave--TX_R-364228'
#login_url='https://wd1.myworkdaysite.com/en-US/recruiting/wf/WellsFargoJobs/login?redirect=%2Fen-US%2Frecruiting%2Fwf%2FWellsFargoJobs%2Fjob%2FBEE-CAVE%252C-TX%2FSenior-Premier-Banker---BEE-CAVE---GALLERIA---Bee-Cave--TX_R-364228%2Fapply%2FuseMyLastApplication'
login_url='https://wd1.myworkdaysite.com/en-US/recruiting/wf/WellsFargoJobs/login?redirect=%2Fen-US%2Frecruiting%2Fwf%2FWellsFargoJobs%2Fjob%2FCHARLOTTE%252C-NC%2FSenior-Auditor---Operations_R-357413%2Fapply%2FuseMyLastApplication'
driver.get(login_url)

wait = WebDriverWait(driver, 120)  # Wait for up to 10 seconds
# Wait for a specific element to be visible
#username = wait.until(EC.visibility_of_element_located((By.ID, "input-4")))
#username.send_keys("yatin.karnik@gmail.com")
#password = wait.until(EC.visibility_of_element_located((By.ID, "input-5")))
#password.send_keys("JobHunt2024*")

##################
# LOGIN PAGE
##################
# Fill in the email field
email_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-automation-id='email']")))
email_field.send_keys(u.email)
# Fill in the password field
password_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-automation-id='password']")))
password_field.send_keys(u.password)
# Handle overlays or click interceptors
time.sleep(2)
overlay = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id='click_filter']")))
overlay.click()

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


def css_add_text_info(under_div, field, key):
    key=key.replace("\r",' ')
    key=key.replace("\t",'  ')
    key = html.escape(key)
    for one in key.split("\n"):
        try:
            q = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"div[data-automation-id='{under_div}'] {field}")))
        except:
            import pdb; pdb.set_trace()
        if q.text:
            print (f"******Already text - {q.text}")
            return
        q.send_keys(one)
        ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
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
workday_wait_till_pageload(wait)

print("Working on My Information...")
search_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-uxi-widget-type='selectinput']")))
if search_box:
    search_box.send_keys("Wells Fargo Employee Referral")
    search_box.click()
else:
    print ("Cannot find referral box")


workday_save_and_next(wait, frm="[My information]", to="[My experience]")
########################################
#           My experience
########################################
workday_wait_till_pageload(wait)

skip_edu = False
def drive_all_experience(wait):
    print ("Drive experience")
    try:
        b = driver.find_element(By.CSS_SELECTOR, "div[data-automation-id='workExperienceSection'] button[aria-label='Add Work Experience']")
    except:
        print ("Cannot find Add Work Exp button. skipping edu")
        skip_edu=True

    if skip_edu:
        print ("**Cannot find Add Work Exp button. skipping edu")
        return skip_edu

    css_click_button(q_str="div[data-automation-id='workExperienceSection'] button[aria-label='Add Work Experience']")

    for i,job in enumerate(u.jobs):
        num=i+1
        if (num > 1):
            css_click_button(q_str="div[data-automation-id='workExperienceSection'] button[data-automation-id='Add Another']")
            time.sleep(2)
        css_add_text_info(f'workExperience-{num}', "input[data-automation-id='jobTitle']", job['title'])
        css_add_text_info(f'workExperience-{num}', "input[data-automation-id='company']",  job['company'])
        css_add_text_info(f'workExperience-{num}', "input[data-automation-id='location']", job['location'])
        if job['current']:
            q_str=f"div[data-automation-id='workExperience-{num}'] input[data-automation-id='currentlyWorkHere']"
            css_click_radio_box(q_str)
        else:
            css_add_text_info(f'workExperience-{num}', "div[data-automation-id='formField-endDate'] input[data-automation-id='dateSectionMonth-input']", job['end'])
        css_add_text_info(f'workExperience-{num}', "div[data-automation-id='formField-startDate'] input[data-automation-id='dateSectionMonth-input']", job['from'])
        css_add_text_info(f'workExperience-{num}', "textarea[data-automation-id='description']", job['description'])
        print (f"******* Job {num} done *****")

#comment this if this doesnt need to be driven
skip_edu = drive_all_experience(wait)

def drive_all_education(wait):
    print ("Drive education")
    css_click_button(q_str="div[data-automation-id='educationSection'] button[aria-label='Add Education']")

    for i,edu in enumerate(u.education):
        num=i+1
        if (num > 1):
            css_click_button(q_str="div[data-automation-id='educationSection'] button[data-automation-id='Add Another']")
            time.sleep(2)
        css_add_text_info(f'education-{num}', "input[data-automation-id='school']", edu['school'])
        css_dropdown_select(q_str=f"div[data-automation-id='education-{num}'] button[data-automation-id='degree']", response=edu['degree'])
        css_dropdown_text_select(q_str=f"div[data-automation-id='education-{num}'] input[data-uxi-widget-type='selectinput']", text=edu['field'])
        css_add_text_info(f'education-{num}', "input[data-automation-id='gpa']", edu['gpa'])
        css_add_text_info(f'education-{num}', "div[data-automation-id='formField-startDate'] input[data-automation-id='dateSectionYear-input']", edu['from'])
        css_add_text_info(f'education-{num}', "div[data-automation-id='formField-endDate'] input[data-automation-id='dateSectionYear-input']", edu['end'])
        print (f"******* Education {num} done *****")

#comment this if this doesnt need to be driven
if not skip_edu:
    drive_all_education(wait)

#Resume section
if not skip_edu:
    import os
    full_resume_path=os.path.abspath(u.resume["pm"])
    try:
        q = driver.find_element(By.CSS_SELECTOR, f"div[data-automation-id='resumeSection'] input[type='file']")
        driver.execute_script("arguments[0].scrollIntoView(true);", q)
    except:
        print ("cannot find file upload")
        import pdb; pdb.set_trace()
    try:
        q.send_keys(full_resume_path)
    except:
        print ("cannot upload")
        import pdb; pdb.set_trace()

time.sleep(4)

workday_save_and_next(wait, frm="[My experience]", to="[Application Questions]")
####################################################################
#                     My Application
####################################################################
workday_wait_till_pageload(wait)
print ("Next screen..moving to Application Questions....")
time.sleep(5)

skip_ques=False
try:
    found = driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Are you a current or former Wells Fargo employee? Yes')]")
    print("Skipping questions")
    skip_ques=True
except Exception as e:
    print("Skipping questions NOT ",e)
    skip_ques=False

if not skip_ques:
    q1_str="button[aria-label='Are you a current or former Wells Fargo employee? select one required']"
    css_dropdown_select(q_str=q1_str, response="Yes, former employee")

    time.sleep(5)
    css_add_text_info(f'primaryQuestionnairePage', "textarea[data-automation-id='fbfd9c6b32531015123e4853743e0001']", u.social_last_four)

    q2_str="button[aria-label='Are you 18 years of age or older? select one required']"
    css_dropdown_select(q_str=q2_str, response="Yes")

    q3_str="button[aria-label='Will you now or in the future require sponsorship for employment visa to work in the country you are applying to work in? For the US, this includes sponsorship of H-1B, TN, or E-3 visas. Persons currently on F-1 visas completing curricular or optional practical training should answer yes. select one required'"
    css_dropdown_select(q_str=q3_str, response="No")


    q4_str="button[aria-label='Have you ever been involuntarily discharged or asked to resign from a position? Your response should not include discharges due to layoff, displacement, or reorganization. select one required'"
    css_dropdown_select(q_str=q4_str, response="No")

    q5_str="button[aria-label='Have you ever been disciplined by an administrative agency or the subject of an administrative order relating to conduct or practices involving any aspect of the financial services, insurance, securities, or real estate industries or any other licensed industry profession? An Administrative agency is a government body authorized to implement legislative directives by developing more precise and technical rules. select one required'"
    css_dropdown_select(q_str=q5_str, response="No")

    q6_str="button[aria-label='Do you have any non-compete/non-solicitation or other agreements that prevents or restricts you from performing the job for which you are applying for? select one required'"
    css_dropdown_select(q_str=q6_str, response="No")

    q7_str="button[aria-label='Do you have any fiduciary appointments (such as an executor, personal representative, administrator, guardian, trustee, or any similar fiduciary designation) that involve a current Wells Fargo customer, or someone you know that intends to become a Wells Fargo customer (for example, a current client)? select one required'"
    css_dropdown_select(q_str=q7_str, response="No")

    q8_str="button[aria-label='Are you currently a member of, or do you currently serve in any capacity on, a Board of Directors, Advisory Board, Committee, Trustee Board, or have any other similar position with any for-profit or non-profit organization? select one required'"
    css_dropdown_select(q_str=q8_str, response="No")


    q9_str="button[aria-label='Do you currently have, or plan to have, any employment or other work that you intend to continue if you accept a job at Wells Fargo? Including, but not limited to, an independent contractor, consultant, real estate agent, home inspector, appraiser, tax preparer, seasonal or part-time employee. select one required'"
    css_dropdown_select(q_str=q9_str, response="No")

    q10_str="button[aria-label='Do you currently have 25% or more (10% or more if seeking a Wells Fargo Executive Officer role) ownership interest in, or plan to have such an ownership interest in any for-profit business entity or activity? Including an inactive business, business entities formed for the purpose of business holdings, investments, or future business activities; sole proprietorships; or non-registered business entities or activities. select one required'"
    css_dropdown_select(q_str=q10_str, response="No")

    q11_str="button[aria-label='Do you currently serve, service, or plan to serve in any position of control with a for-profit business entity or activity? select one required'"
    css_dropdown_select(q_str=q11_str, response="No")

    q12_str="button[aria-label='Are you currently serving as, or planning to serve as, an elected or appointed official or as a member, director, officer, or employee of a government entity or governmental or public agency, authority, advisory board, city council, school board, political party committee, or other similar board or entity? select one required'"
    css_dropdown_select(q_str=q12_str, response="No")

    q13_str="button[aria-label='Do you have a family relationship (biological, adopted, marriage, domestic partnership, civil union, or some other arrangement), or are you a close personal contact (a regular and ongoing close connection that may be personal, romantic, or financial) of any employees, contingent resources, or board members of Wells Fargo or its subsidiaries? select one required'"
    css_dropdown_select(q_str=q13_str, response="Yes")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "textarea[data-automation-id='fbfd9c6b32531015123e4abc2b620006']").send_keys('Swati Karnik. Wife. Dallas, Texas')

    q14_str="button[aria-label='Do you currently work, or have you worked for KPMG (Klynveld Peat Marwick Goerdeler - the bank’s auditor) during the past five years? select one required'"
    css_dropdown_select(q_str=q14_str, response="No")

    q15_str="button[aria-label='Are you a current or former military spouse or domestic partner? select one required'"
    css_dropdown_select(q_str=q15_str, response="No")

    q16_str="button[aria-label='Are you a Senior Government Official or have you served as one in the past two years? select one required'"
    css_dropdown_select(q_str=q16_str, response="No")

    q17_str="button[aria-label='Did a Senior Government Official refer you for this position? select one required'"
    css_dropdown_select(q_str=q17_str, response="No")

    q18_str="button[aria-label='Do you have a family relationship (biological, adopted, marriage, domestic partnership, civil union, or some other arrangement) with, or are you a close personal contact (a regular and ongoing close connection that may be personal, romantic, or financial) of a Senior Government Official? select one required'"
    css_dropdown_select(q_str=q18_str, response="No")

    q19_str="button[aria-label='Did a Senior Executive of a customer, potential customer or third-party vendor of Wells Fargo refer you for this position? select one required'"
    css_dropdown_select(q_str=q19_str, response="No")

    q20_str="button[aria-label='Do you have a family relationship (biological, adopted, marriage, domestic partnership, civil union, or some other arrangement) with, or are you a close personal contact (a regular and ongoing close connection that may be personal, romantic, or financial) of a Senior Executive of a customer, potential customer or third-party vendor of Wells Fargo? select one required'"
    css_dropdown_select(q_str=q20_str, response="No")

    q21_str="button[aria-label='Are you currently serving in, or planning to serve in, any paid or unpaid (volunteer) position on a political campaign? select one required'"
    css_dropdown_select(q_str=q21_str, response="No")


workday_save_and_next(wait, frm="[Application Questions]", to="[Voluntary Disclosures]")
####################################################################
#   Voluntary Disclosures
####################################################################
workday_wait_till_pageload(wait)


skip_identify=False
try:
    time.sleep(2)
    found = driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Please select the Race/Ethnicity which most describes how you identify yourself. Asian')]")
    skip_identify=True
    print("Skipping identify")
except:
    skip_identify=False

if not skip_identify:
    q21_str="button[aria-label='Please select the Race/Ethnicity which most describes how you identify yourself. select one']"
    css_dropdown_select(q_str=q21_str, response="Asian (United States of America)")

    q22_str="button[aria-label='Please select your gender. select one']"
    css_dropdown_select(q_str=q22_str, response="Male")

    q23_str="button[aria-label='Please select the veteran status which most accurately describes your status. select one']"
    css_dropdown_select(q_str=q23_str, response="I am not a Veteran")

# Have to re-do this everytime..so not skipped
q_str=f"input[data-automation-id='agreementCheckbox']"
css_click_radio_box(q_str)

workday_save_and_next(wait, frm="[Voluntary Disclosures]", to="[Self Identify]")
####################################################################
#                     Self Identify
####################################################################
workday_wait_till_pageload(wait)

css_add_text_info(f'self-identification-content', "input[data-automation-id='name']", u.name)
css_add_text_info(f'self-identification-content', "input[data-automation-id='dateSectionYear-input']", u.today)

q_str=f"input[id='64cbff5f364f10000aeec521b4ec0000']"
css_click_radio_box(q_str)

workday_save_and_next(wait, frm="[Self Identify]", to="[Review & Submit]")
####################################################################
#                     Review and Submit
####################################################################
input ("Make sure all information is correct and hit the submit button on webpage. Then press enter here.")

#workday_save_and_next(wait, frm="[Review & Submit]", to="[Submit]")
#####################################################################
print ("Best of luck!")
driver.quit()
service.stop()
