#! /usr/bin/env python3 

import setuptools
import os
import re
import subprocess as subproc

PACKAGE = setuptools.find_packages(exclude=('tests',))[0]

def req_esorex(min_version=(3, 11), cpl_min_version=(6, 5)):

    proc = subproc.Popen(['esorex', '--version'],
                    stdout=subproc.PIPE, stderr=subproc.PIPE)
    stdout, stderr = proc.communicate()
    if len(stderr):
        raise RuntimeError('esorex not properly installed')
    
    help = stdout.decode()
    
    if match := re.search('version (\S+)', help):
        sversion = match.groups()[0]
        version = tuple(int(x) for x in sversion.split('.'))
    else:
        min_sversion = '.'.join([str(x) for x in min_version])
        raise RuntimeError('esorex not properly installed')

    if version < min_version:
        raise RuntimeError(f'esorex version {sversion} too old, {min_sversion} is needed')
    
    if match := re.search('CPL = ([^ ,]+)', help):
        sversion = match.groups()[0]
        version = tuple(int(x) for x in sversion.split('.'))
    else:
        raise RuntimeError(f'CPL is not installed properly')
    
    if version < cpl_min_version:
        min_sversion = '.'.join([str(x) for x in cpl_min_version])
        raise RuntimeError(f'CPL version {sversion} too old, {min_sversion} is needed')

 
def req_instrument_pipeline(ins, min_version=()):
    
    if isinstance(min_version, str):
        min_version = tuple(int(v) for v in min_version.split('.'))
    
    proc = subproc.Popen(['esorex', '--params'], 
                    stdout=subproc.PIPE, stderr=subproc.PIPE)
    stdout = proc.communicate()[0]
    
    match = re.search('recipe-dir\s*: (.*)', stdout.decode())
    if not match:
        raise RuntimeError(f'No esorex recipe dir, installation is broken')
    
    paths = match.groups()[0].split(':')
    plugins = [pl for p in paths if os.path.exists(p) for pl in os.listdir(p)]
    packages = [pl for pl in plugins if pl.split('-')[0] == ins]
    if len(packages) == 0:
       raise RuntimeError(f'{ins} recipes not installed')
    
    package = packages[0]
    sversion = package.split('-')[1]
    version = tuple(int(v) for v in sversion.split('.'))
    if version < min_version:
        min_sversion = '.'.join([str(x) for x in min_version])
        raise RuntimeError(f'{ins} package version {sversion} too old, {min_sversion} is needed')
    
 
def get_readme():
    with open("README.md", "r") as fh:
        text = fh.read()
    return text

def read_init(splitlines=False):

    here = os.path.abspath(os.path.dirname(__file__))
    filename = os.path.join(here, PACKAGE, '__init__.py')

    with open(filename) as fh:
        lines = fh.read()
    if splitlines:
        lines = lines.splitlines()

    return lines

def get_version():
    
    lines = read_init(splitlines=True)
    
    for line in lines:
        if match := re.search('__version__\s*=\s*([\'"])(.*)\\1', line):
            return match.groups()[1]

    raise RuntimeError("Unable to find version string.")

# Check esorex and instrument pipelines

INSTRUMENT_REQUIREMENTS = ['gravity>=1.4']
INSTRUMENTS = [ins.split('>=')[0] for ins in INSTRUMENT_REQUIREMENTS]
INSTRUMENT_SCRIPTS = [ 
    f"{ins}pipe = esopipeline.__main__:{ins}" for ins in INSTRUMENTS
]

req_esorex()
for req in INSTRUMENT_REQUIREMENTS:
    req_instrument_pipeline(*req.split('>='))

# Python package install
 
setuptools.setup(
    name='esopipeline',
    version=get_version(),
    packages=setuptools.find_packages(),
    license='LICENSE.txt',
    author="Régis Lachaume",
    author_email="regis.lachaume@gmail.com",
    description='Process astronomical data from European Southern Observatory',
    long_description=get_readme(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha ",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "License :: Public Domain",
    ],
    python_requires='>=3.8',
    install_requires=[
        "astropy", 
        "numpy",
        "pyoifits",
    ],
    entry_points={
        "console_scripts": [
            "esopipe = esopipeline.__main__:main",
        ] + INSTRUMENT_SCRIPTS
    },
    include_package_data=True,
)
