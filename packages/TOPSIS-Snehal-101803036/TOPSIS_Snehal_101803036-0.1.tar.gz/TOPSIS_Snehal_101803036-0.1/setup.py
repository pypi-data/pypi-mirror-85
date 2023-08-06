# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 20:31:32 2020

@author: Snehal
"""

from setuptools import setup
def readme():
    with open('README.md') as f:
        README = f.read()
    return README
setup(
  name = 'TOPSIS_Snehal_101803036',         # How you named your package folder (MyLib)
  packages = ['TOPSIS_Snehal_101803036'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'We are calculating performances scores for each models which would be ranked and best model is considered',   # Give a short description about your library
  long_description=readme(),
  long_description_content_type="text/markdown",
  author = 'Snehal Shetty',                   # Type in your name
  author_email = 'sshetty_be18@thapar.edu',      # Type in your E-Mail
  url = 'https://github.com/Snehal-2310/TOPSIS_Snehal_101803036',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Snehal-2310/TOPSIS_Snehal_101803036/archive/0.1.tar.gz',    # I explain this later on
  install_requires=[            # I get to this in a second
          'pandas',
          'numpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ]
)