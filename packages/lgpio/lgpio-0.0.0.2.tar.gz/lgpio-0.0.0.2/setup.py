#!/usr/bin/env python

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup (name = 'lgpio',
       version = '0.0.0.2',
       zip_safe=False,
       author='joan',
       author_email='joan@abyz.me.uk',
       maintainer='joan',
       maintainer_email='joan@abyz.me.uk',
       url='http://abyz.me.uk/lg/py_lgpio.html',
       description='Linux SBC GPIO module',
       long_description=long_description,
       long_description_content_type="text/markdown",
       download_url='http://abyz.me.uk/lg/lg.zip',
       license='unlicense.org',
       keywords=['linux', 'sbc', 'gpio',],
       classifiers=[
         "Programming Language :: Python :: 2",
         "Programming Language :: Python :: 3",
       ],
       py_modules = ["lgpio"],
       )

