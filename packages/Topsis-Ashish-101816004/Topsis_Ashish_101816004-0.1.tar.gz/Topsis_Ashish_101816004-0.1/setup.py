# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 15:34:54 2020

@author: ashish
"""

from distutils.core import setup
setup(
  name = 'Topsis_Ashish_101816004',         # How you named your package folder (MyLib)
  packages = ['Topsis_Ashish_101816004'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This library helps in implementing topsis method',   # Give a short description about your library
  author = 'Ashish Kumar Yadav',                   # Type in your name
  author_email = 'ayadav3_be18@thapar.edu',      # Type in your E-Mail
  url = 'https://github.com/blackdog1520/Topsis_Ashish_101816004',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/blackdog1520/Topsis_Ashish_101816004/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['SIMPLE', 'TOPSIS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'os',
		  'sys',
		  'numpy',
		  'pandas'
  
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)