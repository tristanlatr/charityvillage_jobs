#! /usr/bin/env python3

from setuptools import setup
import sys
if sys.version_info[0] < 3: 
    raise Exception("Sorry, you must use Python 3")
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text(encoding='utf-8')

setup(
    name='charityvillage_jobs',
    description="""This is a Scrapy project to scrape jobs from [charityvillage.com](https://charityvillage.com).""",
    url='https://github.com/tristanlatr/charityvillage_jobs',
    maintainer='tristanlatr',
    version='1',
    packages=['charityvillage_jobs','charityvillage_jobs.spiders'],
    install_requires=[ 'scrapy', 'bs4', 'scrapy-selenium' ],
    classifiers=[ "Programming Language :: Python :: 3", ],
    license='The MIT License',
    long_description=README,
    long_description_content_type="text/markdown"
)