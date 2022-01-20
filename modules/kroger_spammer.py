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

def navigate_to_kroger_create_account_page(driver):
    driver.get(location.CREATE_ACCOUNT_URL)
    driver.implicitly_wait(10)
    time.sleep(10)
    #WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, CREATE_AN_ACCOUNT_BUTTON)))
    driver.find_element_by_xpath(xpaths.CREATE_AN_ACCOUNT_BUTTON).click()


def generate_account(driver, fake_identity, using_mailtm):
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



def fill_out_application_and_submit(driver, random_city, fake_identity):
    driver.get(random.choice(location.CITIES_TO_URLS[random_city]))
    
    # wait for page to load
    driver.implicitly_wait(10)
    time.sleep(10)

    # open all dropdowns
    driver.find_element_by_xpath(xpaths.MY_DOCUMENTS_DROPDOWN).click()
    driver.find_element_by_xpath(xpaths.PROFILE_INFORMATION_DROPDOWN).click()
    driver.find_element_by_xpath(xpaths.WORK_HISTORY_DROPDOWN).click()
    driver.find_element_by_xpath(xpaths.EDUCATION_EXPERIENCE_DROPDOWN).click()
    driver.find_element_by_xpath(xpaths.JOB_SPECIFIC_INFO_DROPDOWN).click()
    
    printf("Sleeping for 1200 seconds")
    time.sleep(1200)

    for key in xpaths.XPATHS_1.keys():
        if key == 'resume':
            driver.find_element_by_xpath(xpaths.UPLOAD_A_RESUME_BUTTON).click()
            time.sleep(random.randint(0, 2))
            driver.find_element_by_xpath(xpaths.UPLOAD_FROM_DEVICE_BUTTON).click()
            time.sleep(random.randint(0, 2))
            info = os.getcwd() + '/'+fake_identity['resume_img_filepath']
        elif key == 'addy':
            info = fake_identity['street_address']
        elif key == 'city':
            info = random_city
        elif key == 'zip':
            info = location.CITIES_TO_ZIP_CODES[random_city]
        elif key == 'state':
            info = location.CITIES_TO_STATES[random_city]
        elif key == 'phone_number':
            info = fake_identity['phone']

        driver.find_element_by_xpath(xpaths.XPATHS_1.get(key)).send_keys(info)
    
    """
        elif key == 'job':
            info = fake_identity['job']
        elif key == 'salary':
            first = random.randrange(15000, 30000, 5000)
            info = f'{format(first, ",")}-{format(random.randrange(first + 5000, 35000, 5000), ",")}'
    """
    #work history #TODO Fill this out 
    for key in xpaths.XPATHS_WORK_HISTORY:
        pass
        
    #education 
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

            driver.find_element_by_xpath(xpaths.XPATHS_1.get(key)).send_keys(info)
    else:
        driver.find_element_by_xpath(xpaths.XPATHS_EDUCATION['education_type']).send_keys('High School Diploma')

    #job specific information #TODO Fill this out 
    for key in xpaths.XPATHS_1.keys():
        if key == 'resume':
            driver.find_element_by_xpath(xpaths.UPLOAD_A_RESUME_BUTTON).click()
            time.sleep(random.randint(0, 2))
            driver.find_element_by_xpath(xpaths.UPLOAD_FROM_DEVICE_BUTTON).click()
            time.sleep(random.randint(0, 2))
            info = os.getcwd() + '/'+fake_identity['resume_img_filepath']
        elif key == 'addy':
            info = fake_identity['street_address']
        elif key == 'city':
            info = random_city
        elif key == 'zip':
            info = location.CITIES_TO_ZIP_CODES[random_city]
        elif key == 'state':
            info = location.CITIES_TO_STATES[random_city]
        elif key == 'phone_number':
            info = fake_identity['phone']

        driver.find_element_by_xpath(xpaths.XPATHS_1.get(key)).send_keys(info)
    #availability #TODO Fill this out 
    #previous employment info #TODO Fill this out 
    #personal background info #TODO Fill this out 
    #emergency contact info #TODO Fill this out 
    #applicant statement info #TODO Fill this out 
    #volunatary information info #TODO Fill this out 
    #yes no questions #TODO Fill this out 

    # fill out dropdowns
    select = Select(driver.find_element_by_id(element_id.CITIZEN_QUESTION_LABEL))
    select.select_by_visible_text(common.YES)
    select = Select(driver.find_element_by_id(element_id.COUNTRY_OF_ORIGIN_LABEL))
    select.select_by_visible_text(location.FULL_NAME_US)
    select = Select(driver.find_element_by_id(element_id.EIGHTEEN_YEARS_OLD_LABEL))
    select.select_by_visible_text(common.YES)
    select = Select(driver.find_element_by_id(element_id.REQUIRE_SPONSORSHIP_LABEL))
    select.select_by_visible_text(common.NO)
    select = Select(driver.find_element_by_id(element_id.PREVIOUSLY_WORKED_LABEL))
    select.select_by_visible_text(common.NO)
    select = Select(driver.find_element_by_id(element_id.PREVIOUSLY_PARTNERED_LABEL))
    select.select_by_visible_text(common.NO)
    select = Select(driver.find_element_by_id(element_id.RELATIVE_WORKER_LABEL))
    select.select_by_visible_text(common.NO)
    select = Select(driver.find_element_by_id(element_id.ESSENTIAL_FUNCTIONS_LABEL))
    select.select_by_visible_text(common.YES)
    select = Select(driver.find_element_by_id(element_id.PREVIOUSLY_PARTNERED_LABEL))
    select.select_by_visible_text(common.NO)
    time.sleep(1)
    select = Select(driver.find_element_by_id(element_id.GENDER_LABEL))
    gender = random.choice(common.GENDERS_LIST)
    select.select_by_visible_text(gender)
    driver.find_element_by_xpath(xpaths.MIXER_QUESTION_1_LABEL).click()
    driver.find_element_by_xpath(xpaths.MIXER_QUESTION_2_LABEL).click()

    els = driver.find_elements_by_xpath(xpaths.LONG_PERIODS_QUESTION_LABEL)
    [el.click() for el in els]

    time.sleep(5)
    driver.find_element_by_xpath(xpaths.APPLY_BUTTON).click()
    printf(f"successfully submitted application")
    # take out the trash