#!/usr/bin/env python
import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
name = 'KE'
about = {}

with open(os.path.join(here, name, 'version.py'), 'r') as f:
    exec(f.read(), about)


with open('README.md', 'rb') as f_readme:
    readme = f_readme.read().decode('utf-8')

setup(
    name="KE-py",
    version=about['__version__'],

    description='Python wrapper around the KE API',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='dennis li',
    author_email='xfl1991@163.com',
    url='https://github.com/Kyligence/KE-py',
    download_url='https://github.com/Kyligence/KE-py',
    keywords=['kyligence', 'kyligence enterprise', 'KE'],
    license='MIT License',
    classifiers=[
            'Intended Audience :: Developers',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.7',
    ],
    install_requires=["requests", "pandas", "ipython", "six"],
    packages=find_packages(),
    include_package_data=True,
)
