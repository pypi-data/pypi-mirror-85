import os
from codecs import open

from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), "README.md")) as f:
    long_description = f.read()

setup(
  name = 'umaat',         
  packages = ['umaat'],
  version = '0.1',
  license='MIT',
  description = ' This is a package that houses the  functions which can produce accuracy results for each algorithm in the categories of  Clustering,Regression & Classification based on passing the arguments - independent and dependent variables/features',
  long_description = long_description,
  long_description_content_type = "text/markdown",
  author = ['Vishal Balaji Sivaraman'],
  author_email = 'vb.sivaraman_official@yahoo.com',
  url = 'https://github.com/The-SocialLion/physicscalc',
  download_url = 'https://github.com/The-SocialLion/physicscalc/archive/master.zip',
  keywords = ['Machiene', 'Machiene Learning', 'Learning','accuracy','class and object','Calculator','Test','Model','Accuracy Test','Accuracy Calculator','Ultimate'],   
  install_requires=[           
          'numpy',
          'pandas',
          'Matplotlib',
          'scikit-learn'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)
