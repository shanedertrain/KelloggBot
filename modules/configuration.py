import functools
from pathlib import Path
import sys
import os
from distutils.spawn import find_executable

"""
    This is a file to contain any custom but generic functions that dont need their own file,
    since I'm separating a lot of things to make the functions more modular
"""

# Add printf: print with flush by default. This is for python 2 support.
# https://stackoverflow.com/questions/230751/how-can-i-flush-the-output-of-the-print-function-unbuffer-python-output#:~:text=Changing%20the%20default%20in%20one%20module%20to%20flush%3DTrue
printf = functools.partial(print, flush=True)

warn_installs = True #controls warnings for things not installed. can be disabled because it may be buggy. 

BASE_PATH = Path(__file__).parent.resolve()
DATA_PATH = BASE_PATH / 'data'
INPUT_PATH = DATA_PATH / 'input'
OUTPUT_PATH = DATA_PATH /'output'

def mkdir_if_not_exists(dir):
    if not Path.exists(dir):
        Path.mkdir(dir)
        printf(f"Created: {dir}")    

mkdir_if_not_exists(DATA_PATH)
mkdir_if_not_exists(INPUT_PATH)
mkdir_if_not_exists(OUTPUT_PATH) 

def ask_to_open_link(program_name, url, change_environ_vars=False):
    printf(f"\n{program_name} is not present. Please download / install {program_name}")
    printf(f"Wanna open this link to get {program_name}? URL: {url}")
    if input('Input "y" to open the link: ' ).upper() == 'Y':
        printf(f'Always verify that programs are taking you to real sites!\n    Opening: {url}')
        if sys.platform=='win32':
            os.startfile(url)
        elif sys.platform=='darwin':
            subprocess.Popen(['open', url])
        else:
            try:
                subprocess.Popen(['xdg-open', url])
            except OSError:
                print ('Please open a browser on: ')+url

    if change_environ_vars:
        if sys.platform=='win32':
            printf("You need to add the program to your environment variables. Please do so now.")
            os.system('"start rundll32 sysdm.cpl,EditEnvironmentVariables"')
    
if warn_installs:
    poppler_present = False
    ffmpeg_present = False
    latex_present = False

    if find_executable('latex'): 
        latex_present = True
        
    #ask to install FFMPEG, Poppler, LaTeX if not installed
    for variable in os.environ['Path'].split(';'):
        if 'poppler' in variable.lower():
            poppler_present = True
        elif 'ffmpeg' in variable.lower():
            ffmpeg_present = True
        elif 'miktex'in variable.lower():
            latex_present = True
    
    if not poppler_present:
        ask_to_open_link('Poppler', 'https://pdf2image.readthedocs.io/en/latest/installation.html#installing-poppler', change_environ_vars=True)

    if not ffmpeg_present:
        if sys.platform=='win32':
            ask_to_open_link('FFMpeg', 'https://www.wikihow.com/Install-FFmpeg-on-Windows', change_environ_vars=True)
        elif sys.platform=='darwin':
            ask_to_open_link('FFMpeg', 'https://superuser.com/questions/624561/install-ffmpeg-on-os-x/624562#624562', change_environ_vars=True)
    
    if not latex_present:
        if sys.platform=='win32':
            printf("Select the 'Install for all users option'")
            printf("    also select the 'Download packages as needed' option!")
            ask_to_open_link('LaTeX', 'https://miktex.org/download')
        elif sys.platform=='darwin':
            ask_to_open_link('FFMpeg', 'https://pdf2image.readthedocs.io/en/latest/installation.html#installing-poppler', change_environ_vars=True)

    if not poppler_present or not ffmpeg_present or not latex_present:
        printf("These warnings can be disabled by adding '--no_warn_installs' to the call for this program")
        printf("     Example 1: python main.py --no_warn_installs")
        printf("     Example 2: py -3 main.py --no_warn_installs")
