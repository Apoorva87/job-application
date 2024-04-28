#!bin/python3
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains



##driver = webdriver.Chrome('/path/to/chromedriver')  # Optional argument, if not specified will search path.
#driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
#driver.get('http://www.google.com/');
#time.sleep(5) # Let the user actually see something!
#search_box = driver.find_element_by_name('q')
#search_box.send_keys('ChromeDriver')
#search_box.submit()
#time.sleep(5) # Let the user actually see something!
#driver.quit()
#

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
email_field.send_keys("yatin.karnik@gmail.com")
# Fill in the password field
password_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-automation-id='password']")))
password_field.send_keys("JobHunt2024*")
# Handle overlays or click interceptors
overlay = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id='click_filter']")))
overlay.click()

##################
# My information
##################
next_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id='bottom-navigation-next-button']")))

print("Working on My Information...")
search_box = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-uxi-widget-type='selectinput']")))
if search_box:
    search_box.send_keys("Wells Fargo Employee Referral")
    search_box.click()
else:
    print ("Cannot find referral box")

print ("Next screen..moving to My experience")
next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id='bottom-navigation-next-button']")))
if next_button:
    next_button.click()
else:
    print ("Next button not present..")


##################
# My experience
##################
next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id='bottom-navigation-next-button']")))
print ("Next screen..moving to My experience....")

