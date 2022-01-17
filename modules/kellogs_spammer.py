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
import fake_identity as fid

from constants.kellogs import elementids_kellogs as element_id
from constants.kellogs import xpaths_kellogs as xpaths
from constants.kellogs import location_kellogs as location
from constants import common 


def navigate_to_kellogs_create_account_page(driver, random_city):
    driver.get(location.CITIES_TO_URLS[random_city])
    driver.implicitly_wait(10)
    time.sleep(15)
    #WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, CREATE_AN_ACCOUNT_BUTTON)))
    driver.find_element_by_xpath(xpaths.APPLY_NOW_BUTTON_1).click()
    driver.find_element_by_xpath(xpaths.APPLY_NOW_BUTTON_2).click()
    driver.find_element_by_xpath(xpaths.CREATE_AN_ACCOUNT_BUTTON).click()


def generate_account(driver, fake_identity, using_mailtm):
    """
        Generates account on the Kellogs website and verifies it with the emailed passcode 
    """

    random_city = random.choice(list(location.CITIES_TO_URLS.keys()))
    printf(f"Applying for job in {random_city}")
    time.sleep(2)

    navigate_to_kellogs_create_account_page(driver, random_city)

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
        elif key == 'pn':
            info = fake_identity['phone']

        driver.find_element_by_xpath(xpaths.XPATHS_2.get(key)).send_keys(info)

    time.sleep(random.randint(0, 2))
    select = Select(driver.find_element_by_id(element_id.COUNTRY_REGION_CODE_LABEL))
    select.select_by_value(location.COUNTRY_CODE_US)
    select = Select(driver.find_element_by_id(element_id.COUNTRY_REGION_OF_RESIDENCE_LABEL))
    select.select_by_value(location.COUNTRY_CODE_US)

    driver.find_element_by_xpath(xpaths.READ_ACCEPT_DATA_PRIVACY_STATEMENT_ANCHORTAG).click()
    time.sleep(1.5)
    driver.find_element_by_xpath(xpaths.ACCEPT_BUTTON).click()
    time.sleep(2)
    
    driver.find_element_by_xpath(xpaths.CREATE_ACCOUNT_BUTTON).click()
    time.sleep(1.5)
    for i in range(120):
        time.sleep(1.5)
        passcode = fid.get_passcode_from_email(using_mailtm, fake_identity)
        if passcode:
            break
    else: #failed to get passcode
        #args.mailtm ^= True
        os.execv(sys.argv[0], sys.argv) #restart program with same command line args 

    driver.find_element_by_xpath(xpaths.VERIFY_EMAIL_INPUT).send_keys(passcode)
    driver.find_element_by_xpath(xpaths.VERIFY_EMAIL_BUTTON).click()

    printf(f"Success! Made Kellogs account using email: {email}")

    return random_city



def fill_out_application_and_submit(driver, random_city, fake_identity):
    # wait for page to load
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, xpaths.PROFILE_INFORMATION_DROPDOWN)))

    # fill out form parts of app
    driver.find_element_by_xpath(xpaths.PROFILE_INFORMATION_DROPDOWN).click()
    driver.find_element_by_xpath(xpaths.CANDIDATE_SPECIFIC_INFORMATION_DROPDOWN).click()

    for key in xpaths.XPATHS_1.keys():

        if key == 'resume':
            driver.find_element_by_xpath(xpaths.UPLOAD_A_RESUME_BUTTON).click()
            info = os.getcwd() + '/'+fake_identity['resume_img_filepath']
        elif key == 'addy':
            info = fake_identity['street_address']
        elif key == 'city':
            info = random_city
        elif key == 'zip':
            info = location.CITIES_TO_ZIP_CODES[random_city]
        elif key == 'job':
            info = fake_identity['job']
        elif key == 'salary':
            first = random.randrange(15000, 30000, 5000)
            info = f'{format(first, ",")}-{format(random.randrange(first + 5000, 35000, 5000), ",")}'

        driver.find_element_by_xpath(xpaths.XPATHS_1.get(key)).send_keys(info)

    printf(f"successfully filled out app forms for {random_city}")

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
    