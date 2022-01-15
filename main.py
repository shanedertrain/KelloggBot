import os
import random
import sys
import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pdf2image import convert_from_path

from webdriver_manager.chrome import ChromeDriverManager
os.environ['WDM_LOG_LEVEL'] = '0'

#custom stuff
from configuration.configuration import printf
import fake_identity as fid
from resume_faker import make_resume

from constants.common import *
from constants.fileNames import *
from constants.classNames import *
from constants.elementIds import *
from constants.email import *
from constants.location import *
from constants.parser import *
from constants.urls import *
from constants.xPaths import *
from constants.areaCodes import *

from constants.location import CITIES_TO_URLS

os.environ["PATH"] += ":/usr/local/bin" # Adds /usr/local/bin to my path which is where my ffmpeg is stored

#Option parsing
parser = argparse.ArgumentParser(SCRIPT_DESCRIPTION,epilog=EPILOG)
parser.add_argument('--debug',action='store_true',default=False,required=False,help=DEBUG_DESCRIPTION,dest='debug_enabled')
parser.add_argument('--mailtm',action='store_true',default=False,required=False,help=MAILTM_DESCRIPTION,dest='using_mailtm')
parser.add_argument('--no_warn_installs', action='store_false', default=True, dest='warn_installs')
parser.add_argument('--exploiter', action='store', default='Kellogs', dest='exploiter')
args = parser.parse_args()
# END TEST

import configuration.configuration as config
config.warn_installs = args.warn_installs

def start_driver(random_city):
    options = Options()
    if args.debug_enabled:
        driver = webdriver.Chrome(ChromeDriverManager().install())
    else:
        options.add_argument(f"user-agent={USER_AGENT}")
        options.add_argument('disable-blink-features=AutomationControlled')
        options.headless = True
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        driver.set_window_size(1440, 900)

    driver.get(CITIES_TO_URLS[random_city])
    driver.implicitly_wait(10)
    time.sleep(15)
    #WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, CREATE_AN_ACCOUNT_BUTTON)))
    driver.find_element_by_xpath(APPLY_NOW_BUTTON_1).click()
    driver.find_element_by_xpath(APPLY_NOW_BUTTON_2).click()
    driver.find_element_by_xpath(CREATE_AN_ACCOUNT_BUTTON).click()
    return driver


def generate_account(driver, fake_identity):
    """
        Generates account on the employer's website and verifies it with the emailed passcode 
    """
    email = fake_identity['email']
    for key in XPATHS_2.keys():
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

        driver.find_element_by_xpath(XPATHS_2.get(key)).send_keys(info)

    time.sleep(random.randint(0, 2))
    select = Select(driver.find_element_by_id(COUNTRY_REGION_CODE_LABEL))
    select.select_by_value(COUNTRY_CODE_US)
    select = Select(driver.find_element_by_id(COUNTRY_REGION_OF_RESIDENCE_LABEL))
    select.select_by_value(COUNTRY_CODE_US)

    driver.find_element_by_xpath(READ_ACCEPT_DATA_PRIVACY_STATEMENT_ANCHORTAG).click()
    time.sleep(1.5)
    driver.find_element_by_xpath(ACCEPT_BUTTON).click()
    time.sleep(2)
    
    driver.find_element_by_xpath(CREATE_ACCOUNT_BUTTON).click()
    time.sleep(1.5)
    for i in range(120):
        time.sleep(1.5)
        passcode = fid.get_passcode_from_email()
        if passcode:
            break
    else: #failed to get passcode
        args.mailtm ^= True
        os.execv(sys.argv[0], sys.argv) #restart program with same command line args 

    driver.find_element_by_xpath(VERIFY_EMAIL_INPUT).send_keys(passcode)
    driver.find_element_by_xpath(VERIFY_EMAIL_BUTTON).click()

    printf(f"Success! Made {args.exploiter} account using email: {email}")


