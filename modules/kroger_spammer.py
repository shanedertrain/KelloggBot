from datetime import datetime, timedelta
import time
import random
import os
import sys

from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#custom
from configuration import printf

from constants.kroger import elementids_kroger as element_id
from constants.kroger import xpaths_kroger as xpaths
from constants.kroger import location_kroger as location
from constants import common 
import constants.kroger.application_kroger  as app_data

import fake_identity as fid

from faker import Faker

fake = Faker()

def navigate_to_kroger_create_account_page(driver):
    driver.get(location.CREATE_ACCOUNT_URL)
    driver.implicitly_wait(10)
    time.sleep(10)
    #WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, CREATE_AN_ACCOUNT_BUTTON)))
    driver.find_element_by_xpath(xpaths.CREATE_AN_ACCOUNT_BUTTON).click()


def generate_account(driver, fake_identity):
    """
        Generates account on the Kellogs website and verifies it with the emailed passcode 
    """
    random_city = random.choice(list(location.CITIES_TO_URLS.keys()))
    printf(f"Applying for job in {random_city}")
    time.sleep(2)

    navigate_to_kroger_create_account_page(driver)

    email = fake_identity['email']
    for key in xpaths.XPATHS_2.keys():
        if key in ('email', 'email-retype'):
            info = email
        elif key in ('pass', 'pass-retype'):
            info = fake_identity['password']
        elif key == 'first_name':
            info = fake_identity['first_name']
        elif key == 'last_name':
            info = fake_identity['last_name']
        elif key == 'last_name':
            info = fake_identity['last_name']
        elif key == 'country':
            info = location.FULL_NAME_US

        driver.find_element_by_xpath(xpaths.XPATHS_2.get(key)).send_keys(info)

    time.sleep(random.randint(0, 2))
    driver.find_element_by_xpath(xpaths.READ_TERMS_BUTTON).click()

    time.sleep(random.randint(0, 2))
    driver.find_element_by_xpath(xpaths.ACCEPT_TERMS_BUTTON).click()

    time.sleep(random.randint(0, 2))
    driver.find_element_by_xpath(xpaths.CREATE_ACCOUNT_BUTTON).click()

    printf(f"Success! Made Kroger account using email: {email}")

    return random_city