def drive_all_experience(wait):
    add_work = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Add Work Experience']")))
    add_work.click()

    def add_field_info(under_div, field, key):
        key=key.replace("\r",' ')
        key=key.replace("\t",'  ')
        import html
        key = html.escape(key)
        for one in key.split("\n"):
            q = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"div[data-automation-id='{under_div}'] {field}")))
            q.send_keys(one)
            ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            print(one)

    add_field_info('workExperience-1', "input[data-automation-id='jobTitle']", "Business Operations & Strategy Consultant")
    add_field_info('workExperience-1', "input[data-automation-id='company']", "Confer Inc")
    add_field_info('workExperience-1', "input[data-automation-id='location']", "Dallas, TX")

    time.sleep(4)
    try:
        cb = driver.find_element(By.CSS_SELECTOR, "div[data-automation-id='workExperience-1'] input[data-automation-id='currentlyWorkHere']")
        if cb:
            cb.click()
    except:
        print ("Cannot click current job")
        pass

    add_field_info('workExperience-1', "div[data-automation-id='formField-startDate'] input[data-automation-id='dateSectionMonth-input']", "11/2021")
    job_1_str="""- Developed and launched a user-centric mobile application using advanced AI algorithms to enable efficient loan comparisons across digital platforms, significantly enhancing user experience and decision-making efficiency. (https://confer.today)
    - Engineered a cutting-edge digital mortgage platform that expanded borrower opportunities to reduce closing costs by 88%, showcasing deep expertise in e-commerce solutions. ●	Guided a cross-platform app launch within 90 days through meticulous agile project management and utilization of AWS, Google Cloud, enhancing development efficiency and product quality by 30%.
    - Spearheaded cross-functional teams under agile frameworks to enhance market responsiveness and tech adaptability, achieving a 25% faster time-to-market and increasing product adoption by 15% through effective leadership.
    - Led the strategic pivot of Confer Inc. to a B2B model, overseeing the launch of innovative financial software solutions for banks, which propelled a 25% increase in revenue and solidified market presence."""

    add_field_info('workExperience-1', "textarea[data-automation-id='description']", job_1_str)
    print ("Job 1 done.............")

    time.sleep(10)
    try:
        add_work = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-automation-id='workExperienceSection'] button[data-automation-id='Add Another']")))
        add_work.click()
    except:
        print ("Cannot add another job")
        import pdb; pdb.set_trace()
        pass

    add_field_info('workExperience-2', "input[data-automation-id='jobTitle']", "Senior Vice President, Head of National Operations & Head of Fee Strategy & Governance")
    add_field_info('workExperience-2', "input[data-automation-id='company']", "Wells Fargo")
    add_field_info('workExperience-2', "input[data-automation-id='location']", "Dallas, TX")
    add_field_info('workExperience-2', "div[data-automation-id='formField-startDate'] input[data-automation-id='dateSectionMonth-input']", "04/2014")
    add_field_info('workExperience-2', "div[data-automation-id='formField-endDate'] input[data-automation-id='dateSectionMonth-input']", "11/2021")
    job_2_str="""
    - Revolutionized Home Lending Fee Strategy, boosting regulatory compliance and operational efficiency which slashed error rates dramatically from 7% to less than 1%, by implementing agile methodologies and cross-functional team management.
    - Spearheaded the agile-driven launch of the 'Fee Service' engine, integrating over 1200 settlement agents which enhanced transaction efficiency and cut closing costs by 15%, showcasing strong project management and digital technology application.
    - Directed over 25 global remediation projects in collaboration with marketing, finance, legal, and operations teams, enhancing compliance with CFPB/RESPA/TILA standards under stringent agile practices. This cross-functional effort demonstrated adeptness in large-scale project management and regulatory adherence, ensuring cohesive strategy and execution across departments.
    - Implemented robust project management frameworks that improved product innovation cycles by 30% and operational agility by 25%, facilitating effective cross-functional collaborations and aligning with corporate strategic goals.
    - Developed and deployed innovative digital mortgage platforms that enhanced e-commerce transaction capabilities, boosting user engagement by 46% and financial throughput by 35%.
    - Led the agile transformation in operational practices, enhancing the speed and efficiency of regulatory project deliveries by 22%, and fostering an environment of continuous improvement and innovation. This strategic shift significantly streamlined compliance with federal regulations, contributing to a 18% reduction in compliance issues.
    - Boosted VOI, VOE, and VOD process accuracy and efficiency across international teams, decreasing turnaround by 1 day and led Vendor Support Teams across five locations to a 15% gain in Retail Fulfillment productivity with strategic tech initiatives.
    - Championed cross-functional initiatives, harmonizing tech developments with business and regulatory demands, which streamlined compliance, reduced audit findings by 20%, and achieved annual cost savings of $750k.
    """
    add_field_info('workExperience-2', "textarea[data-automation-id='description']", job_2_str)


    time.sleep(10)
    try:
        add_work = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-automation-id='workExperienceSection'] button[data-automation-id='Add Another']")))
        add_work.click()
    except:
        print ("Cannot add another job")
        import pdb; pdb.set_trace()
        pass


    add_field_info('workExperience-3', "input[data-automation-id='jobTitle']", "Vice President, Sales and Services System Office")
    add_field_info('workExperience-3', "input[data-automation-id='company']", "Wells Fargo")
    add_field_info('workExperience-3', "input[data-automation-id='location']", "Des Moines, IA")
    add_field_info('workExperience-3', "div[data-automation-id='formField-endDate'] input[data-automation-id='dateSectionMonth-input']", "04/2014")
    add_field_info('workExperience-3', "div[data-automation-id='formField-startDate'] input[data-automation-id='dateSectionMonth-input']", "05/2007")
    job_2_str="""
    ●	Pioneered the SDLC for a groundbreaking product recommendation tool, markedly boosting digital customer engagement and securing the prestigious J.D. Power Associates Award for three consecutive years.
    ●	Championed the launch of Wells Fargo's first mobile app for home mortgage services and an award-winning product recommendation tool, developed in collaboration with UX/UI teams to set a digital standard across iOS, Android, and Blackberry platforms. This initiative, enhancing user engagement and support, was adopted by 16,000 mortgage loan originators and significantly improved our digital customer service capabilities.
    ●	Spearheaded the 'Fee Engine' design, a business rules engine using automation to revamp fee calculations, enhancing accuracy and eliminating over-tolerance losses by $2M annually, driving operational improvements.
    ●	Implemented process automation strategies that yielded $12M in annual cost savings, streamlining technology solutions in pricing and fee estimation.
    ●	Directed the design of the HARP/HAMP triage tool, partnering with UX/UI teams to enhance user interface and customer experience, which reviewed 3,000 applications in its first week and improved mortgage affordability and diversity. This project showcased our commitment to using digital solutions to enhance customer service.
    """
    add_field_info('workExperience-3', "textarea[data-automation-id='description']", job_2_str)


    time.sleep(10)
    try:
        add_work = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-automation-id='workExperienceSection'] button[data-automation-id='Add Another']")))
        add_work.click()
    except:
        print ("Cannot add another job")
        import pdb; pdb.set_trace()
        pass


    add_field_info('workExperience-4', "input[data-automation-id='jobTitle']", "Sr. Business Analyst")
    add_field_info('workExperience-4', "input[data-automation-id='company']", "Wells Fargo")
    add_field_info('workExperience-4', "input[data-automation-id='location']", "Des Moines, IA")
    add_field_info('workExperience-4', "div[data-automation-id='formField-startDate'] input[data-automation-id='dateSectionMonth-input']", "12/2004")
    add_field_info('workExperience-4', "div[data-automation-id='formField-endDate'] input[data-automation-id='dateSectionMonth-input']", "05/2007")
    job_2_str="""
    ●	Developed a policy lookup tool for 12,000 mortgage loan originators, cutting lookup times and elevating match accuracy by 40%.
    ●	Created a mortgage recommendation tool, raising mortgage acceptance by 20% and increasing customer satisfaction by offering borrowers better financial terms.
    ●	Designed and deployed a mortgage reconfiguration algorithm, augmenting approval rates by 25% for previously at-risk mortgages by aligning with alternative investor guidelines.
    """
    add_field_info('workExperience-4', "textarea[data-automation-id='description']", job_2_str)

