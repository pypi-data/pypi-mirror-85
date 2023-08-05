# Name:        build.py (part of PyGMI)
#
# Author:      Patrick Cole
# E-Mail:      pcole@geoscience.org.za
#
# Copyright:   (c) 2013 Council for Geoscience
# Licence:     GPL-3.0
#
# This file is part of PyGMI
#
# PyGMI is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyGMI is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------
"""
Sphinx document builder.

This gets run from within the doc directory, with the main github branch. The
copydocs.cmd gets run once we have used git to change to the gh-pages branch.
Don't forget to update the PyGMI version in the conf.py file.
"""

import os
import glob
import shutil
import subprocess
import sphinx.cmd.build as build
import sphinx.ext.apidoc as apidoc
from pygmi import __version__ as PVER


# print('Checking git for logs...')
# subprocess.run(['start', '/WAIT', 'gittolog.sh', 'v'+PVER], shell=True)


# with open('changes.rst') as ifile:
#     ctext = ifile.readlines()

# with open('log.txt') as ifile:
#     ltext = ifile.readlines()


# if ltext[0] in ctext[3]:
#     ctext = ctext[:3] + ltext + ['\n'] + ctext[3:]

# with open('changes.rst', 'w') as ofile:
#     ofile.writelines(ctext)

os.chdir(r'c:\work\programming\pygmi\docs')

shutil.rmtree('./_build/html', ignore_errors=True)

files = glob.glob('./pygmi.*')
for ifile in files:
    os.remove(ifile)

argv = ['-f', '-o', './/', '..//pygmi']
apidoc.main(argv)

os.remove('.//modules.rst')

argv = ['-b', 'html', '.', './_build/html']

build.build_main(argv)
