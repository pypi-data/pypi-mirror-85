from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README

setup(
  name = 'TOPSIS-suryansh-101983044',         # How you named your package folder (MyLib)
  packages = ['TOPSIS-suryansh-101983044'],   # Chose the same as "name"
  version = '3.01',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A python module to implement Multiple Criteria Decision Making using TOPSIS ranking.',   # Give a short description about your library
  long_description=readme(),
  long_description_content_type='text/markdown',
  author = 'Suryansh Bhardwaj',                   # Type in your name
  author_email = 'suryanshbhar@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/suryanshbhar/TOPSIS-suryansh-101983044',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/suryanshbhar/TOPSIS-suryansh-101983044/archive/version0,3.tar.gz',    # I explain this later on
  keywords = ['new version','SIMPLE', 'TOPSIS', 'DATA SCIENCE','MULTI DECISION CRITERIA'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
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
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)