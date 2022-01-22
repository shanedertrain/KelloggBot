import random
from datetime import date
import re
import os
import subprocess
from pathlib import Path
from faker import Faker

#custom
from constants.education import UNIVERSITIES, DEGREES
from configuration import OUTPUT_PATH, MODULES_PATH

fake = Faker()

ROOT_FOLDER = MODULES_PATH / 'resumeSrc'
TEMPLATES_FOLDER = ROOT_FOLDER / 'templates'
PACKAGES_FOLDER = ROOT_FOLDER / 'packages'
    
def make_resume(fake_identity=None, filename='resume', verbose=False):
    """
        Generates a fake resume. Meant to be used with Fake Identity Gen
            but will generate a random identity if None is used. 
    """
    for ext in ['tex','aux','log','out']:
        try:
            os.remove(PACKAGES_FOLDER+'auto_resume.'+ext)
        except Exception:
            continue

    year_today = date.today().year    
    if fake_identity:
        name = f"{fake_identity['first_name']} {fake_identity['last_name']}"
        email = fake_identity['email']
        phone = fake_identity['phone']

        university = fake_identity['university']
        degree = fake_identity['degree']
        grad_year = fake_identity['grad_year']
        mid_year = fake_identity['mid_year']
        city = fake_identity['city']
    else:
        name = fake.name()
        email = fake.free_email() 
        phone = fake.phone_number()
        city = fake.city()

        university = random.choice(UNIVERSITIES)
        degree = random.choice(DEGREES)
        grad_year = random.randrange(1990,year_today-10)
        mid_year = int(grad_year + (year_today-grad_year)*0.1*random.randrange(3,7))


    template = 'developercv.tex' # for testing
    #template = random.choice([file for file in os.listdir(TEMPLATES_FOLDER) if file.endswith('.tex')])

    with open(TEMPLATES_FOLDER / template) as input, open(PACKAGES_FOLDER / 'auto_resume.tex', 'a') as output:
        for idx, line in enumerate(input.readlines()):
            fake_job = fake.job()
            fake_company = fake.company()

            line = re.sub('@@WORDS@@', fake.sentence(6)[:-1], line)
            line = re.sub('@@PARAGRAPH@@', fake.paragraph(6), line)
            line = re.sub('@@BS@@', fake.bs(), line)

            line = re.sub('@@NAME@@', name, line)
            line = re.sub('@@FIRSTNAME@@', name.split(' ', 2)[0], line)
            line = re.sub('@@LASTNAME@@', name.split(' ', 2)[-1], line)

            line = re.sub('@@PHONE@@', phone, line)
            line = re.sub('@@EMAIL@@', email, line)
            line = re.sub('@@CITY@@', city, line)

            line = re.sub('@@UNIVERSITY@@', university, line)
            line = re.sub('@@DEGREE@@', degree, line)
            line = re.sub('@@ENROLLYEAR@@', str(grad_year-4), line)
            line = re.sub('@@GRADYEAR@@', str(grad_year), line)
            line = re.sub('@@GPA@@', str(round(3+random.random(), 2)).ljust(4,'0'), line)

            line = re.sub('@@THISYEAR@@', random.choice([str(year_today), 'Present']), line)
            line = re.sub('@@MIDDLEYEAR@@', str(mid_year), line)
            
            line = re.sub('@@JOB@@', fake_job, line)
            line = re.sub('@@COMPANY@@', fake_company, line)

            output.write(line)

            fake_identity[f'job_{idx}'] = fake_job
            fake_identity[f'company_{idx}'] = fake_company
            
    print(f"!!!!!!verbose for pdflatex: {verbose}!!!!!!")
    subprocess.call(
        ['pdflatex','auto_resume.tex'], 
        cwd=PACKAGES_FOLDER, 
        stderr = subprocess.DEVNULL if verbose else None, 
        stdout = subprocess.DEVNULL if verbose else None
    )

    output_filepath = OUTPUT_PATH / f'{filename}.pdf'

    os.rename(PACKAGES_FOLDER / 'auto_resume.pdf', output_filepath)
    for ext in ['tex','aux','log','out']:
        try:
            os.remove(PACKAGES_FOLDER / 'auto_resume.'+ext)
        except Exception:
            continue
    
    fake_identity['resume_pdf_filepath'] = output_filepath

    return fake_identity

    
