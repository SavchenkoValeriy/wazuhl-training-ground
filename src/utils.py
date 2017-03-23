import os
import shutil
import sys
from distutils.spawn import find_executable

def check_file(file_to_check):
    if not os.path.exists(file_to_check):
        error("There is no such file: \"{0}\"".format(file_to_check))

def check_executable(executable):
    if not find_executable(executable):
        error("Couldn't find '{0}' executable, please, check your environment".format(executable))

def error(message):
    print "Error:", message
    sys.exit(1)
