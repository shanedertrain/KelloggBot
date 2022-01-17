#xpaths for application
XPATHS_1 = {
    'resume': '//*[@id="49:_file"]',
    'addy': '//*[@id="106:_txtFld"]',
    'city': '//*[@id="122:_txtFld"]',
    'state': '//*[@id="118:_select"]',
    'zip': '//*[@id="126:_txtFld"]',
    'country': '//*[@id="195:_select"]',
    'phone_number': '//*[@id="75:_txtFld"]'
}

XPATHS_WORK_HISTORY = {
    'employer': '//*[@id="139:_select"]',
    'job': '//*[@id="101:_txtFld"]',
    'salary': '//*[@id="172:_txtFld"]',
}

XPATHS_EDUCATION = {
    'education_type' : '//*[@id="532:_select"]',
    'country': '//*[@id="536:_select"]', 
    'state': '//*[@id="540:_select"]',
    'city': '//*[@id="544:_txtFld"]', 
    'school': '//*[@id="548:_select"]',
    'degree_status': '//*[@id="556:_select"]',
    'area_of_study': '//*[@id="560:_select"]'
}

XPATHS_JOB_SPECIFIC ={
    'ssn' : '//*[@id="509:"]',
    'learned_how': '//*[@id="275:_select"]',
    'classes_attending': '//*[@id="283:_select"]',
    'highest_education': '//*[@id="287:_select"]',
    'employed_relatives': '//*[@id="291:_select"]',
    'veteran': '//*[@id="299:_select"]',
    '18_or_older': '//*[@id="303:_select"]',
    'prohibition': '//*[@id="307:_select"]',
    'first_choice': '//*[@id="315:_select"]',
    'second_choice': '//*[@id="319:_select"]',
    'start_date': '//*[@id="331:_write"]',
    'evenings': '//*[@id="337:_select"]',
    'weekends': '//*[@id="341:_select"]',
    'holidays': '//*[@id="345:_select"]',
    'type_desired': '//*[@id="349:_select"]',
    'best_call_time': '//*[@id="353:_select"]',
    'available_sunday': '//*[@id="361:_select"]',
    'available_monday': '//*[@id="361:_select"]',
    'available_tuesday': '//*[@id="361:_select"]',
    'available_wednesday': '//*[@id="361:_select"]',
    'available_thursday': '//*[@id="361:_select"]',
    'available_friday': '//*[@id="361:_select"]',
    'available_saturday': '//*[@id="361:_select"]',
    'worked_here_before': '//*[@id="393:_txtArea"]',
    'other_work_fits': '//*[@id="397:_txtArea"]',
    'terminated': '//*[@id="401:_select"]',
    'terminated_describe': '//*[@id="405:_txtArea"]',
    'cash_shortages': '//*[@id="409:_select"]',
    'cash_shortages_describe': '//*[@id="413:_txtArea"]',
    'conviction': '//*[@id="425:_txtFld"]',
    'convicted': '//*[@id="429:_select"]',
    'convicted_describe': '//*[@id="433:_txtArea"]',
    'contact_first_name': '//*[@id="441:_txtFld"]',
    'contact_last_name': '//*[@id="449:_txtFld"]',
    'contact_relationship': '//*[@id="453:_select"]',
    'contact_phone_number': '//*[@id="457:_txtFld"]',
    'app_statement_ack': '//*[@id="477:_select"]',
    'app_statement_ack_signature': '//*[@id="481:_txtFld"]',
    'ethnicity': '//*[@id="493:_select"]',
    'gender_female': '//*[@id="499:_anchorButton"]/span',
    'gender_male': '//*[@id="500:_anchorButton"]',
    '15_or_older': '//*[@id="218:_anchorButton"]/span',
    '18_or_older': '//*[@id="224:_anchorButton"]',
    '12_or_older': '//*[@id="230:_anchorButton"]/span',
    'legal_verification': '//*[@id="236:_anchorButton"]',
    'accomodation': '//*[@id="242:_anchorButton"]/span',
    'overnight_yes': '//*[@id="248:_anchorButton"]/span',
    'overnight_no': '//*[@id="249:_anchorButton"]'
}

#Xpaths for create account screen
XPATHS_2 = {
    'email': '//*[@id="fbclc_userName"]',
    'email-retype': '//*[@id="fbclc_emailConf"]',
    'pass': '//*[@id="fbclc_pwd"]',
    'pass-retype': '//*[@id="fbclc_pwdConf"]',
    'first_name': '//*[@id="fbclc_fName"]',
    'last_name': '//*[@id="fbclc_lName"]',
    'country': '//*[@id="fbclc_country"]', 
}
CREATE_ACCOUNT_BUTTON = '//*[@id="fbclc_createAccountButton"]'
READ_TERMS_BUTTON = '//*[@id="dataPrivacyId"]'
ACCEPT_TERMS_BUTTON = '//*[@id="dlgButton_20:"]'

XPATHS_LOGIN = {
    'email' : '//*[@id="username"]',
    'password': '//*[@id="password"]',
    'sign_in' : '//*[@id="page_content"]/div[2]/div/div/div[2]/div/div/table/tbody/tr[3]/td[2]/span[1]/span/button'
}

CREATE_AN_ACCOUNT_BUTTON = '//*[@id="page_content"]/div[2]/div/div/div[2]/div/div/div[2]/a'

#resume app
MY_DOCUMENTS_DROPDOWN = '//*[@id="51:topBar"]'
UPLOAD_A_RESUME_BUTTON = '//*[@id="52:_attachLabel"]'
UPLOAD_FROM_DEVICE_BUTTON = '//*[@id="53:_file"]'

PROFILE_INFORMATION_DROPDOWN = '//*[@id="134:topBar"]'
WORK_HISTORY_DROPDOWN = '//*[@id="136:topBar"]'
EDUCATION_EXPERIENCE_DROPDOWN = '//*[@id="212:topBar"]'
JOB_SPECIFIC_INFO_DROPDOWN = '//*[@id="508:topBar"]'

APPLY_BUTTON = '//*[@id="510:_submitBtn"]'

READ_ACCEPT_DATA_PRIVACY_STATEMENT_ANCHORTAG = '//*[@id="dataPrivacyId"]'
ACCEPT_BUTTON = '//*[@id="dlgButton_20:"]'
VERIFY_EMAIL_INPUT = '//*[@id="passcode"]'
VERIFY_EMAIL_BUTTON = '//*[@id="continueBtn"]'
CANDIDATE_SPECIFIC_INFORMATION_DROPDOWN = '//*[@id="260:topBar"]'
MIXER_QUESTION_1_LABEL = '//label[text()="350 LBS"]'
MIXER_QUESTION_2_LABEL = '//label[text()="800 LBS"]'
LONG_PERIODS_QUESTION_LABEL = '//label[text()="Yes"]'

