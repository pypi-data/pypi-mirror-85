# BOTLIB - bot programming library
#
#

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
    version='108',
    url='https://bitbucket.org/bthate/botlib',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="the bot library",
    long_description=read(),
    install_requires=["libobj"],
    license='Public Domain',
    package_dir={'': 'bot'},
    py_modules=mods("bot"),
    zip_safe=False,
    scripts=["bin/bot"],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