#comment this if this doesnt need to be driven
drive_all_experience(wait)


next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id='bottom-navigation-next-button']")))
if next_button:
    next_button.click()
else:
    print ("Next button not present..")
##################
# My Application
##################
print ("Next screen..moving to Application Questions....")
next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id='bottom-navigation-next-button']")))

def answer_questions(q_str, response):
    q = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f"{q_str}")))
    q.click()
    driver.execute_script("arguments[0].scrollIntoView(true);", q) 
    wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{response}']"))).click()

q1_str="button[aria-label='Are you a current or former Wells Fargo employee? select one required']"
answer_questions(q_str=q1_str, response="Yes, former employee")

driver.find_element(By.CSS_SELECTOR, "textarea[data-automation-id='fbfd9c6b32531015123e4853743e0001']").send_keys('2711')


q2_str="button[aria-label='Are you 18 years of age or older? select one required']"
answer_questions(q_str=q2_str, response="Yes")

q3_str="button[aria-label='Will you now or in the future require sponsorship for employment visa to work in the country you are applying to work in? For the US, this includes sponsorship of H-1B, TN, or E-3 visas. Persons currently on F-1 visas completing curricular or optional practical training should answer yes. select one required'"
answer_questions(q_str=q3_str, response="No")


q4_str="button[aria-label='Have you ever been involuntarily discharged or asked to resign from a position? Your response should not include discharges due to layoff, displacement, or reorganization. select one required'"
answer_questions(q_str=q4_str, response="No")

q5_str="button[aria-label='Have you ever been disciplined by an administrative agency or the subject of an administrative order relating to conduct or practices involving any aspect of the financial services, insurance, securities, or real estate industries or any other licensed industry profession? An Administrative agency is a government body authorized to implement legislative directives by developing more precise and technical rules. select one required'"
answer_questions(q_str=q5_str, response="No")

q6_str="button[aria-label='Do you have any non-compete/non-solicitation or other agreements that prevents or restricts you from performing the job for which you are applying for? select one required'"
answer_questions(q_str=q6_str, response="No")

q7_str="button[aria-label='Do you have any fiduciary appointments (such as an executor, personal representative, administrator, guardian, trustee, or any similar fiduciary designation) that involve a current Wells Fargo customer, or someone you know that intends to become a Wells Fargo customer (for example, a current client)? select one required'"
answer_questions(q_str=q7_str, response="No")

q8_str="button[aria-label='Are you currently a member of, or do you currently serve in any capacity on, a Board of Directors, Advisory Board, Committee, Trustee Board, or have any other similar position with any for-profit or non-profit organization? select one required'"
answer_questions(q_str=q8_str, response="No")


q9_str="button[aria-label='Do you currently have, or plan to have, any employment or other work that you intend to continue if you accept a job at Wells Fargo? Including, but not limited to, an independent contractor, consultant, real estate agent, home inspector, appraiser, tax preparer, seasonal or part-time employee. select one required'"
answer_questions(q_str=q9_str, response="No")

q10_str="button[aria-label='Do you currently have 25% or more (10% or more if seeking a Wells Fargo Executive Officer role) ownership interest in, or plan to have such an ownership interest in any for-profit business entity or activity? Including an inactive business, business entities formed for the purpose of business holdings, investments, or future business activities; sole proprietorships; or non-registered business entities or activities. select one required'"
answer_questions(q_str=q10_str, response="No")

