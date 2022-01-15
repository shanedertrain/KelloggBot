import random
from faker import Faker
from datetime import date
import re
import os
import subprocess

#custom
from constants.education import UNIVERSITIES, DEGREES

fake = Faker()

ROOT_FOLDER = './resumeSrc/'
TEMPLATES_FOLDER = ROOT_FOLDER+'templates/'
PACKAGES_FOLDER = ROOT_FOLDER+'packages/'
    
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
            
    if fake_identity:
        name = f"{fake_identity['first_name']} {fake_identity['last_name']}"
        email = fake_identity['email']
        phone = fake_identity['phone']

        university = fake_identity['university']
        degree = fake_identity['degree']
        grad_year = fake_identity['grad_year']
        mid_year = fake_identity['mid_year']
    else:
        name = fake.name()
        email = fake.free_email() 
        phone = fake.phone_number()

        university = random.choice(UNIVERSITIES)
        degree = random.choice(DEGREES)
        
        year_today = date.today().year
        grad_year = random.randrange(1990,year_today-10)
        mid_year = int(grad_year + (year_today-grad_year)*0.1*random.randrange(3,7))


    template = 'developercv.tex' # for testing
    #template = random.choice([file for file in os.listdir(TEMPLATES_FOLDER) if file.endswith('.tex')])

    with open(TEMPLATES_FOLDER+template) as input, open(PACKAGES_FOLDER+'auto_resume.tex', 'a') as output:
        for line in input.readlines():
            line = re.sub('@@WORDS@@', fake.sentence(6)[:-1], line)
            line = re.sub('@@PARAGRAPH@@', fake.paragraph(6), line)
            line = re.sub('@@BS@@', fake.bs(), line)

            line = re.sub('@@NAME@@', name, line)
            line = re.sub('@@FIRSTNAME@@', name.split(' ', 2)[0], line)
            line = re.sub('@@LASTNAME@@', name.split(' ', 2)[-1], line)

            line = re.sub('@@PHONE@@', phone, line)
            line = re.sub('@@EMAIL@@', email, line)
            line = re.sub('@@CITY@@', fake.city(), line)

            line = re.sub('@@UNIVERSITY@@', university, line)
            line = re.sub('@@DEGREE@@', degree, line)
            line = re.sub('@@ENROLLYEAR@@', str(grad_year-4), line)
            line = re.sub('@@GRADYEAR@@', str(grad_year), line)
            line = re.sub('@@GPA@@', str(round(3+random.random(), 2)).ljust(4,'0'), line)

            line = re.sub('@@THISYEAR@@', random.choice([str(year_today), 'Present']), line)
            line = re.sub('@@MIDDLEYEAR@@', str(mid_year), line)
            
            line = re.sub('@@JOB@@', fake.job(), line)
            line = re.sub('@@COMPANY@@', fake.company(), line)

            output.write(line)

    subprocess.call(
        ['pdflatex','auto_resume.tex'], 
        cwd=PACKAGES_FOLDER, 
        stderr = subprocess.DEVNULL if verbose else None, 
        stdout = subprocess.DEVNULL if verbose else None
    )
    os.rename(PACKAGES_FOLDER+'auto_resume.pdf','./'+filename+'.pdf')
    for ext in ['tex','aux','log','out']:
        try:
            os.remove(PACKAGES_FOLDER+'auto_resume.'+ext)
        except Exception:
            continue
