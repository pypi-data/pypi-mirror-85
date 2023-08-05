# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 15:03:58 2020

@author: pcole
"""

import os
import sys
import subprocess
import shutil


os.chdir(r'c:\work\programming\pygmi')

shutil.rmtree(r'dist', ignore_errors=True)
shutil.rmtree(r'build', ignore_errors=True)

pipe = subprocess.run(['python', r'setup.py', 'sdist', 'bdist_wheel'],
                      capture_output=True)
print(pipe.stdout.decode())
print(pipe.stderr.decode())

pipe = subprocess.run(['twine', 'check', r'dist/*'], capture_output=True)

print(pipe.stdout.decode())
print(pipe.stderr.decode())

pipe = subprocess.run(['twine', 'upload', r'dist/*',
                       '-u', 'pcole',
                       '-p', 'themightywarzone'], capture_output=True)

print(pipe.stdout.decode())
print(pipe.stderr.decode())

shutil.rmtree(r'dist', ignore_errors=True)
shutil.rmtree(r'build', ignore_errors=True)