q11_str="button[aria-label='Do you currently serve, service, or plan to serve in any position of control with a for-profit business entity or activity? select one required'"
answer_questions(q_str=q11_str, response="No")

q12_str="button[aria-label='Are you currently serving as, or planning to serve as, an elected or appointed official or as a member, director, officer, or employee of a government entity or governmental or public agency, authority, advisory board, city council, school board, political party committee, or other similar board or entity? select one required'"
answer_questions(q_str=q12_str, response="No")

q13_str="button[aria-label='Do you have a family relationship (biological, adopted, marriage, domestic partnership, civil union, or some other arrangement), or are you a close personal contact (a regular and ongoing close connection that may be personal, romantic, or financial) of any employees, contingent resources, or board members of Wells Fargo or its subsidiaries? select one required'"
answer_questions(q_str=q13_str, response="Yes")
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "textarea[data-automation-id='fbfd9c6b32531015123e4abc2b620006']").send_keys('Swati Karnik. Wife. Dallas, Texas')

q14_str="button[aria-label='Do you currently work, or have you worked for KPMG (Klynveld Peat Marwick Goerdeler - the bank’s auditor) during the past five years? select one required'"
answer_questions(q_str=q14_str, response="No")

q15_str="button[aria-label='Are you a current or former military spouse or domestic partner? select one required'"
answer_questions(q_str=q15_str, response="No")

q16_str="button[aria-label='Are you a Senior Government Official or have you served as one in the past two years? select one required'"
answer_questions(q_str=q16_str, response="No")

q17_str="button[aria-label='Did a Senior Government Official refer you for this position? select one required'"
answer_questions(q_str=q17_str, response="No")

q18_str="button[aria-label='Do you have a family relationship (biological, adopted, marriage, domestic partnership, civil union, or some other arrangement) with, or are you a close personal contact (a regular and ongoing close connection that may be personal, romantic, or financial) of a Senior Government Official? select one required'"
answer_questions(q_str=q18_str, response="No")

q19_str="button[aria-label='Did a Senior Executive of a customer, potential customer or third-party vendor of Wells Fargo refer you for this position? select one required'"
answer_questions(q_str=q19_str, response="No")

q20_str="button[aria-label='Do you have a family relationship (biological, adopted, marriage, domestic partnership, civil union, or some other arrangement) with, or are you a close personal contact (a regular and ongoing close connection that may be personal, romantic, or financial) of a Senior Executive of a customer, potential customer or third-party vendor of Wells Fargo? select one required'"
answer_questions(q_str=q20_str, response="No")

q21_str="button[aria-label='Are you currently serving in, or planning to serve in, any paid or unpaid (volunteer) position on a political campaign? select one required'"
answer_questions(q_str=q21_str, response="No")

time.sleep(2)
next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id='bottom-navigation-next-button']")))
if next_button:
    next_button.click()
else:
    print ("Next button not present..")

##################
# My Application
##################
next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id='bottom-navigation-next-button']")))
#next_button.click()


q21_str="button[aria-label='Please select the Race/Ethnicity which most describes how you identify yourself. select one']"
answer_questions(q_str=q21_str, response="Asian (United States of America)")

q22_str="button[aria-label='Please select your gender. select one']"
answer_questions(q_str=q22_str, response="Male")

q23_str="button[aria-label='Please select the veteran status which most accurately describes your status. select one']"
answer_questions(q_str=q23_str, response="I am not a Veteran")
#dropdown_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-haspopup='listbox']")))
#dropdown_button.click()
# Wait for the listbox to appear and locate the "Yes" option
#yes_option = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[contains(text(), 'Yes')]")))
# Click the "Yes" option to select it
#yes_option.click()
#print ("Finished...")
#next_button.click()


#wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
#next_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-automation-id='bottom-navigation-next-button']")))
#print ("Next screen..moving to Application Questions")
#https://wd1.myworkdaysite.com/en-US/recruiting/wf/WellsFargoJobs/job/BEE-CAVE%2C-TX/Senior-Premier-Banker---BEE-CAVE---GALLERIA---Bee-Cave--TX_R-364228/apply/useMyLastApplication

next_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-automation-id='bottom-navigation-next-button']")))
if next_button:
    next_button.click()
else:
    print ("Next button not present..")

import pdb; pdb.set_trace()
time.sleep(120) # Let the user actually see something!
print("click waiting..over + 120s")
driver.quit()
service.stop()
