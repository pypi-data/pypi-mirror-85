# BOTLIB - bot programming library
#
#

"library to program bots"

import os

from setuptools import setup

def mods(names):
    m = []
    for name in names.split(","):
        m.extend([x.split(os.sep)[-1][:-3] for x in os.listdir(name) 
                                           if x.endswith(".py")
                                           and not x == "setup.py"])
    return m

def read():
    return open("README.rst", "r").read()

setup(
    name='botlib',
    version='109',
    url='https://bitbucket.org/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="the bot library",
    long_description=read(),
    license='Public Domain',
    package_dir={'': 'lib'},
    py_modules=mods("lib"),
    zip_safe=False,
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
