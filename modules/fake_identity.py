#libs
import random
import requests
import re
from faker import Faker
from datetime import date

#custom funcs 
from configuration import printf, OUTPUT_PATH
from constants.areaCodes import AREA_CODES
from constants.email import MAIL_GENERATION_WEIGHTS
from constants.education import UNIVERSITIES, DEGREES
import resume_faker
import pdf2image

fake = Faker()

"""
    Used to generate a fake identity and handle the associated emails
"""

def random_email(name=None):
    if name is None:
        name = fake.name()

    mailGens = [lambda fn, ln, *names: fn + ln,
                lambda fn, ln, *names: fn + "_" + ln,
                lambda fn, ln, *names: fn[0] + "_" + ln,
                lambda fn, ln, *names: fn + ln + str(int(1 / random.random() ** 3)),
                lambda fn, ln, *names: fn + "_" + ln + str(int(1 / random.random() ** 3)),
                lambda fn, ln, *names: fn[0] + "_" + ln + str(int(1 / random.random() ** 3)), ]

    return random.choices(mailGens, MAIL_GENERATION_WEIGHTS)[0](*name.split(" ")).lower() + "@" + \
           requests.get('https://api.mail.tm/domains').json().get('hydra:member')[0].get('domain')

def random_phone(format=None):
    area_code = str(random.choice(AREA_CODES))
    middle_three = str(random.randint(0,999)).rjust(3,'0')
    last_four = str(random.randint(0,9999)).rjust(4,'0')

    if format is None:
        format = random.randint(0,4)

    if format==0:
        return area_code+middle_three+last_four
    elif format==1:
        return area_code+' '+middle_three+' '+last_four
    elif format==2:
        return area_code+'.'+middle_three+'.'+last_four
    elif format==3:
        return area_code+'-'+middle_three+'-'+last_four
    elif format==4:
        return '('+area_code+') '+middle_three+'-'+last_four

def generate_fake_identity(USING_MAILTM, generate_resume=False,verbose=False):
    """
        Generates a fake identity with a usable email address. 
        If USING_MAILTM is false, function uses GuerillaMail
    """
    fake_first_name = fake.first_name()
    fake_last_name = fake.last_name()
    fake_phone = random_phone()
    fake_address = fake.street_address()
    fake_job = fake.job()
    fake_password = fake.password()

    university = random.choice(UNIVERSITIES)
    degree = random.choice(DEGREES)
    
    year_today = date.today().year
    grad_year = random.randrange(1990,year_today-10)
    mid_year = int(grad_year + (year_today-grad_year)*0.1*random.randrange(3,7))

    printf(f"Creating eMail account with {'MailTM' if USING_MAILTM else 'GuerillaMail'}...")
    if USING_MAILTM:
        fake_email = requests.post('https://api.mail.tm/accounts', data='{"address":"'+random_email(fake_first_name+' '+fake_last_name)+'","password":" "}', headers={'Content-Type': 'application/json'}).json().get('address')
        mail_sid = requests.post('https://api.mail.tm/token', data='{"address":"'+fake_email+'","password":" "}', headers={'Content-Type': 'application/json'}).json().get('token')

    else:
        response = requests.get('https://api.guerrillamail.com/ajax.php?f=get_email_address').json()

        fake_email = response.get('email_addr')
        mail_sid = response.get('sid_token')
    printf(f"   Success! eMail created: {fake_email}")


    fake_identity = {
        'first_name': fake_first_name,
        'last_name': fake_last_name,
        'email': fake_email,
        'phone': fake_phone,
        'email_sid' : mail_sid,
        'street_address': fake_address,
        'job': fake_job,
        'password': fake_password,
        'university': university,
        'degree': degree,
        'grad_year': grad_year,
        'mid_year': mid_year,
    }

    if generate_resume:
        resume_filename = f"{fake_identity['first_name']} {fake_identity['last_name']}-Resume"
        fake_identity['resume_pdf_filepath'] = resume_faker.make_resume(fake_identity, resume_filename, verbose)
 
        images = pdf2image.convert_from_path(fake_identity['resume_pdf_filepath'])

        fake_identity['resume_img_filepath'] = OUTPUT_PATH / f'{resume_filename}.png'
        images[0].save(fake_identity['resume_img_filepath'], 'PNG')

    if verbose:
        printf("     Fake Identity created:")
        printf(f"Name          : {fake_identity['first_name']} {['last_name']}")
        printf(f"Education     : Degree in {fake_identity['degree']} from {fake_identity['university']}")
        printf(f"                   graduated in {fake_identity['grad_year']} with mid-year in {fake_identity['mid_year']}")
        printf(f"Phone Number  : {fake_identity['phone']}")
        printf(f"Street Address: {fake_identity['street_address']}")
        printf(f"Job Title     : {fake_identity['job']}")
        printf(f"eMail         : {fake_identity['email']}")
        printf(f"eMail SID     : {fake_identity['email_sid']}")
        printf(f"Password      : {fake_identity['password']}")
    
    return fake_identity

def get_passcode_from_email(USING_MAILTM, fake_identity):
    if USING_MAILTM:
        mail = requests.get("https://api.mail.tm/messages?page=1", headers={'Authorization':f'Bearer {fake_identity.get("sid")}'}).json().get('hydra:member')

        if mail:
            passcode = re.findall('(?<=n is ).*', requests.get(f'https://api.mail.tm{mail[0].get("@id")}', headers={'Authorization':f'Bearer {fake_identity.get("sid")}'}).json().get('text'))[0]
            return passcode

    else:
        mail = requests.get(f'https://api.guerrillamail.com/ajax.php?f=check_email&seq=1&sid_token={fake_identity.get("sid")}').json().get('list')

        if mail:
            passcode = re.findall('(?<=n is ).*?(?=<)', requests.get(f'https://api.guerrillamail.com/ajax.php?f=fetch_email&email_id={mail[0].get("mail_id")}&sid_token={fake_identity.get("sid")}').json().get('mail_body'))[0]
            return passcode


if __name__ == '__main__':
    generate_fake_identity(USING_MAILTM=False, verbose=True)

