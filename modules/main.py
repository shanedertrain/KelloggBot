from inspect import trace
import os
import random
import sys
import time
import argparse
import atexit
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
os.environ['WDM_LOG_LEVEL'] = '0'

#custom stuff
from configuration import printf
import configuration as config
import fake_identity as fid
import kellogs_spammer
import kroger_spammer

from constants.parser import SCRIPT_DESCRIPTION, EPILOG, DEBUG_DESCRIPTION, MAILTM_DESCRIPTION
from constants.common import USER_AGENT

os.environ["PATH"] += ":/usr/local/bin" # Adds /usr/local/bin to my path which is where my ffmpeg is stored

#Option parsing
parser = argparse.ArgumentParser(SCRIPT_DESCRIPTION,epilog=EPILOG)
parser.add_argument('--debug',action='store_true',default=False,required=False,help=DEBUG_DESCRIPTION,dest='debug_enabled')
parser.add_argument('--mailtm',action='store_true',default=False,required=False,help=MAILTM_DESCRIPTION,dest='using_mailtm')
parser.add_argument('--no_warn_installs', action='store_false', default=True, dest='warn_installs')
parser.add_argument('--exploiter', action='store', default='kroger', dest='exploiter')
args = parser.parse_args()
# END TEST

config.warn_installs = args.warn_installs

def start_driver(verbose=False):
    options = Options()
    if args.debug_enabled:
        driver = webdriver.Chrome(ChromeDriverManager().install())
    else:
        options.add_argument(f"user-agent={USER_AGENT}") #TODO randomize user agent? 
        options.add_argument('disable-blink-features=AutomationControlled')
        options.headless = True
        driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        driver.set_window_size(1440, 900)
    
    if verbose:
        printf("Started driver!")

    return driver


def main():
    print(f"debug enabled: {args.debug_enabled}")
    exploiter = str(args.exploiter.lower()) #wrapped in string for linter

    try:
        while True: 
            try:
                driver = start_driver()
                atexit.register(driver.close)
            except Exception as e:
                if args.debug_enabled: traceback.print_exc()
                printf(f"FAILED TO START DRIVER: {e}")

            try:
                fake_identity = fid.generate_fake_identity(USING_MAILTM=args.using_mailtm, 
                                                    generate_resume=True, verbose=args.debug_enabled)
                
                if exploiter == 'kellogs':
                    random_city = kellogs_spammer.generate_account(driver, fake_identity, using_mailtm=args.using_mailtm)
                elif exploiter =='kroger':
                    #fake_identity['email'] = f"{fake_identity['email'].split('@')[0]}@{random.choice(['gmail.com', 'outlook.com'])}"
                    random_city = kroger_spammer.generate_account(driver, fake_identity)

            except Exception as e: 
                if args.debug_enabled: traceback.print_exc()
                printf(f"FAILED TO CREATE ACCOUNT: {e}")

            try:
                if exploiter == 'kellogs':
                    kellogs_spammer.fill_out_application_and_submit(driver, random_city, fake_identity)
                elif exploiter =='kroger':
                    kroger_spammer.fill_out_application_and_submit(driver, random_city, fake_identity, upload_resume=random.choice([False, True]),verbose=args.debug_enabled)
                    
            except Exception as e:
                if args.debug_enabled: traceback.print_exc()
                printf(f"FAILED TO FILL OUT APPLICATION AND SUBMIT: {e}")

            time.sleep(5)
            driver.close()
            os.remove(fake_identity['resume_img_filepath'])
            os.remove(fake_identity['resume_pdf_filepath'])
    except KeyboardInterrupt:
        printf("Exited via keyboard")
    except Exception:
        traceback.print_exc()


if __name__ == '__main__':
    main()
    sys.exit()
