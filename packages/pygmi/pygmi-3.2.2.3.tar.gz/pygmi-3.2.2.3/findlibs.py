"""
Created on Wed Mar  6 14:36:46 2019.

@author: pcole
"""

import glob
import os.path
import sys
import pkg_resources
import importlib

python_path = os.path.dirname(sys.executable)


ifiles = glob.glob(r'C:\Work\Programming\pygmi\**\*.py', recursive=True)
exclude = ['findlibs.py', 'pygmi_pypi.py', 'conf.py', 'confold.py',
           'builddocs.py', 'build.py']

tmp = []
for ifile in ifiles:
    if os.path.basename(ifile) in exclude:
        continue
    file = open(ifile)
    data = file.readlines()
    for j2 in data:
        j = j2.split()
        if len(j) == 0:
            continue
        if 'pygmi' in j2:
            continue
        if j[0] == 'import':
            tmp.append(j[1].split('.')[0])

        if j[0] == 'from':
            tmp.append(j[1].split('.')[0])

if 'numba' in tmp:
    tmp.append('llvmlite')

if 'geopandas' in tmp:
    tmp.append('shapely')
    tmp.append('fiona')

tmp2 = set(tmp)


tmp3 = []
tmps = []
for i in tmp2:
    if i == 'ogr' or i == 'osr' or i == 'osgeo':
        i = 'gdal'

    if i == 'setuptools':
        print('Dropping setuptools reference.')
        continue

    if i == 'IPython':
        print('Dropping IPython reference.')
        continue

    mspec = importlib.util.find_spec(i)

    if mspec is None:
        print('no module named', i)
        continue

    if mspec.origin is None:
        continue

    if 'site-packages' not in mspec.origin:
        continue

    if i == 'PIL':
        i = 'pillow'

    if i == 'OpenGL':
        i = 'pyopengl'

    if i == 'skimage':
        i = 'scikit-image'

    if i == 'sklearn':
        i = 'scikit-learn'

    if 'site-packages' in mspec.origin:
        tmps.append(i)
        try:
            i += ' ' + pkg_resources.get_distribution(i).version
        except:
            breakpoint()
        tmp3.append(i)

tmp3.sort()
tmps.sort()

tmp3 = sorted(tmp3, key=str.casefold)
tmps = sorted(tmps, key=str.casefold)

print('################')
print('* python '+sys.version.split()[0])
for i in tmp3:
    print('* '+i)

print('')
print('      install_requires=['+"'"+tmps[0]+"',")
for i in tmps[1:]:
    print(24*' '+"'"+i+"',")
print(24*' '+"'setuptools'],")