def fill_out_application_and_submit(driver, random_city, fake_identity, upload_resume, verbose):
    driver.get(random.choice(location.CITIES_TO_URLS[random_city]))
    
    # wait for page to load
    driver.implicitly_wait(10)
    time.sleep(10)

    #driver.find_element_by_xpath(xpaths.MY_DOCUMENTS_DROPDOWN).click()

    #resume 
    if upload_resume:
        driver.find_element_by_xpath(xpaths.UPLOAD_A_RESUME_BUTTON).click()
        time.sleep(random.randint(0, 2))
        driver.find_element_by_xpath(xpaths.UPLOAD_FROM_DEVICE_BUTTON).click()
        time.sleep(random.randint(0, 2))
        file_to_upload = random.choice([fake_identity['resume_img_filepath'], fake_identity['resume_pdf_filepath']])
        print(f"Uploading: {file_to_upload}")
        handle_upload_file_dialog(file_to_upload.parent, file_to_upload.name)
        time.sleep(random.randint(2, 5))

    
    #profile info
    driver.find_element_by_xpath(xpaths.PROFILE_INFORMATION_DROPDOWN).click()
    for key in xpaths.XPATHS_PROFILE_INFO.keys():
        info = None
        if key == 'legal_first_name':
            #info = fake_identity['first_name']
            pass
        elif key == 'legal_last_name':
            #info = fake_identity['last_name']
            pass
        elif key == 'phone_number':
            info = fake_identity['phone']
        elif key == 'phone_country':
            info = 'United States'
        elif key == 'email':
            #info = fake_identity['email']
            pass
        elif key == 'addy1':
            info = fake_identity['street_address']
        elif key == 'country':
            info = 'United States'
        elif key == 'state':
            time.sleep(1)
            info = 'Colorado' #hardcode bad >:c but this shit is all xpaths I guess
        elif key == 'city':
            info = fake_identity['city']
        elif key == 'zip':
            info = fake_identity['zip_code']
        
        if verbose: print(f"{key}: {info}")
        if info: driver.find_element_by_xpath(xpaths.XPATHS_PROFILE_INFO.get(key)).send_keys(info)
    
    #work history #TODO: function to fill out arbitrary number of jobs 
    driver.find_element_by_xpath(xpaths.WORK_HISTORY_DROPDOWN).click()
    dt_offset = timedelta(days=0) #offset to make job dates relatively contiguous
    jobs = [a for a in fake_identity.keys() if 'job' in a] #this is kinda dirt, but dynamic
    for idx, job in enumerate(['job_0']): 
        print(f"Job {idx}")
        currently_employed = random.choice([True, False]) if idx == 0 else False
        
        now = datetime.now()
        if currently_employed:
            end_date_dt = now
        else:
            end_date_dt = now-timedelta(days=random.randrange(0, 365)) - dt_offset
        from_date_dt = end_date_dt-timedelta(days=random.randrange(10, 1000))
        dt_offset = now - from_date_dt

        for key in xpaths.XPATHS_WORK_HISTORY:
            info = None
            if key == 'employer_type':
                employer_type = 'Current Employer' if currently_employed else 'Previous Employer'
                info = employer_type
            elif key == 'from_date': #do this for each job in fid too and make cohesive
                info = from_date_dt.strftime('%m/%d/%Y') #use fid to generate believable dates, put into fake id
                driver.find_element_by_xpath(xpaths.XPATHS_WORK_HISTORY['company_name']).click()
            elif key == 'end_date':
                if employer_type != 'Current Employer':
                    info = end_date_dt.strftime('%m/%d/%Y')
            elif key == 'company_name':
                info = fake_identity[f'company_{idx}']
            elif key == 'company_state':
                time.sleep(2)
                info = 'Colorado' #could make this randomly generate into fake ID
            elif key == 'company_phone':
                info =  fid.random_phone()#could add to fake id. make area code same as address
            elif key == 'employment_type':
                info = random.choice(['Full-Time', 'Part-Time'])
            elif key == 'type_of_company':
                info = random.choice(app_data.type_of_company_list)
            elif key == 'company_city':
                info = random_city #generate and add company data to fid
            elif key == 'position_title':
                info = fake_identity[f'job_{idx}']
            elif key == 'reason_for_leaving':
                info = 'Not Applicable (Currently Employed)' if currently_employed else'Leaving Company Voluntarily'
            elif key == 'may_we_contact':
                info = 'Yes'
            elif key == 'company_country':
                info = 'United States'
            elif key == 'company_postal_code':
                info = fake_identity['zip_code']
            elif key == 'position_type':
                info = 'Employee'

            if verbose: print(f"{key}: {info}")
            if info: driver.find_element_by_xpath(xpaths.XPATHS_WORK_HISTORY.get(key)).send_keys(info)
    
    driver.find_element_by_xpath(xpaths.EDUCATION_EXPERIENCE_DROPDOWN).click()

    #education #TODO: fill this out after it works in general
    if False:
        degree_split = fake_identity['degree'].split(' ')
        degree = degree_split[0] #TODO make schools match the state
                                    #TODO for now use only colorado schools
        area_of_study = degree_split[2:] #TODO reformat education to input valid areas of study
        for key in xpaths.XPATHS_EDUCATION.keys():
            if key == 'education_type':
                
                info = f'{degree}s'
            elif key == 'country':
                info = location.FULL_NAME_US
            elif key == 'state':
                info = location.CITIES_TO_STATES[random_city]
            elif key == 'city':
                info = random_city
            elif key == 'school':
                info = random_city
            elif key == 'degree_status':
                info = location.CITIES_TO_ZIP_CODES[random_city]
            elif key == 'area_of_study':
                info = fake_identity['phone']

            driver.find_element_by_xpath(xpaths.XPATHS_EDUCATION.get(key)).send_keys(info)

    driver.find_element_by_xpath(xpaths.JOB_SPECIFIC_INFO_DROPDOWN).click()
    #job specific information #TODO Fill this out 
    for key in xpaths.XPATHS_JOB_SPECIFIC.keys():
        info = None
        if key == 'ssn':
            info = fake_identity['ssn']
        elif key == 'learned_how':
            info = random.choice(app_data.learned_how_list)
        elif key == 'classes_attending':
            info = random.choice(['Yes', 'No'])
        elif key == 'highest_education':
            info = random.choice([app_data.education_list])
        elif key == 'employed_relatives':
            info = 'No'
        elif key == 'veteran':
            info = 'No, I am not a veteran'
        elif key == '18_or_older':
            info = 'Yes'
        elif key == 'prohibition':
            info = 'No'
        elif key == 'first_choice':
            first_choice = random.choice(app_data.position_preference_list)
            info = first_choice
        elif key == 'second_choice':
            if first_choice != 'Any':
                second_choice = random.choice(app_data.position_preference_list)
                info = second_choice
        elif key == 'start_date':
            info = (now+timedelta(days=random.randint(0, 30))).strftime('%m/%d/%Y')
        elif key == 'evenings':
            info = 'yes'
        elif key == 'weekends':
            info = 'yes'
        elif key == 'holidays':
            info = 'yes'
        elif key == 'type_desired':
            info = random.choice(['Full-Time', 'Part-Time'])
        elif key == 'best_call_time':
            info = random.choice(['Afternoon', 'Any', 'Evening', 'Morning'])
        elif key == 'available_sunday': #TODO make availability look for cohesive
            info = random.choice(app_data.available_list)
        elif key == 'available_monday':
            info = random.choice(app_data.available_list)
        elif key == 'available_tuesday':
            info = random.choice(app_data.available_list)
        elif key == 'available_wednesday':
            info = random.choice(app_data.available_list)
        elif key == 'available_thursday':
            info = random.choice(app_data.available_list)
        elif key == 'available_friday':
            info = random.choice(app_data.available_list)
        elif key == 'available_saturday':
            info = random.choice(app_data.available_list)
        elif key == 'worked_here_before':
            info = random.choice(['No', 'N/A'])
        elif key == 'other_work_fits':
            info = 'N/A'
        elif key == 'terminated':
            info = 'No'
        elif key == 'cash_shortages':
            info = 'No'
        elif key == 'conviction_legal_name':
            info = f"{fake_identity['first_name']} {fake_identity['last_name']}"
        elif key == 'convicted':
            info = 'No'
        elif key == 'contact_first_name': #TODO: make fid generate contacts 
            info = fake.first_name()
        elif key == 'contact_last_name':
            info = fake_identity['last_name']
        elif key == 'contact_relationship':
            info = random.choice(app_data.contact_relationship_list)
        elif key == 'contact_phone_number':
            info = f"{fake_identity['phone'][:3]}-{random.randint(1,999):03d}-{random.randint(1,9999):04d}"
        elif key == 'app_statement_ack':
            info = 'I Understand'
        elif key == 'app_statement_ack_signature':
            info = f"{fake_identity['first_name']} {fake_identity['last_name']}"

        if verbose: print(f"{key}: {info}")
        if info:
            driver.find_element_by_xpath(xpaths.XPATHS_JOB_SPECIFIC.get(key)).send_keys(info)
    
    if random.choice([True, False]):
        driver.find_element_by_xpath(xpaths.XPATHS_JOB_SPECIFIC['gender_female']).click()
    else:
        driver.find_element_by_xpath(xpaths.XPATHS_JOB_SPECIFIC['gender_male']).click()


    driver.find_element_by_xpath(xpaths.XPATHS_JOB_SPECIFIC['15_or_older_yes']).click()
    driver.find_element_by_xpath(xpaths.XPATHS_JOB_SPECIFIC['18_or_older_yes']).click()
    driver.find_element_by_xpath(xpaths.XPATHS_JOB_SPECIFIC['21_or_older_yes']).click()
    driver.find_element_by_xpath(xpaths.XPATHS_JOB_SPECIFIC['legal_verification_yes']).click()
    driver.find_element_by_xpath(xpaths.XPATHS_JOB_SPECIFIC['accomodation_yes']).click()
    
    if random.choice([True, False]):
        driver.find_element_by_xpath(xpaths.XPATHS_JOB_SPECIFIC['overnight_yes']).click()
    else:
        driver.find_element_by_xpath(xpaths.XPATHS_JOB_SPECIFIC['overnight_no']).click()

    time.sleep(5)
    driver.find_element_by_xpath(xpaths.XPATHS_JOB_SPECIFIC['apply_button']).click()
    printf(f"successfully submitted application")