def fill_out_application_and_submit(driver, random_city, fake_identity):
    # make resume
    resume_filename = fake_identity['last_name']+'-Resume'
    make_resume(fake_identity['email'], resume_filename)
    images = convert_from_path(resume_filename+'.pdf')
    images[0].save(resume_filename+'.png', 'PNG')

    # wait for page to load
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.XPATH, PROFILE_INFORMATION_DROPDOWN)))

    # fill out form parts of app
    driver.find_element_by_xpath(PROFILE_INFORMATION_DROPDOWN).click()
    driver.find_element_by_xpath(CANDIDATE_SPECIFIC_INFORMATION_DROPDOWN).click()

    for key in XPATHS_1.keys():

        if key == 'resume':
            driver.find_element_by_xpath(UPLOAD_A_RESUME_BUTTON).click()
            info = os.getcwd() + '/'+resume_filename+'.png'
        elif key == 'addy':
            info = fake_identity['street_address']
        elif key == 'city':
            info = random_city
        elif key == 'zip':
            info = CITIES_TO_ZIP_CODES[random_city]
        elif key == 'job':
            info = fake_identity['job']
        elif key == 'salary':
            first = random.randrange(15000, 30000, 5000)
            info = f'{format(first, ",")}-{format(random.randrange(first + 5000, 35000, 5000), ",")}'

        driver.find_element_by_xpath(XPATHS_1.get(key)).send_keys(info)

    printf(f"successfully filled out app forms for {random_city}")

    # fill out dropdowns
    select = Select(driver.find_element_by_id(CITIZEN_QUESTION_LABEL))
    select.select_by_visible_text(YES)
    select = Select(driver.find_element_by_id(COUNTRY_OF_ORIGIN_LABEL))
    select.select_by_visible_text(FULL_NAME_US)
    select = Select(driver.find_element_by_id(EIGHTEEN_YEARS_OLD_LABEL))
    select.select_by_visible_text(YES)
    select = Select(driver.find_element_by_id(REQUIRE_SPONSORSHIP_LABEL))
    select.select_by_visible_text(NO)
    select = Select(driver.find_element_by_id(PREVIOUSLY_WORKED_LABEL))
    select.select_by_visible_text(NO)
    select = Select(driver.find_element_by_id(PREVIOUSLY_PARTNERED_LABEL))
    select.select_by_visible_text(NO)
    select = Select(driver.find_element_by_id(RELATIVE_WORKER_LABEL))
    select.select_by_visible_text(NO)
    select = Select(driver.find_element_by_id(ESSENTIAL_FUNCTIONS_LABEL))
    select.select_by_visible_text(YES)
    select = Select(driver.find_element_by_id(PREVIOUSLY_PARTNERED_LABEL))
    select.select_by_visible_text(NO)
    time.sleep(1)
    select = Select(driver.find_element_by_id(GENDER_LABEL))
    gender = random.choice(GENDERS_LIST)
    select.select_by_visible_text(gender)
    driver.find_element_by_xpath(MIXER_QUESTION_1_LABEL).click()
    driver.find_element_by_xpath(MIXER_QUESTION_2_LABEL).click()

    els = driver.find_elements_by_xpath(LONG_PERIODS_QUESTION_LABEL)
    [el.click() for el in els]

    time.sleep(5)
    driver.find_element_by_xpath(APPLY_BUTTON).click()
    printf(f"successfully submitted application")

    # take out the trash
    os.remove(resume_filename+'.pdf')
    os.remove(resume_filename+'.png')

def main():
    while True:
        random_city = random.choice(list(CITIES_TO_URLS.keys()))
        printf(f"Applying for job in {random_city}")
        try:
            driver = start_driver(random_city)
        except Exception as e:
            printf(f"FAILED TO START DRIVER: {e}")
            pass

        time.sleep(2)
        fake_identity = fid.generate_fake_identity(USING_MAILTM=args.using_mailtm, verbose=args.debug_enabled)

        try:
            generate_account(driver, fake_identity)
        except Exception as e:
            printf(f"FAILED TO CREATE ACCOUNT: {e}")
            pass

        try:
            fill_out_application_and_submit(driver, random_city, fake_identity)
        except Exception as e:
            printf(f"FAILED TO FILL OUT APPLICATION AND SUBMIT: {e}")
            pass
            driver.close()
            continue

        driver.close()
        time.sleep(5)


if __name__ == '__main__':
    main()
    sys.exit()