import win32com.client as comclt
#TODO: not working
def handle_upload_file_dialog(file_path_parent, filename):
    #credit: https://stackoverflow.com/questions/34197991/selenium-python-interact-with-fileopen-window
    sleep = 1
    windowsShell = comclt.Dispatch("WScript.Shell")
    time.sleep(sleep)
    windowsShell.SendKeys("{TAB}{TAB}{TAB}{TAB}{TAB}")
    time.sleep(sleep)
    windowsShell.SendKeys("{ENTER}")
    time.sleep(sleep)
    windowsShell.SendKeys(f'{file_path_parent}')
    time.sleep(sleep)
    windowsShell.SendKeys("{ENTER}")
    time.sleep(sleep)
    windowsShell.SendKeys("{TAB}")
    time.sleep(sleep)
    windowsShell.SendKeys("{TAB}")
    time.sleep(sleep)
    windowsShell.SendKeys("{TAB}")
    time.sleep(sleep)
    windowsShell.SendKeys("{TAB}")
    time.sleep(sleep)
    windowsShell.SendKeys("{TAB}")
    time.sleep(sleep)
    windowsShell.SendKeys("{TAB}")
    time.sleep(sleep)
    windowsShell.SendKeys(f"{filename}")
    time.sleep(sleep)
    windowsShell.SendKeys("{TAB}{TAB}")
    time.sleep(sleep)
    windowsShell.SendKeys("{ENTER}")
    